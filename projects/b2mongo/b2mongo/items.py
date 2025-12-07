import scrapy
from   itemloaders.processors import TakeFirst, MapCompose, Join
from   w3lib.html             import remove_tags


def clean_price(price):  # Nettoie le prix et le convertit en float
    if price:
        return float(price.replace('£', '').replace('Â', '').strip())
    return 0.0


def clean_stock(stock):  # Extrait le nombre de livres en stock
    if stock:
        import re
        match = re.search(r'\d+', stock)
        return int(match.group()) if match else 0
    return 0


def rating_to_number(rating):   # Convertit le rating texte en nombre
    ratings = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    return ratings.get(rating, 0)


class BookItem(scrapy.Item):
    title                = scrapy.Field(
        output_processor = TakeFirst()
    )
    url                  = scrapy.Field(
        output_processor = TakeFirst()
    )
    upc                  = scrapy.Field(
        output_processor = TakeFirst()
    )
    price_excl_tax       = scrapy.Field(
        input_processor  = MapCompose(clean_price),
        output_processor = TakeFirst()
    )
    price_incl_tax       = scrapy.Field(
        input_processor  = MapCompose(clean_price),
        output_processor = TakeFirst()
    )
    tax                  = scrapy.Field(
        input_processor  = MapCompose(clean_price),
        output_processor = TakeFirst()
    )
    availability         = scrapy.Field(
        input_processor  = MapCompose(clean_stock),
        output_processor = TakeFirst()
    )
    rating               = scrapy.Field(
        input_processor  = MapCompose(rating_to_number),
        output_processor = TakeFirst()
    )
    category             = scrapy.Field(
        output_processor = TakeFirst()
    )
    description          = scrapy.Field(
        input_processor  = MapCompose(remove_tags, str.strip),
        output_processor = Join('\n')
    )
    number_of_reviews    = scrapy.Field(
        input_processor  = MapCompose(int),
        output_processor = TakeFirst()
    )
    image_url            = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_path           = scrapy.Field() # Champ pour stocker le chemin de l'image