import scrapy
from   scrapy.linkextractors import LinkExtractor
from   scrapy.spiders        import CrawlSpider, Rule


class BypassSpider(CrawlSpider):
    name            = "bypass"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["https://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pager"]/li[@class="next"]/a')),
    )
    def parse_item(self, response):
        yield {
            'user_agent':  response.request.headers.get('User-Agent').decode('utf-8'),
            'title':       response.xpath('//div[@class="product_main"]/h1/text()').get(),
            'product_id': response.url.split('/')[-2],
            'product_type': response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get(),
            'price':       response.xpath('//p[@class="price_color"]/text()').get(),
            'stock':       response.xpath('//p[@class="instock availability"]/text()').re_first('\d+'),
            'availability': response.xpath('//p[@class="instock availability"]/text()').re_first('\S+'),
        }