import scrapy


class B2sSpider(scrapy.Spider):
    name = "b2s"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')[0],
        # book_title  = response.xpath('.//h3/a/text()').get(),
        # book_price  = response.xpath('.//p[@class="price_color"]/text()').get()
        # books_title = response.xpath("//h3[contains(.//text(),'the')]")
        # text_books  = books_title.xpath('.//text()').getall()
        # category_bloc = response.xpath('//div[@class="side_categories"]/ul/li/ul/li')
        # text_category = category_bloc.xpath('normalize-space(.//a/text())').getall()
        # div_image         = response.xpath('.//div[@class="image_container"]')[0]
        # div_image_child   = div_image.xpath('.//child::node()')
        # div_image_sibling = div_image.xpath('.//following-sibling::node()')
        # div_image_preview = div_image.xpath('.//preview-sibling::node()')
        # div_image_parents = div_image.xpath('.//encestor::node()')
        for bloc in books:
            yield {
                'title'  : bloc.xpath('.//h3/a/@title').get(),
                'price'  : bloc.xpath('.//p[@class=price_color"]/text()').get(),
                'img_src': bloc.path('.//img/src').get
            }

        result = {
            # 'h1'    : response.xpath('//h1'),
            # 'li'    : response.xpath('//li'),
            # 'title' : response.xpath('//head/title/text()').get(),
            # 'links' : response.xpath('//a/text()').getall(),
            # 'altert': response.xpath('//div[@role="alert"]/text()').get(),
            # 'price' : response.xpath('//p[@class="price_color"]/text()').getall(),
            # 'book'  : books,
            # 'title1': book_title,
            # 'price1': book_price,
            # 'url'   : books.xpath('//h3/a/@href').get()
            # 'title2': books.xpath('//h3/a/@title').get()
            # 'links_categories': response.xpath("//a[contains(@href,'/category')]")
            # 'title3': books_title
            # 'title4': text_books
            # 'categorie': text_category
            # 'div'     : div_image_child
            # 'div' : div_image_sibling
            # 'div' : div_image_preview
            # 'div ' : div_image_parents
        }
        yield result

# 2 slash au premier et 1 aux suivants, C'est le langage de requête xpath
# + la méthode text() et get() pour récupérer
# getall() S'il y a plusieurs valeurs
# [0] Si je veux le premier ou get()
# .//text() est un référence relative pour le texte
# following-sibling prend balise suivante de m^me niveau
# preview-sibling prend celle d'avant