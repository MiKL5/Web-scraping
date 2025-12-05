import scrapy


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    async def start(self):
        # Démarrage moderne depuis Scrapy 2.13
        yield scrapy.Request(
            url="https://quotes.toscrape.com/login",
            callback=self.parse_login
        )

    def parse_login(self, response):
        # Gèrer le formulaire de connexion
        token = response.xpath('//input[@name="csrf_token"]/@value').get()
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@method="post"]',
            formdata={
                "csrf_token": token,
                "username": "usr",
                "password": "pwd"
            },
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        # Parser les citations après la connexion
        # Vérifier si la connexion a réussi
        if response.xpath('//a[text()="Logout"]'):
            self.logger.info("✓ Connexion réussie !")
            
            # Extraire toutes les citations de la page
            citations = response.xpath('//div[@class="quote"]')
            for citation in citations:
                text = citation.xpath('span[@class="text"]/text()').get()
                # Nettoyer le texte en enlevant les guillemets
                if text:
                    text = text.strip('“')
                
                yield {
                    "text": text,
                    "author": citation.xpath('span/small[@class="author"]/text()').get(),
                    "tags": citation.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall(),
                }
            
            # Suivre le lien "Next" pour paginer
            next_page = response.xpath('//li[@class="next"]/a/@href').get()
            if next_page:
                self.logger.info(f"→ Page suivante trouvée : {next_page}")
                yield response.follow(next_page, callback=self.parse)
            else:
                self.logger.info("✓ Toutes les pages ont été scrapées")
        else:
            self.logger.error("✗ Échec de la connexion - Le bouton 'Logout' n'a pas été trouvé")