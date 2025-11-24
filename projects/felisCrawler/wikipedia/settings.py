# Paramètres Scrapy pour le projet FelisCrwler
#
# Pour plus de simplicité, ce fichier contient uniquement les paramètres considérés comme importants ou
# couramment utilisés. Vous pouvez trouver plus de paramètres en consultant la documentation :
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from typing import Dict, Any

BOT_NAME = "wikipedia"

SPIDER_MODULES = ["wikipedia.spiders"]
NEWSPIDER_MODULE = "wikipedia.spiders"


# Crawl de manière responsable en s'identifiant (et votre site web) sur l'user-agent
# USER_AGENT = "wikipedia (+http://www.yourdomain.com)"

# Respecter les règles robots.txt
ROBOTSTXT_OBEY = True

# Configurer un délai de téléchargement pour les requêtes vers le même site web (par défaut : 0)
# Voir https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# Voir aussi les paramètres autothrottle et docs
# DOWNLOAD_DELAY = 3
# Le délai de téléchargement s'applique à un seul site web, pas à tous
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Désactiver les cookies (activés par défaut)
# COOKIES_ENABLED = False

# Désactiver l'extension Telnet Console (activée par défaut)
# TELNETCONSOLE_ENABLED = False

# Remplacer les en-têtes de requête par défaut :
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Activer ou désactiver les middlewares de spider
# Voir https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "wikipedia.middlewares.WikipediaSpiderMiddleware": 543,
# }

# Activer ou désactiver les middlewares de téléchargement
# Voir https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "wikipedia.middlewares.WikipediaDownloaderMiddleware": 543,
# }

# Activer ou désactiver les extensions
# Voir https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configurer les pipelines d'items
# Voir https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "wikipedia.pipelines.WikipediaPipeline": 300,
# }

# Activer et configurer l'extension AutoThrottle (désactivée par défaut)
# Voir https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# Le délai de téléchargement initial
# AUTOTHROTTLE_START_DELAY = 5
# Le délai de téléchargement maximum à définir en cas de latences élevées
# AUTOTHROTTLE_MAX_DELAY = 60
# La moyenne des requêtes Scrapy à envoyer en parallèle au serveur
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Activer l'affichage des statistiques de throttling pour chaque réponse reçue :
# AUTOTHROTTLE_DEBUG = False

# Activer et configurer la mise en cache HTTP (désactivée par défaut)
# Voir https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Configurer la gestion asynchrone future de Twisted pour reactor
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Addons Scrapy
ADDONS: Dict[str, int] = {}
