# **Le navigateur sans tête**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Le "headless browser" est un navigateur web sans interface graphique. Contrairement aux navigateurs classiques comme Chrome ou Firefox, il exécute les mêmes tâches (chargement de pages, exécution de JavaScript, etc.) mais sans afficher visuellement les pages à l'écran.
---
C'est particulièrement utiles en web scraping.
* Pour rendre des pages dynamiques  
Charger et d'exécuter le contenu généré par JavaScript, ce qui est souvent nécessaire pour extraire des données de sites modernes.
* Simuler un comportement humain  
Effectuer des actions telles que le défilement de page, les clics ou les mouvements de le souris, pour contourner certaines mesures anti-scraping.
* Automatiser les tâches  
Telles que la navigation et l'extraction de données sans interface utilisateur. ​

Quelques headless browsers :
* Puppeteer 👉 Une bibliothèque JavaScript contrôlant Chrome ou Chromium en mode sans tête. ​
* Selenium 👉 Un outil automatisant les navigateurs, y compris en mode sans tête. ​

Ces navigateurs sont très puissants pour le scraping de sites complexes. Nonobstant, leur utilisation doit respecter les règles d'éthique et les conditions d'utilisation des sites web.
___
⚠️ Il est aussi important de noter que les headless browsers peuvent être plus gourmands en ressources que les requêtes HTTP classiques, ce qui peut impacter les performances du scraping à grande échelle.