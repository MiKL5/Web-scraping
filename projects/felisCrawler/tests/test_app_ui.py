import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ajouter le dossier racine au path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

class TestAppUI(unittest.TestCase):
    def setUp(self) -> None:
        # Mocker streamlit avant d'importer app
        self.st_mock = MagicMock()
        self.modules_patcher = patch.dict("sys.modules", {"streamlit": self.st_mock})
        self.modules_patcher.start()

    def tearDown(self) -> None:
        self.modules_patcher.stop()

    def test_app_import(self) -> None:
        # Test simple d'import pour vérifier que le code de haut niveau s'exécute
        # Attention : cela va exécuter tout le script app.py !
        # Il faut s'assurer que les effets de bord sont mockés.
        
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame") as mock_df, \
             patch("utils.csv_name", return_value="test.csv"):
            
            # Configurer les mocks streamlit
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False # Pas de clic par défaut
            
            # st.columns(4) doit retourner 4 mocks
            # Configurer streamlit mocks
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False # No click by default
            
            # st.columns(4) should return 4 mocks
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            # st.tabs doit retourner 4 mocks (car on a 4 tabs dans le code)
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Importer app (ou recharger si déjà importé)
            import app
            import importlib
            importlib.reload(app)
            
            # Vérifier que la config de page est appelée
            self.st_mock.set_page_config.assert_called()
            self.st_mock.title.assert_called_with("🐱 **FelisCrawler** 🐈")

    def test_app_scraping_click(self) -> None:
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame") as mock_df, \
             patch("utils.csv_name", return_value="test.csv"), \
             patch("pathlib.Path.exists", return_value=False): # Éviter les suppressions de fichiers réels
            
            # Simuler le clic sur le bouton
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = True
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Configurer le process mocké
            process_mock = MagicMock()
            process_mock.stdout = iter(["Crawled (200) <GET ...>", "Scraped from ..."])
            process_mock.returncode = 0
            process_mock.wait.return_value = None
            mock_popen.return_value = process_mock
            
            import app
            import importlib
            importlib.reload(app)
            
            # Vérifier que subprocess a été appelé
            mock_popen.assert_called()
            self.st_mock.success.assert_called()

    def test_app_visualization(self) -> None:
        # Créer un vrai DataFrame AVANT de mocker pandas
        import pandas as pd
        real_df = pd.DataFrame([{
            "Titre": "Test",
            "Profondeur": 1,
            "Paragraphes": 10,
            "Images": 2,
            "Longueur": 1000,
            "L'adresse": "http://test"
        }])

        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.read_text", return_value='[{"titre": "Test", "profondeur": 1, "nombre_paragraphes": 10, "nombre_images": 2, "longueur_contenu": 1000, "url": "http://test", "liens_internes": ["a"], "images": ["img.jpg"]}]'), \
             patch("pandas.DataFrame") as mock_df, \
             patch("utils.csv_name", return_value="test.csv"):
            
            # Configurer les mocks streamlit
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            
            def columns_side_effect(spec):
                if isinstance(spec, int):
                    return [MagicMock() for _ in range(spec)]
                else:
                    return [MagicMock() for _ in range(len(spec))]
            
            self.st_mock.columns.side_effect = columns_side_effect
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Configurer les inputs streamlit pour retourner des vraies valeurs
            self.st_mock.number_input.return_value = 0
            self.st_mock.multiselect.return_value = [1]
            
            def text_input_side_effect(label, *args, **kwargs):
                if "nom du fichier" in label.lower() or "json" in label.lower():
                    return "result.json"
                return ""
            self.st_mock.text_input.side_effect = text_input_side_effect
            self.st_mock.sidebar.text_input.return_value = "result.json"
            
            # Utiliser un vrai DataFrame pour éviter les problèmes de comparaison de mocks
            mock_df.return_value = real_df
            
            import app
            import importlib
            importlib.reload(app)
            
            # Vérifier que les données sont chargées
            self.st_mock.dataframe.assert_called()
            self.st_mock.metric.assert_called()
            self.st_mock.metric.assert_called()
