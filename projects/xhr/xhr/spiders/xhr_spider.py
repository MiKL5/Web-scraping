import scrapy


class XhrSpiderSpider(scrapy.Spider):
    name            = "xhr_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls      = ["https://quotes.toscrape.com/"]

    # Paramètres configurables
    custom_settings = {
        'DOWNLOAD_DELAY'                 : 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        'ROBOTSTXT_OBEY'                 : True,
        'FEED_EXPORT_ENCODING'           : 'utf-8'
    }

    def __init__(self, author='J.K. Rowling', tag='dumbledore', *args, **kwargs):
        """
        Initialiser le spider avec des paramètres configurables
        
        Args :
            author : Nom de l'auteur à filtrer
            tag    : Tag à rechercher
        
        Usage :
            scrapy crawl xhr_spider -a author="Albert Einstein" -a tag="life"
        """
        super(XhrSpiderSpider, self).__init__(*args, **kwargs)
        self.author = author
        self.tag = tag
        self.logger.info(f"🔍 Recherche: Auteur='{author}', Tag='{tag}'")

    async def start(self):
        """Méthode moderne de démarrage (Scrapy 2.13+)"""
        self.logger.info("🚀 Démarrage du spider XHR")
        yield scrapy.Request(
            url='https://quotes.toscrape.com/search.aspx',
            callback=self.filter,
            errback=self.handle_error
        )

    def filter(self, response):
        """Soumet le formulaire de filtrage avec VIEWSTATE"""
        # Extraction du VIEWSTATE (protection CSRF pour ASP.NET)
        viewstate = response.xpath("//input[@name='__VIEWSTATE']/@value").get()
        
        if not viewstate:
            self.logger.error("❌ VIEWSTATE n'est pas trouvé")
            return
        
        self.logger.info(f"✅ VIEWSTATE ➜ {viewstate[:50]}...")
        
        yield scrapy.FormRequest(
            url='https://quotes.toscrape.com/filter.aspx',
            formdata={
                'author'      : self.author,
                'tag'         : self.tag,
                'submitbutton': 'search',
                '__VIEWSTATE' : viewstate
            },
            dont_filter = True,
            callback    = self.parse,
            errback     = self.handle_error,
            method      = 'POST'
        )

    def parse(self, response):
        """Parser les citations filtrées"""
        citations = response.xpath("//div[@class='quote']")
        
        if not citations:
            self.logger.warning(f"⚠️ Aucune citation trouvée pour {self.author} / {self.tag}")
            return
        
        self.logger.info(f"📚 {len(citations)} citation(s) trouvée(s)")
        
        for citation in citations:
            text   = citation.xpath(".//span[@class='content']/text()").get()
            author = citation.xpath(".//small[@class='author']/text()").get()
            tags   = citation.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
            
            # Nettoyer le texte
            if text:
                text = text.strip('"')
            
            # Vérifier que les données existent
            if text:
                yield {
                    'citation'      : text,
                    'author'        : author or self.author,
                    'tags'          : tags,
                    'search_author' : self.author,
                    'search_tag'    : self.tag
                }
            else:
                self.logger.warning(f"⚠️ Une citation vide est détectée, ignorée")
        
        # Gestion de la pagination si elle existe
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            self.logger.info(f"➡️ La page trouvée est {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("✅ Toutes les citations sont récupérées")

    def handle_error(self, failure):
        """Gèrer les erreurs de requête"""
        self.logger.error(f"❌ Il y a une erreur lors de la requête {failure.value}")
        self.logger.error(f"L'URL est {failure.request.url}")