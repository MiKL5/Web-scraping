import scrapy
from   scrapy.spiders        import CrawlSpider, Rule
from   scrapy.linkextractors import LinkExtractor
import json
from   quotesApi.items       import QuotesapiItem
import pandas as pd


class QuotesSpider(scrapy.Spider):
    name = "quotesapi"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawled_data = []

    def parse(self, response):
        try:
            parse_json = json.loads(response.body)
        except json.JSONDecodeError:
            self.logger.error(f"Erreur de parsing JSON pour {response.url}")
            return
        
        for quote in parse_json["quotes"]:
            author     = quote.get("author", {}).get("name")
            authorLink = quote.get("author", {}).get("link")
            tags       = quote.get("tags",   [])
            citation   = quote.get("text",   "")

            quotesscraped = QuotesapiItem()
            quotesscraped["author"]     = author
            quotesscraped["authorLink"] = authorLink
            quotesscraped["tags"]       = tags
            quotesscraped["citation"]   = citation
            yield quotesscraped

            self.crawled_data.append({
                "author":     author,
                "authorLink": authorLink,
                "tags":       tags,
                "citation":   citation
            })

        if parse_json["has_next"]:
            current_page = parse_json["page"]
            nextPage = current_page + 1
            next_pageUrl = f"https://quotes.toscrape.com/api/quotes?page={nextPage}"
            yield scrapy.Request(url=next_pageUrl, callback=self.parse)

    def closed(self, reason):
        try:
            df = pd.DataFrame(self.crawled_data)
            df.to_csv("export/quotes.csv",         index  = False)
            df.to_json("export/quotes.json",       orient = "records")
            df.to_excel("export/quotes.xlsx",      index  = False)
            df.to_parquet("export/quotes.parquet", index  = False)
            df.to_feather("export/quotes.feather")
            df.to_pickle("export/quotes.pkl")
            df.to_html("export/quotes.html",       index  = False)
            df.to_markdown("export/quotes.md",     index  = False)
            df.to_latex("export/quotes.tex",       index  = False)
            # df.to_string nécessite un buffer, pas un fichier direct
            with open("export/quotes.txt", "w", encoding="utf-8") as f:
                f.write(df.to_string(index=False))
            df.to_clipboard(                index  = False)
            df.to_numpy().tofile("export/quotes.npy")
            df.to_xml("export/quotes.xml",         index  = False)
            print(f"✔ L'export est terminé ➜ {len(df)} citations sont enregistrées")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export : {e}")