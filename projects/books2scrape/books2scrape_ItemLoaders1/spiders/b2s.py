import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
        for bloc in books:
            link = bloc.xpath('.//h3/a/@href').get()
            yield response.follow(link,callback=self.parse_book_page)

        next = response.xpath("//li[@class='next']/a/@href").get()
        if next:
            new_url = response.urljoin(next)
            yield scrapy.Request(url=new_url,callback=self.parse)

    def parse_book_page(self,response):
        title = response.xpath('//h1/text()').get()
        price = response.xpath('//p[@class="price_color"]/text()').get()
        yield {
            'title':title,
            'price':price
        }