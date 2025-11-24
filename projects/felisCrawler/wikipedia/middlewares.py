# Définir ici les modèles pour vos middlewares de spider
#
# Voir la documentation :
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from typing import Any


class WikipediaSpiderMiddleware:
    # Tous les middlewares de spider ne doivent pas nécessairement définir toutes ces méthodes.
    # Si une méthode n'est pas définie, le hook du middleware de spider ne sera pas appelé.

    @classmethod
    def from_crawler(cls, crawler: Any) -> Any:
        # Cette méthode est utilisée par Scrapy pour créer vos spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response: Any, spider: Any) -> Any:
        # Appelé pour chaque réponse qui passe par le middleware de spider
        # et qui entre dans le spider.

        # Doit retourner None ou lever une exception.
        return None

    def process_spider_output(self, response: Any, result: Any, spider: Any) -> Any:
        # Appelé avec les résultats retournés par le Spider, après
        # qu'il a traité la réponse.

        # Retourner un itérable de Request, ou d'objets item.
        for i in result:
            yield i

    def process_spider_exception(self, response: Any, exception: Any, spider: Any) -> Any:
        # Appelé lorsqu'un spider ou une méthode process_spider_input()
        # (d'un autre middleware de spider) lève une exception.

        # Doit retourner soit None, soit un itérable de Request ou d'objets item.
        pass

    def process_start_requests(self, start_requests: Any, spider: Any) -> Any:
        # Appelé avec les requêtes de démarrage du spider, et fonctionne
        # de manière similaire à la méthode process_spider_output(), sauf
        # qu'il n'a pas de réponse associée.

        # Doit retourner un itérable de requêtes (Requests).
        for r in start_requests:
            yield r

    def spider_opened(self, spider: Any) -> None:
        spider.logger.info("Spider ouvert : %s" % spider.name)


class WikipediaDownloaderMiddleware:
    # Tous les middlewares de téléchargement ne doivent pas nécessairement définir toutes ces méthodes.
    # Si une méthode n'est pas définie, le hook du middleware de téléchargement ne sera pas appelé.

    @classmethod
    def from_crawler(cls, crawler: Any) -> Any:
        # Cette méthode est utilisée par Scrapy pour créer vos spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Any, spider: Any) -> Any:
        # Appelé pour chaque requête qui passe par le middleware de téléchargement.

        # Doit soit :
        # - retourner None: continuer le traitement de cette requête
        # - retourner un objet Response: arrête le traitement de process_request()
        # - retourner un objet Request: arrête le traitement de process_request()
        # - ou lever une exception IgnoreRequest: process_exception() est installé.
        return None

    def process_response(self, request: Any, response: Any, spider: Any) -> Any:
        # Appelé avec la réponse retournée par le téléchargeur.

        # Doit soit;
        # - retourner un objet Response
        # - retourner un objet Request
        # - ou lever une exception IgnoreRequest
        return response

    def process_exception(self, request: Any, exception: Any, spider: Any) -> Any:
        # Appelé lorsqu'un gestionnaire de téléchargement ou une méthode process_request()
        # (d'un middleware de téléchargement) lève une exception.

        # Doit soit :
        # - retourner None: continuer le traitement de cette exception
        # - retourner un objet Response: arrête process_exception()
        # - retourner un objet Request: arrête process_exception()
        pass

    def spider_opened(self, spider: Any) -> None:
        spider.logger.info("Spider ouvert : %s" % spider.name)
