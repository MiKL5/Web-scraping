# **FelisCrawler**<img align="right" src="../../assets/atomicWebScraping.png" alt="Web scraping" height="64px">
<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue?style=flat&logo=python&logoColor=FFD43B) 
![Scrapy](https://img.shields.io/badge/Scrapy-Web_Scraping-5E8862?style=flat&logo=scrapy&logoColor=white) 
![Streamlit](https://img.shields.io/badge/Streamlit-UI_Interactive-FF4B4B?style=flat&logo=streamlit&logoColor=white) 
![Pandas](https://img.shields.io/badge/pandas-Data_Processing-150458?style=flat&logo=pandas&logoColor=white) 
![JSON](https://img.shields.io/badge/JSON-Export-000000?style=flat&logo=json&logoColor=white)

</div>


"**_FelisCrawler_**" est une plateforme interactive et éthique. Elle permet de
scraper tous les articles Wikipédia (en français) liés aux chats et félins. Visualiser et analyser interactivement le contenu structuré issu du scraping. Et de piloter le scraping et exporter les données simplement.
---
## **Les principaux composants du projet sont**
* Un spider Scrapy avancé multi règles, conçu pour explorer en profondeur les liens encyclopédiques autour des chats sur Wikipédia.
* L'interface utilisateur graphique avec Streamlit. Elle centralise la configuration, le lancement du scraping, la visualisation des résultats (statistiques, tableaux, graphiques) et la documentation éthique.
## **Les principales fonctionnalités sont**
* Un scraping exhaustif de Wikipédia sur la thématique féline (avec le suivi intelligent des liens pertinents et filtrage)
* Le contrôle total des paramètres
  * La profondeur de crawl
  * Le délai minimum entre requêtes (pour le respect des serveurs)
  * Le nombre de requêtes simultanées
  * Le nom du fichier de sortie.

* La visualisation instantanée des résultats du scraping
  * La quantité de pages, paragraphes, images, liens internes
  * Le tableau filtrable des articles
  * Les fiches détaillées par article (titre, intro, liens internes, images) ;
  * Les graphiques interactifs
    * La répartition par profondeur, 
    * La distribution des paragraphes,
    * La relation longueur/nombre d’images.

* Le téléchargement à la demande des résultats en JSON
* Une documentation sur l’éthique, l’impact environnemental du scraping, le RGPD et les bonnes pratiques
## **Organisation des fichiers**
**Un CrawlSpider scrutant fr.wikipedia.org/wiki/Chat, en suivant des règles d’exploration**
* Suivre des URL pertinentes
* Exclure les espaces non encyclopédiques
* Extractraire à chaque page : le titre, l'introduction, le nombre paragraphes, la longueur texte, les liens internes, les images filtrées et la profondeur.

**L'application Streamlit permet**
* La configuration intuitive par la sidebar
* Le lancement du scraping en un clic (génère un sous-processus Scrapy configurable)
* La visualisation, le filtrage et l'export interactifs des résultats
* Les statistiques et graphiques
* Une rubrique sur l’éthique, l’environnement, le droit et la gouvernance du scraping.

## **L'utiliser**
Il faut Python 3.9 ou plus récent. Scrapy, Streamlit et Pandas.
### **Pour installer les dépendances**
```py
pip install scrapy streamlit pandas
```
Démarrage de l’application :
```py
streamlit run app.py
```
### **Depuis l’interface ouverte dans un navigateur**, vous pouvez
* Paramétrer les options de scraping dans la barre latérale
* Lancer le scraping
* Explorer les données collectées dans les onglets
* Filtrer, rechercher, et exporter les résultats au format JSON
## **Les spécificités du spider**
* Configuration fine par attributs Scrapy (profondeur, délais, concurrent, User-Agent)
* Respect du fichier '_robots.txt_'
* Extraction robuste des titres, introduction et paragraphes
* Limitation intelligente des liens internes et images extraites pour éviter les débordements
* Compatible avec tous les formats d’export supportés (FEEDS Scrapy)
## Visualiser et analyser
Il y a un tableau filtrable pour sélectionner les pages par profondeur, nombre d’images, longueur, titre. Les détails de chaque page.  
Des graphiques concerant
* La répartition des pages par profondeur de crawl
* La relation longueur de texte/nombre d’images (scatter)
* La distribution du nombre de paragraphes par page
## **Éthique, gouvernance et bonnes pratiques**
Le scraping limité à un usage expérimental et pédagogique. Il respect explicitement les règles Wikipédia (licence CC BY-SA, attribution requise). Il n'y a pas de collecte de données personnelles dans le périmètre du projet. 
Le respect de l’environnement est possible par la modulation des paramètres pour minimiser l’impact carbone et éviter de surcharger le serveur.

![screenshot](assets/screenshot.png)
## **Références et documentation**
[Scrapy — Spiders](https://docs.scrapy.org/en/latest/topics/spiders.html)  
[Scrapy — Sélecteurs XPath](https://docs.scrapy.org/en/latest/topics/selectors.html)  
[Scrapy — Paramètres de pipeline et exports](https://docs.scrapy.org/en/latest/topics/feed-exports.html)  
[Documentation de Streamlit](https://docs.streamlit.io/)  
[Licences et conditions d’utilisation de Wikipédia](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Droit_d%27auteur)  
[Récapitulatif du RGPD](https://www.cnil.fr/fr/rgpd-par-ou-commencer)
___
"**_FelisCrawler_**" est conçu pour illustrer l’intégration de technologies de scraping et d’interface utilisateur dans un contexte pédagogique et gouverné.