import scrapy
from   scrapy.loader import ItemLoader
from   b2mongo.items import BookItem


class MongoSpider(scrapy.Spider):
    name            =  "mongo"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["https://books.toscrape.com/"]

    def __init__(self, category=None, max_pages=None, *args, **kwargs):
        super(MongoSpider, self).__init__(*args, **kwargs)
        self.category_filter = category
        self.max_pages       = int(max_pages) if max_pages else None
        self.pages_scraped   = 0
        self.books_scraped   = 0
        self.logger.info(f"Le spider démarre 🚀 🚀 🚀")
        if self.category_filter:
            self.logger.info(f"🔍 Filtrage catégoriel {self.category_filter}")
        if self.max_pages:
            self.logger.info(f"Il y a {self.max_pages} pages")

    def parse(self, response):
        """Parser la page d'accueil et extrait les catégories"""
        # Extraire toutes les catégories du menu latéral
        categories = response.xpath('//div[@class="side_categories"]//ul/li/ul/li/a')
        
        self.logger.info(f"📚 {len(categories)} catégories trouvées")
        
        for category in categories:
            category_name = category.xpath('./text()').get().strip()
            category_url  = category.xpath('./@href').get()
            
            # Filtrer par catégorie si demandé
            if self.category_filter and self.category_filter.lower() not in category_name.lower():
                continue
            
            self.logger.info(f"📖 Scraping de la  catégorie {category_name}")
            
            yield response.follow(
                category_url,
                callback = self.parse_category,
                meta     = {'category': category_name}
            )
    
    def parse_category(self, response):
        """Parse une page de catégorie et extrait les livres"""
        category = response.meta['category']
        books    = response.xpath('//article[@class="product_pod"]')
        
        self.logger.info(f"📕 Il y a {len(books)} livres trouvés dans {category}")
        
        # Extraire chaque livre
        for book in books:
            book_url = book.xpath('.//h3/a/@href').get()
            
            yield response.follow(
                book_url,
                callback = self.parse_book,
                meta     = {'category': category}
            )
        
        # Gérer la pagination
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        
        if next_page:
            # Vérifier la limite de pages
            if self.max_pages and self.pages_scraped >= self.max_pages:
                self.logger.info(f"⚠️ La limite de {self.max_pages} pages est atteinte")
                return
            
            self.pages_scraped += 1
            self.logger.info(f"➡️ Page suivante")   # {next_page}
            
            yield response.follow(
                next_page,
                callback = self.parse_category,
                meta     = {'category': category}
            )
        else:
            self.logger.info(f"✅ La collection {category} est complète")
    
    def parse_book(self, response):
        """Parse les détails d'un livre"""
        loader = ItemLoader(item = BookItem(), response = response)
        
        # Informations de base
        loader.add_xpath('title'   , '//div[@class="product_main"]/h1/text()')
        loader.add_value('url'     , response.url)
        loader.add_value('category', response.meta['category'])
        
        # Tableau d'informations produit
        loader.add_xpath('upc'           , '//table[@class="table table-striped"]//tr[1]/td/text()')
        loader.add_xpath('price_excl_tax', '//table[@class="table table-striped"]//tr[3]/td/text()')
        loader.add_xpath('price_incl_tax', '//table[@class="table table-striped"]//tr[4]/td/text()')
        loader.add_xpath('tax'           , '//table[@class="table table-striped"]//tr[5]/td/text()')
        loader.add_xpath('availability'  , '//table[@class="table table-striped"]//tr[6]/td/text()')
        loader.add_xpath('number_of_reviews', '//table[@class="table table-striped"]//tr[7]/td/text()')
        
        # Rating (extraire la classe CSS)
        rating_class = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        if rating_class:
            rating = rating_class.split()[-1]  # Ex: "star-rating Three" -> "Three"
            loader.add_value('rating', rating)
        
        loader.add_xpath('description', '//div[@id="product_description"]/following-sibling::p/text()')
        
        image_url = response.xpath('//div[@class="item active"]//img/@src').get()
        if image_url:
            # Convertir l'URL relative en absolue et l'ajouter comme valeur unique
            absolute_url = response.urljoin(image_url)
            loader.add_value('image_url', absolute_url)
        
        self.books_scraped += 1
        
        if self.books_scraped % 50 == 0:
            self.logger.info(f"{self.books_scraped} livres scrapés")
        
        yield loader.load_item()