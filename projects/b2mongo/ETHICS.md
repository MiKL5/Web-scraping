# ⚖️ Éthique et bonnes pratiques - Web Scraping
Guide d'éthique et de bonnes pratiques pour un scraping responsable et légal.
## **🎯 Les principes fondamentaux**
### 1. Le respect avant tout
Le web scraping n'est **pas** un droit acquis. C'est un privilège qui s'accompagne de responsabilités :
* ✅ **Respecter** les propriétaires des sites web
* ✅ **Minimiser** l'impact sur les serveurs
* ✅ **Se conformer** aux lois et réglementations
* ✅ **Protéger** les données personnelles
* ✅ **Être transparent** sur vos intentions
### 2. La règle d'or
> **"Scrapez les autres sites comme vous aimeriez que votre propre site soit scrapé."**

Si une action pourrait nuire, ralentir ou coûter de l'argent au propriétaire du site, ne la faites pas.
## ⚖️ Aspects légaux
### Cadre juridique général
**⚠️ AVERTISSEMENT** : Ce projet est un **outil éducatif** et ne constitue pas un conseil juridique. Consultez toujours un avocat pour des questions légales spécifiques.
### 1. Conditions d'utilisation (ToS)
```
✅ Toujours lire les Terms of Service du site
✅ Respecter les interdictions explicites
❌ Ne jamais contourner les protections techniques
❌ Ne pas scraper si c'est explicitement interdit
```
**Example** :
```
Site A : "No automated scraping allowed" → ❌ Ne pas scraper
Site B : Pas de mention → ⚠️ Procéder avec prudence
Site C : "API available for data access" → ✅ Utiliser l'API
```
### 2. Robots.txt
**Le fichier `robots.txt` est une convention**, pas une loi, mais il exprime clairement les souhaits du propriétaire.
```python
# Ce projet RESPECTE robots.txt par défaut
ROBOTSTXT_OBEY = True  # ← Ne JAMAIS changer en False sans raison valable
```
**Vérifier robots.txt** :
```bash
curl https://example.com/robots.txt

# Exemple books.toscrape.com :
# User-agent: *
# Disallow:
# → Pas de restriction, scraping autorisé
```
### 3. Législation par région
Région | Loi applicable | Points clés
---|---|---
**UE** | RGPD | Protection données personnelles
**USA** | CFAA, DMCA | Accès non autorisé interdit
**France** | LPD, Code pénal | Art. 323-1 (accès frauduleux)
**UK** | Computer Misuse Act | Accès non autorisé puni

**Règle générale** : Le scraping de **données publiques** est généralement légal, mais :
* ❌ **Jamais** de données personnelles sans consentement
* ❌ **Jamais** de contenu protégé par copyright
* ❌ **Jamais** de contournement d'authentification
### 4. Précédents juridiques notables
**Cas hiQ Labs vs LinkedIn (2022)** :
* ✅ Scraping de données **publiques** : Légal
* ❌ Scraping après interdiction explicite : Risqué
**Règle pratique** :
```
Données publiques + robots.txt OK + pas de ToS violés = Probablement OK
Données privées OU authentification requise = NE PAS SCRAPER
```
## **🔧 Respect technique**
### 1. Rate limiting (limitation de débit)
**Pourquoi c'est important** :
* Éviter la surcharge des serveurs
* Ne pas impacter les utilisateurs légitimes
* Ne pas être banni
**Implémentation dans ce projet** :
```python
# settings.py
DOWNLOAD_DELAY = 0.5                    # 500ms entre requêtes
CONCURRENT_REQUESTS_PER_DOMAIN = 2      # Max 2 requêtes simultanées
CONCURRENT_REQUESTS = 16                # Global limité

# ❌ MAUVAIS EXEMPLE (ne pas faire)
DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS_PER_DOMAIN = 50
```
**Calcul d'impact** :
```
Paramètres actuels :
- 2 requêtes/seconde max par domaine
- 0.5s délai entre requêtes

Impact : ~120 requêtes/minute
→ Très raisonnable pour un site de test

⚠️ Sur un site de production :
- Augmenter DOWNLOAD_DELAY à 1-2 secondes
- Scraper pendant les heures creuses
```
### 2. User-Agent honnête
```python
# BON : User-Agent identifiable
USER_AGENT = "Mozilla/5.0 (Educational Scraper; +http://myproject.com/bot)"

# ACCEPTABLE : User-Agent navigateur standard
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# MAUVAIS : Se faire passer pour un utilisateur légitime systématiquement
USER_AGENT = "GoogleBot/2.1"  # Usurpation d'identité
```
### 3. Caching et déduplication
```python
# Ne pas re-télécharger les mêmes données
# MongoDB upsert évite les doublons
db.books.update_one(
    {'upc': item['upc']},
    {'$set': item_dict},
    upsert=True  # ← Mise à jour au lieu de duplication
)

# Cache HTTP activé
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1 heure
```
### 4. Gestion des erreurs
```python
# Retry intelligent (ne pas marteler le serveur)
RETRY_ENABLED = True
RETRY_TIMES = 3                        # Seulement 3 tentatives
RETRY_HTTP_CODES = [500, 502, 503]    # Seulement erreurs serveur

# Backoff exponentiel (temps entre retries augmente)
RETRY_BACKOFF = 2  # 1s, 2s, 4s, ...
```
## 🎓 Cas d'usage de ce projet
### books.toscrape.com : Un cas particulier
**Ce site est explicitement conçu pour l'apprentissage du scraping.**
```
✅ Objectif : Formation et tests
✅ robots.txt : Pas de restriction
✅ ToS : Pas de conditions interdisant le scraping
✅ Propriétaire : Consent explicite au scraping éducatif
✅ Données : Fictives (pas de vraies personnes/entreprises)
```
**C'est pourquoi ce projet est éthique** :
1. Site de démonstration (pas de production)
2. Données fictives (pas de PII)
3. Impact minimal (serveur prévu pour ça)
4. Objectif pédagogique clair
### ⚠️ NE PAS UTILISER CE CODE SUR :
Site type | Raison | Alternative
---|---|---
E-commerce réel | Impact business, ToS | Utiliser leur API
Réseaux sociaux | RGPD, ToS strict | API officielle
Sites d'actualités | Copyright | Flux RSS
Sites gouvernementaux | Données sensibles | Open Data portals
Sites protégés par login | Violation ToS | Demander accès API
## ✅ Bonnes pratiques
### 1. Avant de commencer
```
□ Lire les ToS du site
□ Vérifier robots.txt
□ Chercher une API officielle (préférable au scraping)
□ Évaluer l'impact potentiel
□ Documenter l'objectif du scraping
□ Contacter le propriétaire si doute (meilleure pratique)
```
### 2. Pendant le scraping
```python
# Identifier clairement votre bot
USER_AGENT = "MyResearchBot/1.0 (+mailto:contact@example.com)"

# Limiter la charge
DOWNLOAD_DELAY = 1  # Au moins 1 seconde

# Respecter les heures de faible trafic
# Scraper la nuit si possible

# Logger toutes les actions
LOG_LEVEL = 'INFO'
LOG_FILE = 'scraping.log'

# Monitorer l'impact
stats = crawler.stats.get_stats()
```
### 3. Après le scraping
```
□ Nettoyer les données (supprimer PII si présentes par erreur)
□ Ne pas publier de données sensibles
□ Respecter le copyright du contenu
□ Documenter la source des données
□ Mettre à jour régulièrement (pas scraper en continu)
```
### 4. Stockage et utilisation des données
```python
# BON : Données anonymisées et agrégées
stats = {
    'avg_price_by_category': {...},
    'total_books': 1000,
    'top_rated_categories': [...]
}

# MAUVAIS : Publication de données complètes
# Ne PAS publier dumps complets de bases de données scrapées
```
## **🚫 Que faire / Ne pas faire**
### ✅ À FAIRE
Action | Raison
---|---
Lire robots.txt | Respect des règles
Utiliser des délais | Ne pas surcharger
S'identifier clairement | Transparence
Utiliser l'API si disponible | Méthode privilégiée
Scraper données publiques uniquement | Légalité
Respecter le copyright | Loi
Monitorer l'impact | Responsabilité 
Cacher les requêtes | Efficacité 
### ❌ À NE PAS FAIRE
Action | Raison
---|---
Ignorer robots.txt | Irrespect flagrant
Faire du scraping agressif | Surcharge serveur
Usurper un User-Agent | Malhonnêteté
Scraper des données privées | Illégal (RGPD)
Contourner des protections | Potentiellement illégal
Revendre les données | Copyright, éthique
Scraper en continu 24/7 | Abus de ressources
Publier les données brutes | Respect propriété intellectuelle
___
## **🎯 Checklist éthique**
Avant de lancer un scraping, posez-vous ces questions :
### Questions légales
- [ ] Ai-je lu les ToS du site ?
- [ ] Le robots.txt autorise-t-il le scraping ?
- [ ] Existe-t-il une API officielle ?
- [ ] Vais-je scraper des données personnelles ?
- [ ] Le contenu est-il protégé par copyright ?
### Questions techniques
- [ ] Mes paramètres sont-ils respectueux ? (délais, concurrence)
- [ ] Mon User-Agent est-il honnête ?
- [ ] Ai-je un système de retry raisonnable ?
- [ ] Vais-je cacher les requêtes ?
- [ ] Puis-je scraper en heures creuses ?
### Questions éthiques
- [ ] Mon scraping pourrait-il nuire au site ?
- [ ] Puis-je justifier mon objectif ?
- [ ] Les données seront-elles utilisées à bon escient ?
- [ ] Suis-je transparent sur mon identité ?
- [ ] Ai-je contacté le propriétaire si nécessaire ?

**Si vous répondez "non" ou "je ne sais pas" à plusieurs questions → NE PAS SCRAPER.**
___
## **📚 Ressources supplémentaires**
### **Lectures recommandées**
* **RGPD** : https://gdpr.eu/
* **robots.txt RFC** : https://www.rfc-editor.org/rfc/rfc9309
* **Web Scraping Ethics** : https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01
* **Legal aspects** : https://benbernardblog.com/web-scraping-and-crawling-are-perfectly-legal-right/
### **Alternatives au scraping**
1. **APIs officielles** : Toujours privilégier
2. **Open Data** : Données gouvernementales ouvertes
3. **RSS/Atom feeds** : Pour les actualités
4. **Web Archives** : Archive.org, Common Crawl
5. **Datasets publics** : Kaggle, UCI ML Repository
___
## **🔐 Gestion des données personnelles (RGPD)**
### **Qu'est-ce qu'une donnée personnelle ?**
Toute information permettant d'identifier une personne :
* Nom, prénom, email
* Adresse IP, cookies
* Numéro de téléphone
* Photo, voix
* Données de localisation
### **Obligations RGPD**
Si vous scrapez des données personnelles :
```
✅ Base légale valide (consentement, intérêt légitime, etc.)
✅ Information transparente des personnes
✅ Droit d'accès, rectification, suppression
✅ Sécurisation des données
✅ Durée de conservation limitée
✅ Pas de transfert hors UE sans garanties
```
**Conseil** : **Évitez complètement de scraper des données personnelles** si possible.
___
## **🌟 En résumé**
### **Les 3 piliers du scraping éthique**
1. **LÉGALITÉ** : Respecter les lois et ToS
2. **RESPECT** : Ne pas nuire au site ou aux utilisateurs
3. **TRANSPARENCE** : Être honnête sur qui vous êtes et ce que vous faites
<!-- ### **Le test du journal**
> **"Serais-je à l'aise si mes pratiques de scraping faisaient la Une d'un journal ?"**

Si la réponse est non, reconsidérez votre approche. -->
<!-- ___
## **📞 Contact et signalement**
Si vous constatez une utilisation abusive de ce projet ou avez des préoccupations éthiques :
1. Ouvrir une issue GitHub avec le tag `ethics`
2. Contacter directement le propriétaire du projet
3. Signaler aux autorités compétentes si nécessaire (CNIL en France) -->
___
**Rappel final** : Ce projet est un outil **éducatif** pour apprendre Scrapy et MongoDB sur un site de **démonstration**. L'utilisation sur des sites réels nécessite une analyse éthique et légale approfondie au cas par cas.