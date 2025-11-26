import unittest
from   utils       import csv_name
from   unittest.mock import patch

class TestUtils(unittest.TestCase):
    def test_csv_name_json(self) -> None:
        """Teste la conversion .json -> .csv"""
        self.assertEqual(csv_name("test.json"), "test.csv")

    def test_csv_name_other(self) -> None:
        """Teste avec d'autres extensions"""
        self.assertEqual(csv_name("test.txt"), "test.csv")
        self.assertEqual(csv_name("test"), "test.csv")

    def test_csv_name_path(self) -> None:
        """Teste avec un chemin complet"""
        self.assertEqual(csv_name("/path/to/file.json"), "/path/to/file.csv")

    def test_csv_name_exception(self) -> None:
        # Simuler une erreur de Path pour déclencher le bloc except
        # Comme Path est difficile à faire échouer sur une string valide, on peut mocker Path
        with patch("utils.Path", side_effect=Exception("Boom")):
            self.assertEqual(csv_name("data.json"), "data.csv")
            self.assertEqual(csv_name("data"), "data.csv")
            self.assertEqual(csv_name("error.json"), "error.csv")
