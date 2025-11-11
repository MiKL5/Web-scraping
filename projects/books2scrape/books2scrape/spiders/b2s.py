import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        pass