from pymongo.mongo_client import MongoClient
from pymongo.server_api   import ServerApi


BOT_NAME = "b2mongo"

SPIDER_MODULES = ["b2mongo.spiders"]
NEWSPIDER_MODULE = "b2mongo.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.5

# Cookies enabled
COOKIES_ENABLED = True

# Disable Telnet Console
TELNETCONSOLE_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'b2mongo.pipelines.BooksImagesPipeline': 200,
    "b2mongo.pipelines.MongoDBPipeline":     300,
}

# Configuration MongoDB LOCAL
MONGO_URI      = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'books_toscrape'

# Tentative de connexion pour vérifier
MONGO_URI      = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'books_toscrape'

# Tentative de connexion pour vérifier
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✓ La connexion est établie à MongoDB")
    print(f"✓ La base de données est {MONGO_DATABASE}")
    client.close()
except Exception as e:
    print(f"✗ L'erreur de connexion à MongoDB est {e}")
    print("Vérifiez que le service MongoDB est démarré")

MONGO_OPTIONS = {
    'serverSelectionTimeoutMS':  5000,  # Timeout de 5 secondes
    'connectTimeoutMS'        : 10000,  # Timeout de connexion 10 secondes
    'socketTimeoutMS'         : 45000,  # Timeout socket 45 secondes
    'maxPoolSize'             :    10,  # Pool de connexions
}

# Configuration des images
IMAGES_STORE        = 'images'     # Dossier pour les images téléchargées
IMAGES_URLS_FIELD   = 'image_url'  # Champ contenant l'URL de l'image
IMAGES_RESULT_FIELD = 'images'     # Champ pour les résultats du téléchargement

# Configuration MongoDB Atlas (Cloud) - DÉSACTIVÉE
# MONGO_URI = 'mongodb+srv://miklgaillard_db_user:vupenl5ixlKWs6El@scrapy.5ruqptn.mongodb.net/?appName=Scrapy'
# MONGO_DATABASE = 'MongoDB_with_scrapy'

# Request fingerprinter
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

# Twisted reactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Logs
LOG_LEVEL = 'INFO'

# SÉCURITÉ & PERFORMANCE
# Retry sur échec
RETRY_ENABLED    = True
RETRY_TIMES      = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Timeout des requêtes
DOWNLOAD_TIMEOUT = 30

# Redirection
REDIRECT_ENABLED   = True
REDIRECT_MAX_TIMES = 3

# DNS cache
DNSCACHE_ENABLED = True
DNSCACHE_SIZE    = 10000

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# STATISTIQUES & MONITORING
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'