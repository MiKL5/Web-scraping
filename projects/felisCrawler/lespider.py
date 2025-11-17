import scrapy
from   scrapy.linkextractors import LinkExtractor
from   scrapy.spiders        import CrawlSpider , Rule


class WikiChatSpider(CrawlSpider):
    name = 'wiki_chat'
    allowed_domains = ['fr.wikipedia.org']
    start_urls = ['https://fr.wikipedia.org/wiki/Chat']
    
    # Règles pour suivre les liens
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/wiki/',  # Suit tous les liens /wiki/
                deny=(
                    r'/wiki/Fichier:',  # Ignore les fichiers
                    r'/wiki/Sp%C3%A9cial:',  # Ignore les pages spéciales
                    r'/wiki/Aide:',  # Ignore les pages d'aide
                    r'/wiki/Wikip%C3%A9dia:',  # Ignore les pages meta
                    r'/wiki/Cat%C3%A9gorie:',  # Ignore les catégories
                    r'/wiki/Portail:',  # Ignore les portails
                    r'/wiki/Discussion:',  # Ignore les discussions
                )
            ),
            callback='parse_page',
            follow=True  # Continue à suivre les liens récursivement
        ),
    )
    
    def parse_page(self, response):
        """Parse chaque page crawlée"""
        # Extrait le titre de la page
        title = response.css('h1.firstHeading::text').get()
        
        # Extrait tous les liens de la page
        links = response.css('a[href^="/wiki/"]::attr(href)').getall()
        
        yield {
            'url': response.url,
            'title': title,
            'links_count': len(links),
            'links': [response.urljoin(link) for link in links]
        }


# Pour exécuter le spider, utilisez :
# scrapy runspider wiki_chat_spider.py -o resultats.json
# 
# Options utiles :
# -o resultats.csv : Sauvegarde en CSV
# -o resultats.json : Sauvegarde en JSON
# -L INFO : Niveau de log
# -s DEPTH_LIMIT=3 : Limite la profondeur de crawl
# -s DOWNLOAD_DELAY=1 : Délai entre les requêtes (politesse)
#
# Exemple avec limitations :
# scrapy runspider wiki_chat_spider.py -o resultats.json -s DEPTH_LIMIT=2 -s DOWNLOAD_DELAY=1