import pymongo
import scrapy
from   itemadapter             import ItemAdapter
from   scrapy.pipelines.images import ImagesPipeline
from   scrapy.exceptions       import DropItem


class MongoDBPipeline:
    """Pipeline pour stocker les items dans MongoDB"""
    collection_name = 'books'
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db  = mongo_db
        self.client    = None
        self.db        = None
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017/'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'books_db')
        )
    
    def open_spider(self, spider):
        """Connexion à MongoDB au démarrage du spider"""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            spider.logger.info(f"✅ Connexion établie à MongoDB {self.mongo_db}")
            
            # Créer des index pour optimiser les recherches
            self.db[self.collection_name].create_index('upc', unique=True)
            self.db[self.collection_name].create_index('category')
            self.db[self.collection_name].create_index('rating')
            
        except Exception as e:
            spider.logger.error(f"❌ Erreur de connexion à MongoDB {e}")
            raise
    
    def close_spider(self, spider):
        """Fermeture de la connexion MongoDB"""
        if self.client:
            # Statistiques finales
            count = self.db[self.collection_name].count_documents({})
            spider.logger.info(f"📊 Il y a {count} livres stockés")
            self.client.close()
            spider.logger.info("✅ La connexion est fermée")
    
    def process_item(self, item, spider):
        """Traiter et insérer chaque item"""
        try:
            # Convertir l'item en dictionnaire
            item_dict = ItemAdapter(item).asdict()
            
            # Mettre à jour ou insérer (upsert)
            result = self.db[self.collection_name].update_one(
                {'upc': item_dict['upc']},
                {'$set': item_dict},
                upsert=True
            )
            
            if result.upserted_id:
                spider.logger.debug(f"✅ {item_dict.get('title', 'N/A')} est ajouté")
            else:
                spider.logger.debug(f"🔄 {item_dict.get('title', 'N/A')} est à jour ")
            
            return item
            
        except Exception as e:
            spider.logger.error(f"❌ Erreur d'insertion à MongoDB: {e}")
            raise DropItem(f"Erreur MongoDB: {e}")


class BooksImagesPipeline(ImagesPipeline):
    """Pipeline pour télécharger les images des livres"""
    
    def get_media_requests(self, item, info):
        """Télécharger l'image du livre"""
        adapter = ItemAdapter(item)
        image_url = adapter.get('image_url')
        
        if image_url:
            # ✅ Vérification que l'URL est valide
            if isinstance(image_url, str) and image_url.startswith('http'):
                info.spider.logger.debug(f"📷 Téléchargement image: {image_url}")
                yield scrapy.Request(image_url)
            else:
                info.spider.logger.warning(f"⚠️ L'URL de l'image est invalide {image_url}")
    
    def item_completed(self, results, item, info):
        """Traiter les résultats du téléchargement"""
        adapter = ItemAdapter(item)
        
        if results:
            ok, result = results[0]
            if ok:
                adapter['image_path'] = result['path']
                info.spider.logger.debug(f"✅ Image sauvegardée: {result['path']}")
            else:
                info.spider.logger.warning(f"❌ Échec du téléchargement de l'image pour {adapter.get('title', 'N/A')}")
        
        return item