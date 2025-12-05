# **Bypass - Contournement Anti-Bot**<a href="../../"><img align="right" src="../../assets/atomicWebScraping.png" alt="Web scraping" height="64px"></a>

<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue?style=flat&logo=python&logoColor=FFD43B) 
![Scrapy](https://img.shields.io/badge/Scrapy-2.13.4-5E8862?style=flat&logo=scrapy&logoColor=white) 
![Cloudflare](https://img.shields.io/badge/Cloudflare-Bypass-EA580C?style=flat&logo=cloudflare&logoColor=white) 
![curl_cffi](https://img.shields.io/badge/curl_cffi-TLS_Fingerprint-059669?style=flat&logo=curl&logoColor=white) 
![Selenium](https://img.shields.io/badge/Selenium-Stealth-43B02A?style=flat&logo=selenium&logoColor=white) 
![Playwright](https://img.shields.io/badge/Playwright-Anti_Detect-0EA5E9?style=flat&logo=playwright&logoColor=white)
![User Agents](https://img.shields.io/badge/User_Agents-4531+-8B5CF6?style=flat&logo=internetexplorer&logoColor=white)

</div>

<hr>

**Bypass** est un framework Scrapy conçu pour contourner les protections anti-scraping avec des techniques de stealth scraping, rotation dynamique de User-Agents, TLS fingerprinting et simulation de comportement humain.
---
## ✨ **Les fonctionnalités**
### 🔄 **Rotation intelligente de User-Agents**
- **4531+ User-Agents** chargés dynamiquement depuis GitHub
- Rotation automatique à **chaque requête**
- Support de Safari, Firefox, Chrome et Opera
- Chargement avec rotation (chaque liste est téléchargée avec un UA différent)
### 🛡️ **Protection anti-détection**
- Middleware de rotation automatique des User-Agents
- Support du TLS fingerprinting avec `curl_cffi`
- Headers HTTP réalistes
- Gestion des cookies intelligente
### 🎯 **Performance optimisée**
- Requêtes concurrentes configurables
- Système de retry intelligent
- Cache HTTP optionnel
- Timeout configurable
### 📊 **Monitoring et logging**
- Logs détaillés des User-Agents utilisés
- Statistiques de scraping
- Support Telnet pour monitoring en temps réel
## 🏗️ **L'architecture du projet**
```
bypass/
├── __init__.py                 # Initialisation du package
├── settings.py                 # Configuration principale + chargement User-Agents
├── middlewares.py              # Middlewares personnalisés
├── items.py                    # Définition des items Scrapy
├── pipelines.py                # Pipelines de traitement
├── spiders/                    # Dossier des spiders
│   ├── __init__.py
│   ├── example_spider.py       # Spider d'exemple
│   └── ...                     # Vos spiders personnalisés
├── scrapy.cfg                  # Configuration Scrapy
└── README.md                   # Documentation
```
### 📦 **Les principaux composants**
#### `settings.py`
Configuration centrale du projet incluant :
* Chargement dynamique des User-Agents depuis 4 sources GitHub
* Configuration Scrapy (delays, concurrency, retries)
* Fonction `get_random_user_agent()` exportable
#### `middlewares.py`
Deux middlewares personnalisés :
* **`RandomUserAgentMiddleware`** : Change le User-Agent à chaque requête
* **`BypassSpiderMiddleware`** : Middleware Spider optionnel
#### `spiders/`
Contient tous vos spiders de scraping. Chaque spider hérite de `scrapy.Spider` et utilise automatiquement la rotation de User-Agents.
## 🔐 **Les techniques de contournement**
### 1. **Rotation de User-Agents**
```python
# Chargement depuis GitHub avec rotation
urls = [
    "Safari.txt",    # 596 User-Agents
    "Firefox.txt",   # 2104 User-Agents
    "Chrome.txt",    # 852 User-Agents
    "Opera.txt"      # 992 User-Agents
]
# Total : 4531 User-Agents uniques
```
**Fonctionnement** :
1. Chaque liste est téléchargée avec un User-Agent différent
2. Les User-Agents sont stockés dans un pool global
3. À chaque requête, un UA aléatoire est sélectionné
4. Évite la détection par patterns répétitifs
### 2. **TLS Fingerprinting (curl_cffi)**
```python
# Imitation de navigateurs réels au niveau TLS
impersonate = "chrome110"  # ou firefox, safari, edge
```
### 3. **Headers réalistes**
```python
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
```
### 4. **Les delays et comportement humain**
```python
DOWNLOAD_DELAY = 1  # Délai entre requêtes
RANDOMIZE_DOWNLOAD_DELAY = True  # Variation aléatoire
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # Évite la surcharge
```
### 5. **Le système de retry intelligent**
```python
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
```
### 6. **La gestion des cookies**
```python
COOKIES_ENABLED = True
COOKIES_DEBUG = False
```
## 📥 **L'istallation**
### Les prérequis
`Python 3.13+` et `pip`
### Installer les dépendances
```bash
# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
# Installer les packages
pip install scrapy requests curl_cffi selenium playwright
```
### Installer (optionnelement) Playwright
```bash
playwright install chromium
```
## ⚙️ **La configuration**
### `settings.py` - Configuration principale
```python
# Délai entre requêtes
DOWNLOAD_DELAY = 1

# Requêtes concurrentes
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Timeout
DOWNLOAD_TIMEOUT = 30

# Log level
LOG_LEVEL = 'INFO'  # DEBUG pour plus de détails

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'bypass.middlewares.RandomUserAgentMiddleware': 400,
}
```
### Les variables d'environnement (optionnel)
Créez un fichier `.env` :
```env
SCRAPY_LOG_LEVEL=INFO
SCRAPY_DOWNLOAD_DELAY=1
SCRAPY_CONCURRENT_REQUESTS=16
```
## 🚀 **L'utilisation**
### Démarrer le spider
```bash
# Spider basique
scrapy crawl bypass

# Avec output JSON
scrapy crawl bypass -O output.json

# Avec output CSV
scrapy crawl bypass -O output.csv

# Avec log détaillé
scrapy crawl bypass -L DEBUG
```
### Tester la rotation de User-Agents
```bash
# Lancer settings.py directement
python bypass/settings.py
```
Output attendu :
```
✓ Chargé 596 User-Agents depuis Safari.txt
✓ Chargé 2104 User-Agents depuis Firefox.txt
✓ Chargé 852 User-Agents depuis Chrome.txt
✓ Chargé 992 User-Agents depuis Opera.txt

📊 Il y a 4531 User-Agents uniques chargés

[Requête 1] User-Agent utilisé: Mozilla/5.0 (Windows NT 10.0...)
[Requête 2] User-Agent utilisé: Mozilla/5.0 (Macintosh; Intel...)
```
## 📦 **Les dépendances**
### Packages Python
```bash
scrapy>=2.13.4
requests>=2.31.0
curl_cffi>=0.6.0
selenium>=4.15.0
playwright>=1.40.0
lxml>=5.0.0
```
### L'installation complète
```bash
pip install -r requirements.txt
```
**requirements.txt** :
```txt
scrapy==2.13.4
requests==2.32.3
curl-cffi==0.7.4
selenium==4.27.1
playwright==1.49.1
lxml==6.0.2
parsel==1.10.0
twisted==25.5.0
pyOpenSSL==25.3.0
cryptography==46.0.3
```
## 🛡️ **Les bonnes pratiques**
✅ À faire | ❌ À éviter
---|---
Respecter les délais entre requêtes (`DOWNLOAD_DELAY`) | Scraper trop rapidement (risque de ban IP)
Utiliser un User-Agent différent à chaque requête | Utiliser le même User-Agent partout
Vérifier le `robots.txt` avant de scraper | Ignorer les codes d'erreur 429 (Too Many Requests)
Implémenter un système de retry | Scraper des données sensibles sans autorisation
Logger les erreurs et succès | Négliger la gestion des cookies
## 📝 **Licence**
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

<hr><div align="center">

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**

Made with ❤️ and Scrapy
