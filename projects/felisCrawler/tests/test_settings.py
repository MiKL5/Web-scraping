import unittest
import sys
from   pathlib import Path


# Ajouter le dossier racine au path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from wikipedia import settings

class TestSettings(unittest.TestCase):
    def test_settings_values(self) -> None:
        self.assertEqual(settings.BOT_NAME, "wikipedia")
        self.assertTrue(settings.ROBOTSTXT_OBEY)
        # ITEM_PIPELINES est commenté par défaut dans Scrapy, vérifions ADDONS à la place
        self.assertIsInstance(settings.ADDONS, dict)
