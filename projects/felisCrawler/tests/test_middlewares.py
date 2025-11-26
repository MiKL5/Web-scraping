import sys
import unittest
from   pathlib       import Path
from   unittest.mock import MagicMock, Mock

sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.middlewares import WikipediaSpiderMiddleware, WikipediaDownloaderMiddleware


class TestWikipediaSpiderMiddleware(unittest.TestCase):
    def setUp(self) -> None:
        self.middleware = WikipediaSpiderMiddleware()

    def test_process_spider_output(self) -> None:
        """
        Teste que process_spider_output yield correctement les résultats.
        Couvre la ligne 34 (yield i).
        """
        response = Mock()
        spider = Mock()
        
        # Simuler des résultats du spider
        result = [{"data": "item1"}, {"data": "item2"}]
        
        # Appeler la méthode
        output = list(self.middleware.process_spider_output(response, result, spider))
        
        # Vérifier que tous les items sont yielded
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], {"data": "item1"})
        self.assertEqual(output[1], {"data": "item2"})

    def test_process_spider_exception(self) -> None:
        """
        Teste que process_spider_exception retourne None (pass).
        Couvre la ligne 41 (pass).
        """
        response = Mock()
        exception = Exception("Test exception")
        spider = Mock()
        
        # Appeler la méthode
        result = self.middleware.process_spider_exception(response, exception, spider)
        
        # Vérifier que ça retourne None
        self.assertIsNone(result)


class TestWikipediaDownloaderMiddleware(unittest.TestCase):
    def setUp(self) -> None:
        self.middleware = WikipediaDownloaderMiddleware()

    def test_process_exception(self) -> None:
        """
        Teste que process_exception retourne None (pass).
        Couvre la ligne 94 (pass).
        """
        request = Mock()
        exception = Exception("Download error")
        spider = Mock()
        
        # Appeler la méthode
        result = self.middleware.process_exception(request, exception, spider)
        
        # Vérifier que ça retourne None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
