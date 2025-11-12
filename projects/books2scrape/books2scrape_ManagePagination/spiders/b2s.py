import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
        for bloc in books:
            yield {
                'title'  : bloc.xpath('.//h3/a/@title').get(),
                'price'  : bloc.xpath('.//p[@class="price_color"]/text()').get(),
                'img_src': bloc.xpath('.//img/@src').get()
            }

        next = response.xpath("//li[@class='next']/a/@href").get()
        if next:
            new_url = response.urljoin(next)
            yield scrapy.Request(url=new_url,callback=self.parse)