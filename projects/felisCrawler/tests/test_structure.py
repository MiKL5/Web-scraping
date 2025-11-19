import unittest
import requests
from   pathlib     import Path
import sys
from   scrapy.http import HtmlResponse, Request

# Ajoute la racine du projet au chemin
sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.spiders.feliscrawler_spider import feliscrawlerSpider

class TestfeliscrawlerStructure(unittest.TestCase):
    def setUp(self):
        self.spider = feliscrawlerSpider()
        self.url = 'https://fr.wikipedia.org/wiki/Chat'

    def test_live_page_structure(self):
        """
        Récupère la page en direct et vérifie que le spider peut toujours extraire les éléments clés.
        Cela détecte si la structure HTML de Wikipédia a changé significativement.
        """
        try:
            # 1. Récupérer la page
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; feliscrawlerBot/1.0; +http://example.com/bot)'}
            response_requests = requests.get(self.url, headers=headers, timeout=10)
            response_requests.raise_for_status()
        except requests.RequestException as e:
            self.skipTest(f"Network error or Wikipedia unavailable: {e}")

        # 2. Créer la réponse Scrapy
        request = Request(url=self.url)
        response = HtmlResponse(
            url=self.url,
            request=request,
            body=response_requests.content,
            encoding=response_requests.encoding or 'utf-8'
        )

        # 3. Lancer le spider
        results = list(self.spider.parse_page(response))
        
        self.assertEqual(len(results), 1, "Spider should yield one item for the page")
        item = results[0]

        # 4. Vérifier que les champs critiques ne sont pas vides/None
        # Si cela échoue, cela signifie que les sélecteurs sont probablement cassés
        
        # Titre
        self.assertIsNotNone(item['titre'], "Title selector failed - Structure changed?")
        self.assertNotEqual(item['titre'], "Je n'ai pas trouvé le titre", "Title fallback triggered - Structure changed?")
        
        # Contenu
        self.assertGreater(item['nombre_paragraphes'], 0, "No paragraphs found - Content selector failed?")
        self.assertGreater(item['longueur_contenu'], 0, "Content length is 0 - Content selector failed?")
        
        # Images (Il devrait toujours y avoir des images sur la page Chat)
        self.assertGreater(item['nombre_images'], 0, "No images found - Image selector failed?")
        
        # Liens internes
        self.assertGreater(len(item['liens_internes']), 0, "No internal links found - Link selector failed?")

        print(f"\n[SUCCESS] Live structure test passed for {self.url}")
        print(f"  - Title found: {item['titre']}")
        print(f"  - Paragraphs: {item['nombre_paragraphes']}")
        print(f"  - Images: {item['nombre_images']}")

if __name__ == '__main__':
    unittest.main()
