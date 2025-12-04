import scrapy
from   scrapy.linkextractors import LinkExtractor
from   scrapy.spiders        import CrawlSpider, Rule
from   ..items               import Books2ScrapeItem


class CrawlbooksSpider(CrawlSpider):
    name            = "crawlbooks"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["https://books.toscrape.com"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/h3/a"),callback="parse_item", follow=True), # allow autorise, deny refuse les liens, restrict_xpaths limite la recherche a une partie de la page et restrict_css idem en css, callback appelle une methode sur la page trouvée, follow dit si on continue a chercher des liens sur cette page
             Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"),follow=True),)

    def parse_item(self, response):
        title        = response.xpath("//h1/text()").get()
        price        = response.xpath("//p[@class='price_color']/text()").get()
        product_id   = response.xpath("//th[text()='UPC']/following-sibling::td/text()").get()
        product_type = response.xpath("//th[text()='Product Type']/following-sibling::td/text()").get()
        stock        = response.xpath("//th[text()='Availability']/following-sibling::td/text()").get()

        books = Books2ScrapeItem()
        books['title']        = title
        books['price']        = price
        books['product_id']   = product_id
        books['product_type'] = product_type
        books['stock']        = stock
        yield books