import requests
import random

urls = [
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Safari.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Firefox.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Chrome.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Opera.txt"
]

# Liste initiale de user-agents de base pour commencer
initial_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

ua = []
for url in urls:
    # Choisir un user-agent aléatoire pour cette requête
    headers = {
        'User-Agent': random.choice(initial_user_agents)
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        lines = response.text.split("\n")
        # Ajouter à la liste uniquement à partir du 3ᵉ élément
        if len(lines) > 2:
            ua.extend(lines[2:len(lines)-1])
    else:
        print(f"Erreur lors du chargement de {url}")

# print(f"Total de user-agents récupérés : {len(ua)}")