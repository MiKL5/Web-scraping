import scrapy
from   scrapy.linkextractors import LinkExtractor
from   scrapy.spiders        import CrawlSpider, Rule
from   ..items               import Books2ScrapeItem
from   scrapy.loader         import ItemLoader


class CrawlbooksSpider(CrawlSpider):
    name            = "crawlbooks"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["https://books.toscrape.com"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/h3/a"),callback="parse_item", follow=True), # allow autorise, deny refuse les liens, restrict_xpaths limite la recherche a une partie de la page et restrict_css idem en css, callback appelle une methode sur la page trouvée, follow dit si on continue a chercher des liens sur cette page
             Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"),follow=True),)

    def parse_item(self, response):
        l = ItemLoader(item = Books2ScrapeItem(), response=response)
        l.add_value('title',        "//h1/text()")
        l.add_value('price',        "//p[@class='price_color']/text()")
        l.add_value('product_id',   "//th[text()='UPC']/following-sibling::td/text()")
        l.add_value('product_type', "//th[text()='Product Type']/following-sibling::td/text()")
        l.add_value('stock',        "//th[text()='Availability']/following-sibling::td/text()")
        yield l.load_item()
        