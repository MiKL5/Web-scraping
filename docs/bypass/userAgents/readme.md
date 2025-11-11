# **Les User-Agents**<a href="../../../"><img align="right" src="../../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>
Les sites web utilisent les User-Agents pour identifier et bloquer les scrapers [1].  
Si un site web détecte un User-Agent inconnu ou suspect, il peut lui bloquer l'accès. Les scrapers qui utilisent le User-Agent par défaut d'une bibliothèque HTTP (requests, ...) sont facilement identifiables.

La technique la plus courante consiste à utiliser une liste de User-Agents valides et à les faire tourner aléatoirement à chaque requête [2] [3]. Cela permet de masquer l'identité du scraper et de le faire ressembler à un navigateur web normal [1] [4].

La rotation des User-Agents : [2] [4]
Maintenir une liste de User-Agents valides et réalistes [1] [3]. Il y a des listes de User-Agents valides en ligne.  
Choisir un User-Agent aléatoire à partir de la liste pour chaque requête [4].  
Mettre à jour régulièrement la liste de User-Agents pour éviter d'utiliser des User-Agents obsolètes [3].  
Exemple de code Python : L'exemple de code Python est un exemple classique de rotation des User-Agents et ne provient pas d'une source spécifique. Il est basé sur les meilleures pratiques courantes [2] [3].
```py
import requests
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def get_random_user_agent():
    return random.choice(user_agents)

url = 'https://www.example.com'
headers = {'User-Agent': get_random_user_agent()}
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
```
___
Références :
[1] https://www.scrapingbee.com/blog/best-anti-scraping-techniques/
[2] https://www.scraperapi.com/blog/how-to-bypass-anti-scraping-techniques/
[3] https://proxyscrape.com/blog/best-ways-to-bypass-anti-scraping-measures/
[4] https://www.geeksforgeeks.org/how-to-rotate-user-agents-while-web-scraping-in-python/