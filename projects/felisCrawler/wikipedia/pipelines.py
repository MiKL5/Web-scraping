# Définir vos pipelines d'items ici
#
# Ajouter le pipeline au paramètre ITEM_PIPELINES
# Voir : https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Utile pour gérer différentes classes d'items
from itemadapter import ItemAdapter
from typing import Any

from scrapy import Spider


class WikipediaPipeline:
    def process_item(self, item: Any, spider: Spider) -> Any:
        return item
