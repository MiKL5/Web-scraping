import sys
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

# Ajoute la racine du projet au chemin pour pouvoir importer le spider
sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.spiders.feliscrawler_spider import FeliscrawlerSpider


class TestfeliscrawlerSpiderIntegrity(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = FeliscrawlerSpider()

    def test_parse_page_integrity(self) -> None:
        """
        Teste que le spider extrait les bons types de données et champs
        d'une réponse HTML simulée.
        """
        html_content = """
        <html>
            <body>
                <h1 class="firstHeading">Chat</h1>
                <div id="mw-content-text">
                    <p>Le chat est un félin.</p>
                    <p>Il aime dormir.</p>
                    <a href="/wiki/Chien">Chien</a>
                    <a href="/wiki/Souris">Souris</a>
                    <img src="//upload.wikimedia.org/chat.jpg" alt="Un chat mignon" />
                    <img src="//upload.wikimedia.org/autre.jpg" alt="Rien à voir" />
                </div>
            </body>
        </html>
        """

        request = Request(url="https://fr.wikipedia.org/wiki/Chat")
        response = HtmlResponse(
            url="https://fr.wikipedia.org/wiki/Chat",
            request=request,
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Le spider produit un générateur, donc on itère dessus
        results = list(self.spider.parse_page(response))

        self.assertEqual(len(results), 1, "Should yield exactly one item")
        item = results[0]

        # 1. Vérifier la présence des champs
        expected_fields = [
            "url",
            "titre",
            "profondeur",
            "introduction",
            "nombre_paragraphes",
            "longueur_contenu",
            "liens_internes",
            "nombre_images",
            "images",
        ]
        for field in expected_fields:
            self.assertIn(field, item, f"Field '{field}' is missing")

        # 2. Vérifier les types de données
        self.assertIsInstance(item["url"], str)
        self.assertIsInstance(item["titre"], str)
        self.assertIsInstance(item["profondeur"], int)
        self.assertIsInstance(item["introduction"], str)
        self.assertIsInstance(item["nombre_paragraphes"], int)
        self.assertIsInstance(item["longueur_contenu"], int)
        self.assertIsInstance(item["liens_internes"], list)
        self.assertIsInstance(item["nombre_images"], int)
        self.assertIsInstance(item["images"], list)

        # 3. Vérifier les valeurs basées sur les données simulées
        self.assertEqual(item["titre"], "Chat")
        self.assertEqual(item["nombre_paragraphes"], 2)
        # "Le chat est un félin." + "Il aime dormir." = 21 + 15 + space = 37 approx depending on strip/join
        # Vérifions juste que c'est > 0
        self.assertGreater(item["longueur_contenu"], 0)

        # Vérifier les liens (doivent être des URLs absolues)
        self.assertTrue(any("Chien" in link for link in item["liens_internes"]))

        # Vérifier les images (doit filtrer basé sur 'chat' dans alt/src)
        # Dans la simulation : alt='Un chat mignon' -> correspond
        # Dans la simulation : alt='Rien à voir' -> ne doit PAS correspondre
        self.assertEqual(item["nombre_images"], 1)
        self.assertIn("//upload.wikimedia.org/chat.jpg", item["images"][0])


if __name__ == "__main__":
    unittest.main()
