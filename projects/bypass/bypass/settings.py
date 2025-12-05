# Scrapy settings for bypass project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import random


BOT_NAME = "bypass"

SPIDER_MODULES = ["bypass.spiders"]
NEWSPIDER_MODULE = "bypass.spiders"

ADDONS = {}

# URLs des listes de User-Agents
urls = [
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Safari.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Firefox.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Chrome.txt",
    "https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/refs/heads/master/Opera.txt"
]

# User-Agent par défaut
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

# Pool global de User-Agents
user_agents_pool = []


def load_user_agents():
    """Charge tous les User-Agents depuis les URLs avec rotation"""
    global user_agents_pool
    
    for idx, url in enumerate(urls):
        # Changer le User-Agent pour chaque URL récupérée
        if user_agents_pool:
            current_ua = random.choice(user_agents_pool)
        else:
            current_ua = DEFAULT_UA
        
        headers = {"User-Agent": current_ua}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                # Filtrer les lignes vides et les en-têtes
                valid_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
                
                if len(valid_lines) > 2:
                    user_agents_pool.extend(valid_lines[2:])
                else:
                    user_agents_pool.extend(valid_lines)
                
                print(f"✓ Chargé {len(valid_lines)} User-Agents depuis {url.split('/')[-1]} avec UA: {current_ua[:50]}...")
            else:
                print(f"✗ Erreur {response.status_code} lors du chargement de {url}")
        
        except requests.RequestException as e:
            print(f"✗ Erreur de connexion pour {url}: {e}")
    
    # Supprimer les doublons
    user_agents_pool = list(set(user_agents_pool))
    print(f"\n📊 Total: {len(user_agents_pool)} User-Agents uniques chargés\n")


def get_random_user_agent():
    """Retourne un User-Agent aléatoire depuis le pool"""
    return random.choice(user_agents_pool) if user_agents_pool else DEFAULT_UA


# Charger les User-Agents avec rotation
load_user_agents()

# Copier dans la liste 'ua' pour compatibilité
ua = user_agents_pool.copy()


# Test: requêtes avec User-Agent différent à chaque fois
if __name__ == "__main__":
    print("=" * 80)
    print("TEST: 5 requêtes avec User-Agents différents")
    print("=" * 80)
    
    for i in range(5):
        user_agent = get_random_user_agent()
        headers = {"User-Agent": user_agent}
        
        try:
            response = requests.get("https://httpbin.org/user-agent", headers=headers, timeout=5)
            print(f"\n[Requête {i+1}]")
            print(f"User-Agent utilisé: {user_agent[:80]}...")
            print(f"Réponse serveur: {response.json()}")
        except requests.RequestException as e:
            print(f"\n[Requête {i+1}] Erreur: {e}")


# Configuration Scrapy pour utiliser les User-Agents rotatifs
USER_AGENT = get_random_user_agent()

# Middleware Scrapy personnalisé pour rotation automatique
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        request.headers['User-Agent'] = get_random_user_agent()


# Ajouter à DOWNLOADER_MIDDLEWARES dans settings.py:
DOWNLOADER_MIDDLEWARES = {
    'bypass.middlewares.RandomUserAgentMiddleware': 400,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1.75632
RANDIMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "bypass.middlewares.BypassDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "bypass.pipelines.BypassPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
