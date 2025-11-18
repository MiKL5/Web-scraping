import streamlit as     st
import pandas    as     pd
from   pathlib   import Path
import time
import json
import csv
import subprocess


# Configurer la page
st.set_page_config(
    page_title="FelisCrawler",
    page_icon="🐱",
    layout="wide"
)

st.title("🐱 **FelisCrawler** 🐈")
st.markdown("")

# Initialiser la session
if "scraping" not in st.session_state:
    st.session_state["scraping"]    = False
if "last_output" not in st.session_state:
    st.session_state["last_output"] = None

# État pour la fenêtre de confirmation de téléchargement
if "show_download_modal" not in st.session_state:
    st.session_state["show_download_modal"] = False
if "download_info" not in st.session_state:
    st.session_state["download_info"] = {}

# Utilitaire pour nommer le CSV à partir du JSON
def _csv_name(json_name: str) -> str:
    try:
        p = Path(json_name)
        return str(p.with_suffix(".csv"))
    except Exception:
        return (json_name.rsplit(".", 1)[0] if "." in json_name else json_name) + ".csv"

# Ouvre la modale de confirmation
def _open_download_modal(file_name: str, kind: str, server_hint: str | None = None):
    st.session_state["download_info"] = {
        "kind": kind,
        "file_name": file_name,
        "icon": "https://upload.wikimedia.org/wikipedia/commons/c/c6/.csv_icon.svg" if kind == "csv"
                else "https://upload.wikimedia.org/wikipedia/commons/c/c9/JSON_vector_logo.svg",
        "server_hint": server_hint or ""
    }
    st.session_state["show_download_modal"] = True

# Sidebar des paramètres
st.sidebar.title("⚙️ Configurer le scraper")
st.sidebar.header(" ") # espacement
st.sidebar.header(" ") # espacement

depth_limit = st.sidebar.slider(
    "Quelle est la profondeur de crawl ?",
    min_value= 1,
    max_value= 5,
    value    = 4,
    help     = "C'est le nombre de niveaux de liens à suivre. Plus c'est élevé, plus ça consomme de ressources."
)

st.sidebar.header(" ") # espacement

download_delay = st.sidebar.number_input(
    "Combien de secondes entre les requêtes ?",
    min_value  =   .5,
    max_value  = 10.0,
    value      =  1.23,
    step       =   .1,
    help       = "Temps d'attente entre chaque requête HTTP. Il est recommandé d'être ≥ 1 s pour respecter les serveurs."
)

st.sidebar.header(" ") # espacement

concurrent_requests = st.sidebar.slider(
    "Combien de requêtes simultanées ?",
    min_value       =  1,
    max_value       = 12,
    value           =  4,
    help            = "Plus il y a de requêtes en parallèle, plus le serveur est chargé."
)

st.sidebar.header(" ") # espacement

output_file = st.sidebar.text_input(
    "Le nom du fichier (JSON) est",
    value   = "result.json",
    help    = "Nom du fichier JSON où sauvegarder les résultats du scraping."
)
st.sidebar.header(" ") # espacement

st.sidebar.markdown("___")
st.sidebar.markdown(" ") # Espacement
st.sidebar.markdown(" ") # Espacement
st.sidebar.markdown("### 🌱 Les recommandations sont")
st.sidebar.markdown(
    "* La profondeur de **_2 à 4_**\n"
    "* Le délai doit être **_≥ 1 s_**\n"
    "* Et **_≤ 8_** requêtes simultanées\n"
)
st.sidebar.markdown(" ") # Espacement
st.sidebar.markdown(" ") # Espacement
st.sidebar.markdown(" ") # Espacement
# Bouton pour crawler
if st.sidebar.button("🚀 Je scrape !", type="primary"):
    st.session_state["scraping"]   = True
    st.session_state["start_time"] = time.time()

    output_file_csv = _csv_name(output_file)

    cmd = [
        "scrapy" , "runspider" , "wikichat_spider.py",
        "-O", output_file,
        "-O", output_file_csv,  # sortie CSV en parallèle
        "-s", f"DEPTH_LIMIT={depth_limit}",
        "-s", f"DOWNLOAD_DELAY={download_delay}",
        "-s", f"CONCURRENT_REQUESTS={concurrent_requests}",
    ]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⏱️ Progression...")

    pages_metric = st.sidebar.empty()
    pages_metric.metric("Pages scrapées", 0)

    with st.spinner("🔄 Patience... je scrape..."):
        progress_bar   = st.progress(0)
        status_text    = st.empty()

        pages_count    = 0
        progress       = 0

        try:
            p_json = Path(output_file)
            p_csv  = Path(output_file_csv)
            if p_json.exists():
                p_json.unlink()
            if p_csv.exists():
                p_csv.unlink()
        except Exception as _:
            pass

        try:
            process     = subprocess.Popen(
                cmd,
                stdout  = subprocess.PIPE,
                stderr  = subprocess.STDOUT,
                text    = True,
                bufsize = 1
            )

            log_output  = []

            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                log_output.append(line)
                status_text.text(line)

                # Heuristique simple : compter les pages crawlées
                if "Crawled" in line or "Scraped" in line:
                    pages_count += 1
                    pages_metric.metric("Pages scrapées", pages_count)

                # Progression pseudo-approximative (0 → 90 %)
                progress = min(progress + 1, 90)
                progress_bar.progress(progress)

            process.wait()

            if process.returncode == 0:
                progress_bar.progress(100)
                st.success("✅ Le scraping est terminé.")
                st.session_state["scraping"]    = False
                st.session_state["last_output"] = output_file
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(f"❌ Erreur lors du scraping (code: {process.returncode})")
                with st.expander("📋 Voir les journaux"):
                    st.code("\n".join(log_output))

        except FileNotFoundError:
            st.error("❌ Le spider est introuvable.")
        except Exception as e:
            st.error(f"❌ Il y a une erreur 👉 {str(e)}")

# Charger les données
output_path = Path(output_file)
data        = None
df          = None

if output_path.exists():
    try:
        raw_text = output_path.read_text(encoding="utf-8")
        data     = json.loads(raw_text)

        if data:
            df_data = []
            for item in data:
                df_data.append({
                    "Titre"      : item.get("titre", "N/A"),
                    "Profondeur" : item.get("profondeur", 0),
                    "Paragraphes": item.get("nombre_paragraphes", 0),
                    "Images"     : item.get("nombre_images", 0),
                    "Longueur"   : item.get("longueur_contenu", 0),
                    "L'adresse"  : item.get("url", ""),
                })

            df = pd.DataFrame(df_data)

            # fallback : garantir un CSV si Scrapy ne l'a pas écrit
            try:
                csv_fallback = _csv_name(output_file)
                if len(df) and not Path(csv_fallback).exists():
                    df.to_csv(csv_fallback, index=False, encoding="utf-8-sig")
            except Exception:
                pass

    except json.JSONDecodeError:
        st.error("❌ Le fichier de résultats est vide ou invalide. Lance un scraping.")
    except Exception as e:
        st.error(f"❌ Erreur à la lecture du fichier 👉 {str(e)}")

# Les onglets principaux
tab_config, tab_results, tab_plots, tab_ethics = st.tabs(
    ["⚙️ La config. et l'état", "📊 Les résultats", "📈 Les graphiques", "⚖️ Éthique & infos"]
)

# 1er Onglet : La configuration
with tab_config:
    st.subheader("⚙️ La configuration actuelle est")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(f"Profondeur", depth_limit)
    with col2:
        st.metric(f"Délai", download_delay)
    with col3:
        st.metric(f"Requêtes simultanées", concurrent_requests)
    with col4:
        st.write("**Le fichier de sortie est**")
        st.code(str(output_file))

    if st.session_state.get("scraping", False):
        st.info("# 🟠 Patience, je scrape... Consulte la sidebar pour suivre la progression.")
    elif df is not None:
        st.success(f"✅ Données chargées depuis 👉 `{output_file}`")
    else:
        st.info("# ℹ️ Il n'y a pas de résultat. Lance le scraper.")

    if st.session_state.get("last_output"):
        st.markdown(
            f"🗃️ Le dernier fichier utilisé est **`{st.session_state['last_output']}`**"
        )


# 2d onglet Les résultats
with tab_results:
    st.subheader("📊 Voici les résultats du scraping")

    if data and df is not None and not df.empty:
        st.success(f"✅ {len(df)} pages trouvées")

        # Statistiques globales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pages", len(df))
        with col2:
            total_paragraphes = int(df["Paragraphes"].sum())
            st.metric("Paragraphes", total_paragraphes)
        with col3:
            total_images = int(df["Images"].sum())
            st.metric("Images", total_images)
        with col4:
            total_liens = sum(len(item.get("liens_internes", [])) for item in data)
            st.metric("Liens internes", total_liens)

        st.markdown("## **🔎 Filtrer les pages**")

        colf1, colf2, colf3, colf4 = st.columns(4)

        with colf1:
            depth_filter = st.multiselect(
                "Profondeur",
                options=sorted(df["Profondeur"].unique()),
                default=sorted(df["Profondeur"].unique()),
            )

        with colf2:
            search_term = st.text_input("Recherche dans les titres")

        with colf3:
            min_len = st.number_input(
                "Longueur minimale du contenu",
                min_value=0,
                max_value=int(df["Longueur"].max()),
                value=0,
                step=100,
            )

        with colf4:
            min_imgs = st.number_input(
                "Nombre minimal d'images",
                min_value=0,
                max_value=int(df["Images"].max()),
                value=0,
                step=1,
            )

        # Application des filtres
        filtered_df = df[df["Profondeur"].isin(depth_filter)]
        filtered_df = filtered_df[filtered_df["Longueur"] >= min_len]
        filtered_df = filtered_df[filtered_df["Images"] >= min_imgs]

        if search_term:
            filtered_df = filtered_df[
                filtered_df["Titre"].str.contains(search_term, case=False, na=False)
            ]

        st.markdown("### 📄 **Tableau des pages scrapées**")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### 🔍 **Les détails de page**")

        titles = [item.get("titre") for item in data if item.get("titre")]
        selected_title = st.selectbox(
            "Choisis une page", options=titles
        )

        if selected_title:
            selected_item = next(
                (item for item in data if item.get("titre") == selected_title),
                None,
            )

            if selected_item:
                cold1, cold2 = st.columns([2, 1])

                with cold1:
                    st.markdown(
                        f"L'adresse est [{selected_item['url']}]({selected_item['url']})"
                    )

                    if selected_item.get("introduction"):
                        st.markdown("L'introduction est ")
                        st.write(selected_item["introduction"])

                    # Liens internes
                    if selected_item.get("liens_internes"):
                        st.markdown("Les liens internes (≤ 10) sont ")
                        for link in selected_item["liens_internes"][:10]:
                            st.markdown(f"- {link}")

                with cold2:
                    st.metric("La profondeur est ", selected_item.get("profondeur", 0))
                    st.metric(
                        "Le nombre de paragraphes est ",
                        selected_item.get("nombre_paragraphes", 0),
                    )
                    st.metric(
                        "Images",
                        selected_item.get("nombre_images", 0),
                    )

                    if selected_item.get("images"):
                        st.markdown("Aperçu jusqu'à 3 images")
                        for img in selected_item["images"][:3]:
                            try:
                                st.image(f"https:{img}", width=150)
                            except Exception:
                                st.text(img)

        # (Section d'export retirée de l'onglet : déplacée dans la sidebar)

    else:
        st.info("# ℹ️ Il n'y a pas de résultat. Tu peux lancer le scraper.")

# 3ème onglet Les graphiques
with tab_plots:
    st.subheader("📈 Les pages scrapées")

    if df is not None and not df.empty:
        colg1, colg2 = st.columns(2)

        with colg1:
            st.markdown("La répartition des pages par profondeur")
            depth_counts = df.groupby("Profondeur")["Titre"].count()
            st.bar_chart(depth_counts)

        with colg2:
            st.markdown("La relation longueur du contenu / nombre d'images")
            st.scatter_chart(df, x="Longueur", y="Images")

        st.markdown("La distribution du nombre de paragraphes")
        paragraphs_counts = df["Paragraphes"].value_counts().sort_index()
        st.bar_chart(paragraphs_counts)

        st.markdown(
            "Ces graphiques permettent de repérer rapidement les pages longues, riches en images ou particulièrement denses en texte."
        )
    else:
        st.info("# ℹ️ N'ayant pas de résultat, il n'y a pas de graphique.")

# 4ème onglet L'éthique & infos
with tab_ethics:
    st.subheader("⚖️ Éthique, droit, environnement et bonnes pratiques")

    st.markdown("### 📚 Le cadre de Wikipédia")
    st.markdown(
        "* Wikipedia impose des **conditions d’utilisation** et une **licence CC BY-SA**.\n"
        "* Ce projet est conçu pour un usage **pédagogique** et expérimental.\n"
        "* Toute réutilisation publique du contenu doit citer Wikipédia et respecter la licence."
    )

    st.markdown("### 🤖 Le scraping responsable")
    st.markdown(
        "* `ROBOTSTXT_OBEY=True` est activé dans le spider Scrapy.\n"
        "* Le délai entre requêtes (`DOWNLOAD_DELAY`) limite la charge envoyée au serveur.\n"
        "* Le nombre de requêtes simultanées (`CONCURRENT_REQUESTS`) doit rester raisonnable.\n"
        "* Évite d’augmenter profondeur + requêtes simultanées + délai très faible en même temps."
    )

    st.markdown("### 🔐 Les données personnelles (RGPD)")
    st.markdown(
        "* Les pages Wikipédia scrapées ici ne visent pas des **données à caractère personnel**.\n"
        "* Ce projet ne traite donc pas, en l’état, de données couvertes par le **RGPD**.\n"
        "* Si tu adaptes ce code pour d’autres sites / contenus, tu devras vérifier :\n"
        "  * la présence de données personnelles,\n"
        "  * la base légale de traitement,\n"
        "  * les droits des personnes (accès, suppression, etc.)."
    )

    st.markdown("### 🌍 L'impact environnemental")
    st.markdown(
        "* Chaque requête HTTP consomme des ressources côté client et serveur.\n"
        "* Des paramètres agressifs (profondeur élevée, nombreuses requêtes simultanées, délai faible) "
        "augmentent l’empreinte carbone.\n"
        "* Utilise ce scraper avec **modération** et préfère des expériences limitées dans le temps et en volume."
    )

    st.markdown("### 🧠 Le management et les bonnes pratiques")
    st.markdown(
        "* Définis des **politiques internes** pour le scraping dans un contexte pro (lignes directrices, limites, logs).\n"
        "* Documente :\n"
        "  * les paramètres utilisés,\n"
        "  * les cibles scrapées,\n"
        "  * les finalités (pourquoi on scrape),\n"
        "  * les risques et mesures de mitigation.\n"
        "* Ce type d’interface peut servir de **tableau de bord de gouvernance** du scraping."
    )

    st.markdown("___")
    st.markdown(
        "🐱 **FelisCrawler** | _Scrapy et Streamlit_ — C'est un projet pédagogique. Il n'est pas destiné à une exploitation massive."
    )

# Récupérer les données
st.sidebar.markdown(" ")
st.sidebar.markdown("___")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown("### 💾 Exporter")

if data is not None or (df is not None and not df.empty):
    _json_bytes = (json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8") if data is not None else b"")
    _json_name  = f"scraping_{time.strftime('%Y%m%d_%H%M%S')}.json"

    clicked_json = st.sidebar.download_button(
        label="📥 Récupérer le ficier JSON",
        data=_json_bytes,
        file_name=_json_name,
        mime="application/json",
        disabled=not (data is not None),
        key="dl_json_btn"
    )

    _csv_name_now = f"scraping_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    _csv_bytes    = (df.to_csv(index=False, encoding="utf-8-sig") if df is not None else "").encode("utf-8-sig") if df is not None else b""

    clicked_csv = st.sidebar.download_button(
        label="📥 Récupérer le fichier CSV",
        data=_csv_bytes,
        file_name=_csv_name_now,
        mime="text/csv",
        disabled=not (df is not None and not df.empty),
        key="dl_csv_btn"
    )

    if clicked_json:
        _open_download_modal(
            file_name=_json_name,
            kind="json",
            server_hint="Généré en mémoire. Il n'y a rien côté serveur."
        )
        st.rerun()

    if clicked_csv:
        possible_server_csv = Path(_csv_name(output_file))
        server_hint = str(possible_server_csv.resolve()) if possible_server_csv.exists() else "Généré en mémoire. Il n'y a rien côté serveur."
        _open_download_modal(
            file_name=_csv_name_now,
            kind="csv",
            server_hint=server_hint
        )
        st.rerun()
else:
    st.sidebar.info("Aucun résultat à exporter pour l’instant.")