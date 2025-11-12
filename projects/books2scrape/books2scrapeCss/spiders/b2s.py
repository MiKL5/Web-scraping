import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # result = {'title':response.css('title').get()}
        # result = {'title':response.css('title::text').get()}
        # result = {'image':response.css('img::attr(src)').getall()}
        # result = {'alert':response.css('div[role="alert"]::text')}.get()
        result = {'price':response.css('p[class="price_color"]::text').get()}
        yield result