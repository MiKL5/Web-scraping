# **Les mesures anti-scrawling**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Les sites web mettent en place diverses mesures pour détecter et bloquer les activités de scraping automatisé. 
1. **L'analyse du comportement de l'utilisateur (UBA)**
* Il s'agit du suivi et l'analyse du comportement des utilisateurs sur un site web pour détecter les anomalies suggérant une activité de bot.
* Pour fonctionner ces systèmes UBA étudient la manière dont les utilisateurs interagissent avec le site, en surveillant des actions telles que les mouvements de la souris, les clics et la vitesse de navigation. Les bots ont souvent des schémas d'interaction non naturels, les trahissant.
2. **Le CAPTCHA et les tests de sécurité**
* utiliser les tests CAPTCHA (_Completely Automated Public Turing test to tell Computers and Humans Apart_) permet la distinction des humains et bots.
* Les CAPTCHA présentent des questions visuelles ou audio que seuls les humains peuvent résoudre facilement. Les bots ont du mal à interpréter ces tests, et ce font bloquer.
3. **La limitation de la fréquence des requêtes (Rate Limiting)**
Réstrindre le nombre de requêtes qu'une adresse IP ou d'un agent utilisateur sur un site web pendant un délai.
* La limitation de débit empêche les scrapers d'envoyer un nombre excessif de requêtes en peu de temps, évitant la surcharge des serveurs.
4. **Le blocage d'adresses IP**
* L'identifier et bloquer les IP associées à une activité de scraping malveillante.
* Les sites web surveillent les adresses IP qui envoient un nombre anormalement élevé de requêtes ou présentant un comportement suspect. Ces adresses IP sont ensuite bloquées.
5. **Les agents utilisateurs**
* L'analyse de l'en-tête "User-Agent" des requêtes HTTP pour identifier les scrapers.
* Les sites web peuvent bloquer les agents utilisateurs par défaut ou non standard, car ils peuvent indiquer qu'il s'agit d'un bot.
6. **Le fichier robots.txt**
Utiliser le fichier "robots.txt" pour indiquer aux robots d'exploration quelles parties d'un site web ne doivent pas être traitées.
* Ce dernier contient des directives que les robots d'exploration doivent suivre. Bien que ce fichier ne puisse pas empêcher complètement le scraping, il peut dissuader les robots respectueux de suivre les zones interdites.
7. **Les honeypots**
* Ajouter des liens ou éléments cachés dans le code HTML invisibles des utilisateurs humains, que les bots peuvent suivre.
* Si un bot accède à un honeypot, il est immédiatement bloqué.
8. **Surveiller et détecter les bots**
* Utiliser des solutions de détection de bots pour identifier et bloquer les bots malveillants en temps réel.
* Ces solutions analysent le trafic et distinguent les utilisateurs humains des programmes automatisés.  
Elles utilisent diverses techniques, telles que l'analyse comportementale et la réputation de l'IP, pour détecter les bots.
9. **L'obfuscation des données**
* Rendre les données difficiles à comprendre en changeant la forme sur le site web compliquant leur extraction par les scrapers.
* Cette technique consiste à modifier la structure HTML ou à utiliser des techniques de codage pour rendre les données moins accessibles aux scrapers.
10. **L'authentification multifacteur (MFA)**
* Exiger plusieurs méthodes d'authentification pour accéder au site web.
* Bien que principalement utilisée pour la sécurité des comptes utilisateurs, MFA peut également dissuader certains types de bots en ajoutant une couche de complexité à l'accès.
11. **Le filigrane numérique**
* Intégrer des filigranes numériques dans le contenu pour suivre et identifier les sources de scraping non autorisé.
* Ils permettent de surveiller l'utilisation du contenu et de prendre des mesures contre les scrapers qui utilisent le contenu sans autorisation.
12. **L'analyse du trafic**
* Analyser le trafic web pour identifier les schémas anormaux ou les pics de trafic provenant de certaines sources.
* Une augmentation soudaine du trafic provenant de certaines sources ou pays peut indiquer une activité de scraping.
13. **Les conditions d'utilisation**
* Indiquer clairement dans les conditions d'utilisation du site web que le scraping est interdit.
* Bien que cela ne puisse pas empêcher techniquement le scraping, cela donne une base juridique pour prendre des mesures contre les scrapers.
14. **Surveiller les nouveaux comptes utilisateurs**
Surveiller les nouveaux comptes utilisateurs ou ceux existants avec des niveaux élevés d'activité et sans achats.
* Cele aide à identifier les comptes potentiellement utilisés pour le scraping.
15. **Les redirections**
* Rediriger les requêtes de bots vers la page d'accueil du site ou vers une autre destination.
* Cette technique perturbe le processus de scraping et peut empêcher les bots d'accéder au contenu souhaité.
16. **Les résultats vides ou factices**
* Le site web répond "normalement", mais prétend ne trouver aucun résultat ou renvoie des données totalement fausses.
* Cette technique complique pour les scrapers le fait de déterminer la véracité des données. Nécessitant des tests manuels approfondis.
___
⚠️ Il y a constament le jeu du chat et de la souris entre les scrapers et les mesures anti-scraping.  
Les scrapers développent constamment de nouvelles techniques pour contourner ces mesures.  
Les défenses des sites web doivent dovnent êtres régulièrement mise à jour pour rester protégés.