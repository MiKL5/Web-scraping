import unittest
import sys
from   pathlib       import Path
from   unittest.mock import MagicMock, AsyncMock, patch
from   typing        import Any

# Ajouter le répertoire racine au path pour importer wikipedia
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from wikipedia.pipelines   import WikipediaPipeline
from wikipedia.middlewares import WikipediaSpiderMiddleware, WikipediaDownloaderMiddleware
from wikipedia.items       import WikipediaItem

class TestComponents(unittest.TestCase):
    def test_pipeline_process_item(self) -> None:
        """Teste que le pipeline retourne l'item tel quel."""
        pipeline = WikipediaPipeline()
        item = {"test": "data"}
        spider = MagicMock()
        result = pipeline.process_item(item, spider)
        self.assertEqual(result, item)

    def test_spider_middleware(self) -> None:
        """Teste les méthodes du middleware de spider."""
        middleware = WikipediaSpiderMiddleware()
        spider = MagicMock()
        response = MagicMock()
        
        # Test process_spider_input
        self.assertIsNone(middleware.process_spider_input(response, spider))
        
        # Test process_spider_output
        result = list(middleware.process_spider_output(response, [], spider))
        self.assertEqual(result, [])
        
        # Test spider_opened
        spider = MagicMock()
        middleware.spider_opened(spider)
        spider.logger.info.assert_called()

    def test_downloader_middleware(self) -> None:
        """Teste les méthodes du middleware de téléchargement."""
        middleware = WikipediaDownloaderMiddleware()
        spider = MagicMock()
        request = MagicMock()
        response = MagicMock()
        
        # Test process_request
        self.assertIsNone(middleware.process_request(request, spider))
        
        # Test process_response
        self.assertEqual(middleware.process_response(request, response, spider), response)
        
        # Test spider_opened
        spider = MagicMock()
        middleware.spider_opened(spider)
        spider.logger.info.assert_called()

    def test_downloader_middleware_from_crawler(self) -> None:
        """Teste la méthode de classe from_crawler."""
        crawler = MagicMock()
        middleware = WikipediaDownloaderMiddleware.from_crawler(crawler)
        self.assertIsInstance(middleware, WikipediaDownloaderMiddleware)
        crawler.signals.connect.assert_called()

    def test_item(self) -> None:
        item = WikipediaItem()
        self.assertIsInstance(item, WikipediaItem)

    def test_spider_middleware_process_start_requests(self) -> None:
        """Teste la méthode process_start_requests."""
        middleware = WikipediaSpiderMiddleware()
        spider = MagicMock()
        
        # Créer des requêtes mockées
        mock_requests = [MagicMock(), MagicMock()]
        
        # Tester que process_start_requests yield toutes les requêtes
        results = list(middleware.process_start_requests(mock_requests, spider))
        self.assertEqual(results, mock_requests)

    def test_spider_middleware_methods(self) -> None:
        middleware = WikipediaSpiderMiddleware()
        # Test spider_opened
        spider = MagicMock()
        middleware.spider_opened(spider)
        spider.logger.info.assert_called()

        # Test from_crawler
        crawler = MagicMock()
        obj = middleware.from_crawler(crawler)
        self.assertIsInstance(obj, WikipediaSpiderMiddleware)
