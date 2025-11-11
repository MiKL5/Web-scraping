import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')[0],
        book_title = response.xpath('.//h3/a/text()').get(),
        book_price = response.xpath('.//p[@class="price_color"]/text()').get()
        
        result = {
            'h1'    : response.xpath('//h1'),
            'li'    : response.xpath('//li'),
            'title' : response.xpath('//head/title/text()').get(),
            'links' : response.xpath('//a/text()').getall(),
            'altert': response.xpath('//div[@role="alert"]/text()').get(),
            'price' : response.xpath('//p[@class="price_color"]/text()').getall(),
            'book'  : books,
            'title1': book_title,
            'price1': book_price,
            'url'   : books.xpath('//h3/a/@href').get(),
            'title2': books.xpath('//h3/a/@title').get()
        }
        yield result

# 2 slash au premier et 1 aux suivants, C'est le langage de requête xpath
# + la méthode text() et get() pour récupérer
# getall() S'il y a plusieurs valeurs
# [0] Si je veux le premier ou get()