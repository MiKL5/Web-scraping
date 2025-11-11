# **La rotation d'adresse IP**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Lors du web scraping, il est courant de rencontrer des restrictions basées sur l'adresse IP, telles que le blocage ou la limitation du nombre de requêtes.  
Pour contourner ces restrictions, la rotation d'adresse IP est une technique efficace qui consiste à changer régulièrement l'adresse IP utilisée pour envoyer des requêtes. ​
Voici quelques méthodes courantes pour mettre en œuvre la rotation d'adresse IP :

En pratique, la rotation des adresses IP fonctionne en utilisant un pool de serveurs proxy [1]. Voici les étapes clés :
1. L'obtention d'un pool d'adresses IP :
    * Il faut obtenir une liste d'adresses IP à utiliser. Ces adresses proviennent généralement de services de proxy.
    * Les services de proxy peuvent fournir des adresses IP de centres de données, des adresses IP résidentielles ou des adresses IP mobiles. Les adresses IP résidentielles sont souvent préférées car elles sont moins susceptibles d'être bloquées, car elles sont associées à de véritables utilisateurs.
2. Configurer un scraper :
    * pour utiliser ce pool d'adresses IP au lieu d'utiliser directement mon adresse IP.
    * Il faut donc modifier les paramètres de requête HTTP pour spécifier l'adresse IP du proxy à utiliser pour chaque requête.
3. La rotation des adresses IP :
    * Ça consiste à changer l'adresse IP utilisée pour chaque requête ou après un certain nombre de requêtes.
    * Cela peut être fait de plusieurs manières :
        * Par rotation programmée 👉 elle change à des intervalles prédéterminés.
        * La rotation basée sur les requêtes 👉 elle change après un nombre de requêtes.
        * La sélection aléatoire 👉 une adresse du pool est attribuée aléatoirement à chaque nouvelle connexion.
4. La gestion des sessions :
    * Pour certains sites web, il est important de maintenir une session (pour simuler un utilisateur connecté, ...). Dans ce cas, il est impératif de s'assurer que toutes les requêtes d'une même session utilisent la même adresse IP.
5. L'automatisation :
    * La rotation des adresses IP est généralement automatisée par des bibliothèques de programmation ou de services spécialisés.
    * Par exemple, en Python, on peut utiliser la bibliothèque '`requests`' pour envoyer des requêtes via des proxys et faire tourner les adresses IP par une boucle.

Ainsi, les requêtes répartiessur plusieurs adresses, il est plus difficile de détecter et de bloquer le scraper. Cela permet de contourner les limitations de débit et d'éviter les blocages d'IP, assurant un accès continu aux données.