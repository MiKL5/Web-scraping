# Web Scraping de livres sur books.toscrape.com avec Scrapy<a href="../../"><img align="right" src="../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue?style=flat&logo=python&logoColor=FFD43B) 
![Scrapy](https://img.shields.io/badge/Scrapy-Web_Scraping-5E8862?style=flat&logo=scrapy&logoColor=white)

</div><hr>

Il s'agit d'un spider Scrapy visant à extraire automatiquement des informations bibliographiques (titre, prix, image, ...) depuis le site de démonstration [books.toscrape.com](https://books.toscrape.com/).  
Le but est de collecter et structurer les données pour chaque livre d’une page principale.
---
## **Le fonctionnement avec le langage de requête "xpath"**
1. **Collecte des blocs de livres** avec la requête XPath sur la classe de chaque livre (`//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]`).
2. **Extraction des informations** pour chaque livre :
   - Titre (`.//h3/a/@title`)
   - Prix (`.//p[@class="price_color"]/text()`)
   - Source de l’image (`.//img/@src`)
3. **Astuces XPath** documentées dans le fichier pour manipuler descendants, attributs, siblings, etc.
### **Notes**
- La syntaxe `.//` dans les XPaths cible des descendants à partir d’un noeud local (ex: un bloc livre).
- Les méthodes `.get()`, `.getall()`, `.extract()`, etc., selon le nombre de valeurs attendues.
- Pour extraire « le premier » élément, utiliser `[0]` ou `.get()` ; pour tous, `.getall()`.
### **Références**
- [Documentation officielle Scrapy](https://docs.scrapy.org/)
- [XPath Cheatsheet](https://devhints.io/xpath)
___
## **Le fonctionnement avec le "CSS"**
- Récupération des prix des livres présents avec le sélecteur CSS `p.price_color`.
- Envoi des résultats sous forme de dictionnaire contenant le prix extrait.
### **Notes**
- Le sélecteur CSS `p.price_color::text` cible le texte du prix pour chaque livre.
- Le spider explore uniquement la page d’accueil dans cette version.
### **Références**
- [Documentation officielle Scrapy](https://docs.scrapy.org/)
- [CSS Selectors Reference](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_Selectors)
___
## **Exporter les données**
* En "json" ➜ `scrapy runspider b2s -o data.json`
  * Faire '`ctrl` + `A` + `K` + `F`' pour l'indentation.
* En "csv"  ➜ `scrapy runspider b2s -o data.csv`

Dans "settings", '`FEED_EXPORT_ENCODING = 'utf-8'`' permet de bien afficher les caractères.  
