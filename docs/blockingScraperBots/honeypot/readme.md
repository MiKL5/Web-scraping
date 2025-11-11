# **L'honeypot**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Un honeypot est une technique utilisée par les sites web pour détecter et bloquer les bots ou scrapers.  
Il s'agit d'éléments cachés dans le code HTML, comme des liens ou des champs invisibles, qui ne sont pas visibles pour les utilisateurs humains mais que les bots peuvent détecter et suivre par erreur.

Comment il fonctionne ?
Souvent marqué avec des styles CSS tels que `display: none` ou `visibility: hidden`, ce qui les rend invisibles pour les utilisateurs humains.  
Si un bot interagit avec ces éléments cachés, cela signale au site web qu'il s'agit d'une activité automatisée, et entraîner le blocage.

Quelle s solution s pour les éviter ?
Inspecter le code source HTML des pages web et identifier les éléments cachés ou suspects.  
Configurer le scraper pour qu'il ignore les éléments marqués comme invisibles ou inutiles (e.g. certains styles CSS). ​

Ce ne sont qu'une des nombreuses mesures anti-scraping pour protéger les données du web contre l'extraction non autorisée.