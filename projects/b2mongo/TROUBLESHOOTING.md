# **🔧 Troubleshooting - Books to MongoDB**
Guide de résolution des problèmes courants et solutions aux erreurs fréquentes.
## 🗄️ Erreurs MongoDB
### Erreur : "Connection refused" ou "Server not available"
**Symptômes** :
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: 
[Errno 111] Connection refused
```
**Cause** : MongoDB n'est pas démarré.  
**Solutions** :
```sh
# Linux
sudo systemctl status mongod
sudo systemctl start mongod
sudo systemctl enable mongod  # Démarrage automatique

# macOS
brew services start mongodb-community

# Windows
net start MongoDB

# Vérifier le port
sudo netstat -tulpn | grep 27017
```
**Alternative** : Changer le port dans `settings.py` :
```py
MONGO_URI = 'mongodb://localhost:27018/'  # Port alternatif
```
### Erreur : "Authentication failed"
**Symptômes** :
```
pymongo.errors.OperationFailure: Authentication failed
```
**Cause** : MongoDB configuré avec authentification mais identifiants incorrects.  
**Solutions** :
```py
# Dans settings.py
MONGO_URI = 'mongodb://username:password@localhost:27017/'
MONGO_DATABASE = 'books_toscrape'

# Ou créer un utilisateur
```
```js
// Dans mongosh
use admin
db.createUser({
  user: "scraper",
  pwd: "password123",
  roles: [{role: "readWrite", db: "books_toscrape"}]
})
```
### Erreur : "Duplicate key error"
**Symptômes** :
```
pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: 
books_toscrape.books index: upc_1 dup key: { upc: "abc123" }
```
**Cause** : Tentative d'insertion d'un livre avec un UPC existant (ne devrait pas arriver avec upsert).  
**Solutions** :
```py
# Vérifier que le pipeline utilise bien upsert=True
db.books.update_one(
    {'upc': item['upc']},
    {'$set': item_dict},
    upsert=True  # ← Important
)

# Si persistant, supprimer l'index et le recréer
```
```js
// Dans mongosh
db.books.dropIndex("upc_1")
db.books.createIndex({upc: 1}, {unique: true})
```
### Erreur : "Database locked"
**Symptômes** :
```
pymongo.errors.OperationFailure: database is locked
```
**Cause** : Arrêt incorrect de MongoDB ou corruption.  
**Solutions** :
```sh
# Supprimer le fichier de lock
sudo rm /var/lib/mongodb/mongod.lock

# Réparer la base
mongod --repair

# Redémarrer
sudo systemctl start mongod
```
## 🕷️ Erreurs Scrapy
### Erreur : "ModuleNotFoundError: No module named 'scrapy'"
**Symptômes** :
```
ModuleNotFoundError: No module named 'scrapy'
```
**Cause** : Scrapy non installé ou mauvais environnement virtuel.  
**Solutions** :
```sh
# Vérifier l'environnement
which python
pip list | grep -i scrapy

# Installer Scrapy
pip install scrapy

# Ou réinstaller toutes les dépendances
pip install -r requirements.txt
```
### Erreur : "ImportError: cannot import name 'BookItem'"
**Symptômes** :
```
ImportError: cannot import name 'BookItem' from 'b2mongo.items'
```
**Cause** : Problème de structure de projet ou fichier manquant.  
**Solutions** :
```sh
# Vérifier la structure
ls -la b2mongo/
# Doit contenir : __init__.py, items.py, spiders/, etc.

# Vérifier que __init__.py existe
touch b2mongo/__init__.py
touch b2mongo/spiders/__init__.py

# Réinstaller le projet en mode développement
pip install -e .
```
### Erreur : "Spider not found"
**Symptômes** :
```sh
$ scrapy crawl mongo
KeyError: 'Spider not found: mongo'
```
**Cause** : Mauvais dossier de travail ou nom incorrect.  
**Solutions** :
```sh
# Vérifier que vous êtes dans le bon dossier
pwd  # Doit afficher .../b2mongo

# Lister les spiders disponibles
scrapy list

# Vérifier le nom du spider dans mongo.py
grep "name =" b2mongo/spiders/mongo.py
# Doit afficher : name = "mongo"

# Si le nom est différent
scrapy crawl <nom_affiché>
```
### Erreur : "robots.txt disallow"
**Symptômes** :
```
[scrapy.downloadermiddlewares.robotstxt] DEBUG: 
Forbidden by robots.txt: <GET https://...>
```
**Cause** : Le site bloque le scraping via robots.txt.  
**Solutions** :
```py
# Dans settings.py
ROBOTSTXT_OBEY = False  # ⚠️ Utiliser avec précaution

# books.toscrape.com autorise le scraping
# Vérifier : https://books.toscrape.com/robots.txt
```
### Erreur : "Twisted reactor already installed"
**Symptômes** :
```
ReactorAlreadyInstalledError: reactor already installed
```
**Cause** : Conflit entre asyncio et twisted.  
**Solutions** :
```py
# Dans settings.py, commenter ou changer
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Ou utiliser le reactor par défaut
TWISTED_REACTOR = "twisted.internet.selectreactor.SelectReactor"
```
## 🖼️ Problèmes d'images
### Erreur : Images non téléchargées
**Symptômes** :
```
[scrapy.pipelines.images] WARNING: File (unknown-error): Error downloading file
```
**Causes possibles** :
1. URL d'image invalide
2. Pipeline d'images désactivé
3. Dossier `images/` sans permissions  
**Solutions** :
```sh
# Vérifier les permissions
ls -la images/
chmod -R 755 images/

# Créer le dossier manuellement
mkdir -p images/full

# Vérifier la configuration
grep IMAGES_STORE b2mongo/settings.py
# Doit afficher : IMAGES_STORE = 'images'

# Vérifier que le pipeline est activé
grep BooksImagesPipeline b2mongo/settings.py
# Doit être présent avec priority < 300
```
**Debug** :
```py
# Dans mongo.py, ajouter des logs
image_url = response.xpath('.../@src').get()
if image_url:
    absolute_url = response.urljoin(image_url)
    self.logger.info(f"🖼️ Image URL: {absolute_url}")  # ← Debug
    loader.add_value('image_url', absolute_url)
```
### Erreur : "OSError: [Errno 28] No space left on device"
**Symptômes** :
```
OSError: [Errno 28] No space left on device
```
**Cause** : Disque plein.  
**Solutions** :
```sh
# Vérifier l'espace disque
df -h

# Nettoyer les anciennes images
rm -rf images/full/*

# Limiter le scraping
scrapy crawl mongo -a max_pages=5
```
### Images corrompues ou incomplètes
**Symptômes** : Images non ouvrables ou taille 0.  
**Cause** : Téléchargement interrompu ou timeout.  
**Solutions** :
```py
# Dans settings.py, augmenter le timeout
DOWNLOAD_TIMEOUT = 60  # Au lieu de 30

# Augmenter les retries
RETRY_TIMES = 5

# Supprimer les images corrompues
```
```sh
# Trouver les images de taille 0
find images/full -type f -size 0 -delete

# Re-scraper pour télécharger à nouveau
scrapy crawl mongo
```
## ⚡ Problèmes de performance
### Scraping trop lent
**Symptômes** : Moins de 1 page/minute.  
**Causes** :
1. DOWNLOAD_DELAY trop élevé
2. Concurrence trop faible
3. Problème réseau  
**Solutions** :
```py
# Dans settings.py
DOWNLOAD_DELAY = 0.25  # Réduire (attention au serveur)
CONCURRENT_REQUESTS_PER_DOMAIN = 4  # Augmenter
CONCURRENT_REQUESTS = 32  # Augmenter

# Désactiver les cookies si non nécessaires
COOKIES_ENABLED = False

# Désactiver certains logs
LOG_LEVEL = 'INFO'  # Au lieu de DEBUG
```
**Monitoring** :
```sh
# Voir la vitesse en temps réel
scrapy crawl mongo 2>&1 | grep "Crawled"

# Résultat typique :
# Crawled 150 pages (at 5 pages/min)
```
### MongoDB trop lent
**Symptômes** : Insertions lentes, CPU élevé.  
**Causes** :
1. Pas d'index
2. Trop de connexions simultanées
3. MongoDB non optimisé  
**Solutions** :
```js
// Vérifier les index
db.books.getIndexes()

// Créer les index si manquants
db.books.createIndex({upc: 1}, {unique: true})
db.books.createIndex({category: 1})
db.books.createIndex({rating: 1})

// Statistiques
db.books.stats()
```
```py
# Dans settings.py
MONGO_OPTIONS = {
    'maxPoolSize': 5,  # Réduire le pool
    'socketTimeoutMS': 30000,
}
```
### Mémoire saturée
**Symptômes** : Process killed, OOM error.  
**Cause** : Trop d'items en mémoire.  
**Solutions** :
```py
# Dans settings.py
# Limiter les requêtes concurrentes
CONCURRENT_REQUESTS = 16  # Réduire

# Activer le garbage collector agressif
import gc
gc.set_threshold(700, 10, 10)

# Limiter la queue des items
CONCURRENT_ITEMS = 100
```
## 📊 Problèmes de données
### Données manquantes ou None
**Symptômes** : Champs `None` dans MongoDB.  
**Causes** :
1. XPath incorrect
2. Structure HTML changée
3. Processeur défaillant  
**Solutions** :
```sh
# Tester les XPath dans Scrapy shell
scrapy shell "https://books.toscrape.com/catalogue/..."

>>> response.xpath('//h1/text()').get()  # Test unitaire
>>> response.xpath('//table//tr[1]/td/text()').get()
```
**Debug dans le spider** :
```py
def parse_book(self, response):
    title = response.xpath('//h1/text()').get()
    self.logger.info(f"📖 Titre extrait : {title}")  # ← Debug
    
    if not title:
        self.logger.error(f"❌ Titre manquant pour {response.url}")
```
### Prix incorrects (0.0 ou NaN)
**Symptômes** : Tous les prix à 0.  
**Cause** : Processeur `clean_price()` défaillant.  
**Solutions** :
```py
# Tester le processeur
from b2mongo.items import clean_price

test_prices = [
    "£51.77",
    "Â£32.50",
    "Ã‚Â£10.00"
]

for p in test_prices:
    result = clean_price(p)
    print(f"{p} → {result}")

# Si échec, améliorer la fonction
def clean_price(price):
    if price:
        # Supprimer tous les caractères non-numériques sauf . et ,
        import re
        cleaned = re.sub(r'[^\d.,]', '', price)
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0
```
### Ratings invalides (0)
**Symptômes** : Tous les ratings à 0.  
**Cause** : Extraction de la classe CSS échoue.  
**Solutions** :
```py
# Dans parse_book()
rating_class = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
self.logger.debug(f"⭐ Rating class: {rating_class}")  # ← Debug

if rating_class:
    rating = rating_class.split()[-1]
    self.logger.debug(f"⭐ Rating value: {rating}")  # ← Debug
    loader.add_value('rating', rating)
```
### Descriptions HTML non nettoyées
**Symptômes** : `<p>Text</p>` au lieu de `Text`.  
**Cause** : Processeur `remove_tags` non appliqué.  
**Solutions** :
```py
# Vérifier items.py
description = scrapy.Field(
    input_processor=MapCompose(remove_tags, str.strip),  # ← Important
    output_processor=Join('\n')
)

# Tester manuellement
from w3lib.html import remove_tags
html = "<p>Test <strong>bold</strong></p>"
print(remove_tags(html))  # → "Test bold"
```
## ⚙️ Erreurs de configuration
### Erreur : "ITEM_PIPELINES not found"
**Symptômes** : Aucune donnée insérée dans MongoDB.  
**Cause** : Pipelines non configurés.  
**Solutions** :
```py
# Dans settings.py, vérifier
ITEM_PIPELINES = {
    'b2mongo.pipelines.BooksImagesPipeline': 200,
    'b2mongo.pipelines.MongoDBPipeline': 300,
}

# Syntaxe correcte : chemin.complet.NomClasse: priorité
```
### Erreur : Settings non pris en compte
**Symptômes** : Modifications de `settings.py` ignorées.  
**Causes** :
1. Mauvais fichier `scrapy.cfg`
2. Settings surchargés en ligne de commande  
**Solutions** :
```sh
# Vérifier scrapy.cfg
cat scrapy.cfg
# [settings]
# default = b2mongo.settings  # ← Doit pointer vers settings.py

# Forcer les settings
scrapy crawl mongo -s DOWNLOAD_DELAY=1

# Voir les settings actifs
scrapy settings --get DOWNLOAD_DELAY
```
## 🐛 Debugging
### Mode verbose
```sh
# Logs détaillés
scrapy crawl mongo -s LOG_LEVEL=DEBUG

# Encore plus de détails
scrapy crawl mongo -s LOG_LEVEL=DEBUG -s DEPTH_STATS_VERBOSE=True
```
### Scrapy shell interactif
```sh
# Tester une page spécifique
scrapy shell "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Dans le shell
>>> response.xpath('//h1/text()').get()
>>> view(response)  # Ouvre dans le navigateur
>>> fetch('https://autre-url.com')  # Changer d'URL
```
### Logs structurés
```py
# Ajouter des logs dans le spider
self.logger.debug(f"🐛 Debug: {variable}")
self.logger.info(f"ℹ️ Info: {message}")
self.logger.warning(f"⚠️ Warning: {issue}")
self.logger.error(f"❌ Error: {error}")
```
### Breakpoints Python
```py
# Dans le spider
def parse_book(self, response):
    import pdb; pdb.set_trace()  # ← Arrêt debugger
    # Inspecter variables : print(response.url)
```
### Stats Scrapy
```py
# À la fin du scraping
from scrapy.statscollectors import MemoryStatsCollector

stats = crawler.stats.get_stats()
print(f"Pages scrapées : {stats.get('response_received_count')}")
print(f"Items scrapés : {stats.get('item_scraped_count')}")
print(f"Erreurs : {stats.get('log_count/ERROR', 0)}")
```
## 📞 Obtenir de l'aide
### Checklist avant de demander de l'aide
- [ ] MongoDB est-il démarré ? (`sudo systemctl status mongod`)
- [ ] Les dépendances sont-elles installées ? (`pip list`)
- [ ] Êtes-vous dans le bon dossier ? (`scrapy list`)
- [ ] Les logs contiennent-ils des erreurs ? (chercher `ERROR`)
- [ ] Avez-vous testé en mode DEBUG ? (`-s LOG_LEVEL=DEBUG`)
### Informations à fournir
```sh
# Version Python
python --version

# Version Scrapy
scrapy version -v

# Version MongoDB
mongod --version

# Structure du projet
tree -L 2 b2mongo/

# Logs complets
scrapy crawl mongo 2>&1 | tee error.log
```
### Ressources externes
- **Documentation Scrapy** : https://docs.scrapy.org/
- **Documentation MongoDB** : https://docs.mongodb.com/
- **Stack Overflow** : Tag `scrapy` ou `pymongo`
- **GitHub Issues** : Ouvrir un ticket avec les logs
## 🎯 Checklist de diagnostic rapide
Problème | Commande de diagnostic
---|---
MongoDB down | `sudo systemctl status mongod`
Port occupé | `netstat -tulpn \| grep 27017`
Dépendances manquantes | `pip list \| grep -E "scrapy\|pymongo"`
Spider introuvable | `scrapy list`
Permissions images | `ls -la images/`
Espace disque | `df -h`
Settings actifs | `scrapy settings --get ITEM_PIPELINES`
XPath incorrect | `scrapy shell <URL>`
___
**Conseil** : La plupart des problèmes se résolvent en activant les logs DEBUG et en lisant attentivement les messages d'erreur.