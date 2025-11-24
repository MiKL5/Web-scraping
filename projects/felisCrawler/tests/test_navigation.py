import sys
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.spiders.feliscrawler_spider import FeliscrawlerSpider


class TestNavigationRules(unittest.TestCase):
    def setUp(self) -> None:
        # Extrait le LinkExtractor des règles du spider
        # La règle 0 est celle qui nous intéresse
        self.link_extractor = FeliscrawlerSpider.rules[0].link_extractor

    def test_allowed_links(self) -> None:
        """Teste que les liens pertinents sont extraits."""
        html = """
        <html>
            <body>
                <a href="/wiki/Chat">Chat</a>
                <a href="/wiki/Félin">Félin</a>
                <a href="/wiki/Race_de_chat">Race de chat</a>
                <a href="/wiki/Domestication_du_chat">Domestication</a>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/Source", body=html.encode("utf-8")
        )
        links = self.link_extractor.extract_links(response)
        extracted_urls = [link.url for link in links]

        self.assertIn("https://fr.wikipedia.org/wiki/Chat", extracted_urls)
        self.assertIn(
            "https://fr.wikipedia.org/wiki/F%C3%A9lin", extracted_urls
        )  # Scrapy encode les URLs
        self.assertIn("https://fr.wikipedia.org/wiki/Race_de_chat", extracted_urls)
        self.assertIn(
            "https://fr.wikipedia.org/wiki/Domestication_du_chat", extracted_urls
        )

    def test_denied_links(self) -> None:
        """Teste que les liens non pertinents ou exclus sont ignorés."""
        html = """
        <html>
            <body>
                <a href="/wiki/Chien">Chien</a>
                <a href="/wiki/Voiture">Voiture</a>
                <a href="/wiki/Fichier:Image.jpg">Fichier</a>
                <a href="/wiki/Discussion:Chat">Discussion</a>
                <a href="/wiki/Aide:Sommaire">Aide</a>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/Source", body=html.encode("utf-8")
        )
        links = self.link_extractor.extract_links(response)
        extracted_urls = [link.url for link in links]

        self.assertEqual(
            len(extracted_urls),
            0,
            f"Should not extract any links, found: {extracted_urls}",
        )


if __name__ == "__main__":
    unittest.main()
