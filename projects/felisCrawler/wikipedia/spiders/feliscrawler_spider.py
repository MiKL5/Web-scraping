from collections.abc       import Generator, Iterable
from typing                import Any, Dict
from scrapy.http           import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders        import CrawlSpider, Rule


class feliscrawlerSpider(CrawlSpider):
    name            = 'wiki_chat'
    allowed_domains = ['fr.wikipedia.org']
    start_urls      = ['https://fr.wikipedia.org/wiki/Chat']
    
    # Configuration par défaut
    custom_settings = {
        'DEPTH_LIMIT':              6,
        'DOWNLOAD_DELAY':           1.23,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS':      8,
        'ROBOTSTXT_OBEY':           True,
        'USER_AGENT':              'Mozilla/5.0 (compatible; feliscrawlerBot/1.0)',
        'FEEDS': {
            'result.json': {
                'format':   'json',
                'encoding': 'utf8',
                'indent':       4 ,
            }
        }
    }

    # Les règles pour suivre les liens liés aux chats
    rules = (
        Rule(
            LinkExtractor(
                allow = r"/wiki/(Chat|F[ée]lin|F%C3%A9lin|Race_de_chat|Domestication_du_chat)",
                deny  = (
                    r"/wiki/Fichier:",
                    r"/wiki/Sp%C3%A9cial:",
                    r"/wiki/Aide:",
                    r"/wiki/Wikip%C3%A9dia:",
                    r"/wiki/Cat%C3%A9gorie:",
                    r"/wiki/Portail:",
                    r"/wiki/Discussion:",
                    r"/wiki/Mod%C3%A8le:",
                ),
            ),
            callback = "parse_page",
            follow   = True,
        ),
    )

    def parse_start_url(self, response: Response) -> Iterable[dict[str, Any]]:
        return self.parse_page(response)

    def parse_page(self, response: Response) -> Generator[dict[str, Any], None, None]:
        title = response.xpath('//h1[@class="firstHeading"]/text()').get()
        title = (
            response.xpath('//h1[@id="firstHeading"]//text()').get()                or
            response.xpath('//h1[@class="firstHeading"]//text()').get()             or
            response.xpath('//h1//span[@class="mw-page-title-main"]//text()').get() or
            response.xpath('//h1//text()').get()                                    or
            response.css('h1#firstHeading::text').get()                             or
            response.css('h1.firstHeading::text').get()                             or
            "Je n'ai pas trouvé le titre"
        )

        # Premier paragraphe
        introduction = response.xpath(
            '//div[@id="mw-content-text"]//p[not(ancestor::table)][1]//text()'
        ).getall()
        intro_text = " ".join(introduction).strip()

        # Tous les paragraphes du contenu principal
        paragraphes = response.xpath(
            '//div[@id="mw-content-text"]//p[not(ancestor::table)]//text()'
        ).getall()
        contenu_complet = " ".join([p.strip() for p in paragraphes if p.strip()])

        # Liens internes vers d'autres articles
        liens_internes = response.xpath(
            '//div[@id="mw-content-text"]//a[starts-with(@href, "/wiki/")]/@href'
        ).getall()
        liens_internes = list(set(liens_internes))  # Supprime les doublons

        # Images de chats uniquement (filtrage par alt et src)
        images = response.xpath(
            '//div[@id="mw-content-text"]//img['
            'contains(translate(@alt, "CHAT", "chat"), "chat") or '
            'contains(translate(@src, "CHAT", "chat"), "chat") or '
            'contains(translate(@alt, "FÉLIN", "félin"), "félin") or '
            'contains(translate(@alt, "FELIN", "felin"), "felin")'
            "]/@src"
        ).getall()

        depth = response.meta.get("depth", 10)  # Profondeur

        yield {
            'url'               : response.url,
            'titre'             : title,
            'profondeur'        : depth,
            'introduction'      : intro_text[:500] if intro_text else None, # 500 caractères
            'nombre_paragraphes': len([p for p in paragraphes if p.strip()]),
            'longueur_contenu'  : len(contenu_complet),
            'liens_internes'    : [response.urljoin(link) for link in liens_internes[:20]],  # Limite
            'nombre_images'     : len(images),
            'images'            : images[:10],  # Limite
        }