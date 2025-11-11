# **Délais et limitations de requêtes**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Envoyer des requêtes trop rapidement peut indiquer une activité de bot et entraîner un blocage [2] [3].

Implémenter des délais aléatoires entre les requêtes [2] [3].  
Utiliser la fonction `sleep()` en Python pour introduire des pauses [2].  
Éviter d'envoyer des requêtes à des intervalles réguliers, car cela peut également trahir [2].
___
Références :
[1] https://www.scrapingbee.com/blog/best-anti-scraping-techniques/
[2] https://www.scraperapi.com/blog/how-to-bypass-anti-scraping-techniques/
[3] https://proxyscrape.com/blog/best-ways-to-bypass-anti-scraping-measures/