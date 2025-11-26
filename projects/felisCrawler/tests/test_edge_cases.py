import sys
import unittest
from   pathlib     import Path
from   scrapy.http import HtmlResponse, Request

sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.spiders.feliscrawler_spider import feliscrawlerSpider


class TestEdgeCases(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = feliscrawlerSpider()

    def test_missing_title(self) -> None:
        """Tester le comportement quand le titre h1 est manquant."""
        html = "<html><body><p>Just content.</p></body></html>"
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/NoTitle",
            request=Request(url="https://fr.wikipedia.org/wiki/NoTitle"),
            body=html.encode("utf-8"),
        )
        results = list(self.spider.parse_page(response))
        item = results[0]
        self.assertEqual(item["titre"], "Je n'ai pas trouvé le titre")

    def test_empty_content(self) -> None:
        """Tester le comportement quand la div de contenu est manquante ou vide."""
        html = '<html><body><h1 class="firstHeading">Title</h1></body></html>'
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/Empty",
            request=Request(url="https://fr.wikipedia.org/wiki/Empty"),
            body=html.encode("utf-8"),
        )
        results = list(self.spider.parse_page(response))
        item = results[0]
        self.assertEqual(item["nombre_paragraphes"], 0)
        self.assertEqual(item["longueur_contenu"], 0)
        self.assertIsNone(item["introduction"])

    def test_no_images_or_links(self) -> None:
        """Tester le comportement sans images ou liens internes."""
        html = """
        <html>
            <body>
                <h1 class="firstHeading">Title</h1>
                <div id="mw-content-text">
                    <p>Text only.</p>
                </div>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/TextOnly",
            request=Request(url="https://fr.wikipedia.org/wiki/TextOnly"),
            body=html.encode("utf-8"),
        )
        results = list(self.spider.parse_page(response))
        item = results[0]
        self.assertEqual(item["nombre_images"], 0)
        self.assertEqual(item["images"], [])
        self.assertEqual(item["liens_internes"], [])


if __name__ == "__main__":
    unittest.main()
