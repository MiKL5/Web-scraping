# **Les cookies et sessions**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Les cookies sont de petits fichiers de texte que les sites Web stockent sur l'ordinateur de l'utilisateur pour mémoriser des informations le concernant. Notamment des informations de connexion, des préférences 
linguistiques, des articles dans un panier d'achat, etc. [1] [2].

Les sessions sont des mécanismes côté serveur permettant de stocker des informations sur l'activité d'un utilisateur pendant qu'il navigue sur un site Web [2].  
Contrairement aux cookies, les données de session sont stockées sur le serveur[2].  
Un identifiant de session unique est généralement stocké dans un cookie sur l'ordinateur de l'utilisateur afin de le relier aux données de session sur le serveur [2].

Comment sont-ils utilisés pour lutter contre le scraping ?
Les sites web utilisent des cookies et des sessions pour suivre le comportement des utilisateurs et identifier les activités suspectes [1]. Le refus des cookies ou le lancement rapide de nombreuses sessions peut signaler une activité de bot [1].

Comment contourner l'anti-scraping basé sur les cookies et les sessions ?
Avec une gestion appropriée des cookies. Le scraper doit accepter, stocker et renvoyer les cookies au site web lors des requêtes suivantes [3] [4]. Des bibliothèques telles que `requests` en Python peuvent aider [4] [5].

Les sites web utilisent les cookies et les sessions pour suivre le comportement des utilisateurs et détecter les activités suspectes [5] [6]. Si un utilisateur ne semble pas accepter les cookies ou s'il initie un grand nombre de sessions en peu de temps, cela peut être un signe d'activité de bot [5].

Le scraper doit gèrer correctement les cookies et les sessions [6] [7].
<!-- Gestion des cookies : [7][8]
Activer la gestion des cookies dans votre scraper.
Accepter les cookies du site web [7].
Stocker les cookies et les renvoyer avec les requêtes suivantes [8] [9].
Rotation des cookies : Supprimer et recréer régulièrement de nouveaux cookies pour éviter d'être détecté.
Maintien des sessions : [6] [8]
Si le site web utilise des sessions, votre scraper doit maintenir une session active [6] [9].
Récupérer l'identifiant de session à partir du cookie [5] [7].
Inclure l'identifiant de session dans toutes les requêtes suivantes [7] [8].
Simulation du comportement humain :
Imitez le comportement d'un utilisateur réel en naviguant sur le site web, en cliquant sur des liens et en remplissant des formulaires avant de commencer à scraper [1] [4].
Cela permet d'établir une session "normale" avant de lancer l'extraction de données.
Exemple de code Python (avec requests): L'exemple de code Python est un exemple classique de gestion des cookies et des sessions et ne provient pas d'une source spécifique, mais il est basé sur les meilleures pratiques courantes [6] [8]. -->
```py
import requests

session = requests.Session()

# Simuler une visite initiale pour obtenir les cookies et l'ID de session
response = session.get('https://www.example.com')

# Afficher les cookies récupérés
print(session.cookies.get_dict())

# Effectuer des requêtes en utilisant la même session
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = session.get('https://www.example.com/page2', headers=headers)
print(response.status_code)
print(response.text)
```
___
Références :
[1] https://www.scrapingbee.com/blog/best-anti-scraping-techniques/
[2] https://www.scraperapi.com/blog/how-to-bypass-anti-scraping-techniques/
[3] https://proxyscrape.com/blog/best-ways-to-bypass-anti-scraping-measures/
[4] https://docs.python-requests.org/en/latest/user/quickstart/#cookies/
[5] https://realpython.com/python-requests/#handling-cookies-with-requests/
[6] https://www.geeksforgeeks.org/how-to-handle-cookies-in-python-using-requests-module/
[7] https://www.dataquest.io/blog/python-api-tutorial/
[8] https://www.crummy.com/software/BeautifulSoup/bs4/doc/#cookies
[9] https://stackoverflow.com/questions/3296286/how-to-handle-sessions-and-cookies-in-python-requests