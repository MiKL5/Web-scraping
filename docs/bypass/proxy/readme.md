# **Les serveurs proxy**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Les sites web peuvent identifier les scrapers en analysant l'en-tête "User-Agent" des requêtes HTTP [1] [2]. Un agent utilisateur par défaut ou un agent utilisateur non standard peut signaler qu'il s'agit d'un bot [2].

Maintenir une liste d'agents utilisateurs courants (ceux de Chrome, Firefox, Safari) et les faire tourner aléatoirement à chaque requête [1] [2]. Permettant de masquer le scraper en le faisant ressembler à un navigateur web normal [2].
___
Références :
[1] https://www.scrapingbee.com/blog/best-anti-scraping-techniques/
[2] https://www.scraperapi.com/blog/how-to-bypass-anti-scraping-techniques/