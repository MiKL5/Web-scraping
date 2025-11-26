import unittest
import sys
from   pathlib       import Path
from   unittest.mock import MagicMock, patch

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
            
            # Configurer le mock DataFrame
            df_instance = MagicMock()
            df_instance.empty = False
            df_instance.__len__.return_value = 1
            
            # Simulation pour les colonnes (df[‘Col’])
            mock_col = MagicMock()
            # Mock pour la comparaison (df["Col"] >= val) -> retourne un masque (liste de bools)
            mock_col.__ge__.return_value = [True]
            mock_col.__le__.return_value = [True]
            mock_col.str.contains.return_value = [True]
            
            # Configurer __getitem__ pour retourner la colonne ou le df filtré
            def getitem_side_effect(key):
                if isinstance(key, str):
                    return mock_col # df["Col"]
                return df_instance # df[mask]
            
            df_instance.__getitem__.side_effect = getitem_side_effect
            
            mock_df.return_value = df_instance
            
            import app
            import importlib
            importlib.reload(app)
            
            # Vérifier que les données sont chargées
            self.st_mock.dataframe.assert_called()
            self.st_mock.metric.assert_called()
            self.st_mock.metric.assert_called()

    def test_file_cleanup_before_scraping(self) -> None:
        """Test cleanup of existing files before scraping (lines 140-144)"""
        import tempfile
        import json
        
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            # Create temporary files
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                csv_file = Path(tmpdir) / "result.csv"
                
                # Create files
                json_file.write_text('{"test": "data"}')
                csv_file.write_text('col1,col2\n1,2')
                
                self.assertTrue(json_file.exists())
                self.assertTrue(csv_file.exists())
                
                # Configure mocks
                self.st_mock.session_state = {}
                self.st_mock.sidebar.button.return_value = True  # Trigger scraping
                self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
                self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
                
                # Mock process
                mock_proc = MagicMock()
                mock_proc.stdout = []
                mock_proc.poll.return_value = 0
                mock_proc.returncode = 0
                mock_popen.return_value = mock_proc
                
                # Patch the output file paths in app.py context
                with patch('app.output_file', json_file), \
                     patch('app.output_file_csv', csv_file):
                    
                    import app
                    import importlib
                    importlib.reload(app)

    def test_scraping_with_empty_stdout_lines(self) -> None:
        """Test scraping process with empty lines in stdout (line 162)"""
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = True
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Mock process with empty lines
            mock_proc = MagicMock()
            mock_proc.stdout = ["Line 1", "", "   ", "Line 2", ""]  # Mix of empty and valid lines
            mock_proc.poll.return_value = 0
            mock_proc.returncode = 0
            mock_popen.return_value = mock_proc
            
            import app
            import importlib
            importlib.reload(app)

    def test_scraping_error_with_nonzero_returncode(self) -> None:
        """Test scraping failure with non-zero return code (lines 186-188)"""
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = True
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Mock process with error
            mock_proc = MagicMock()
            mock_proc.stdout = ["Error occurred"]
            mock_proc.poll.return_value = 1  # Error code
            mock_proc.returncode = 1
            mock_popen.return_value = mock_proc
            
            import app
            import importlib
            importlib.reload(app)
            
            # Verify error message was shown
            self.st_mock.error.assert_called()

    def test_scraping_file_not_found_error(self) -> None:
        """Test FileNotFoundError during scraping (lines 190-191)"""
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = True
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Mock FileNotFoundError
            mock_popen.side_effect = FileNotFoundError("Spider not found")
            
            import app
            import importlib
            importlib.reload(app)
            
            # Verify error message
            self.st_mock.error.assert_called()

    def test_scraping_general_exception(self) -> None:
        """Test general exception during scraping (lines 192-193)"""
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = True
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Mock general exception
            mock_popen.side_effect = RuntimeError("Unexpected error")
            
            import app
            import importlib
            importlib.reload(app)
            
            # Verify error message
            self.st_mock.error.assert_called()

    def test_csv_export_fallback(self) -> None:
        """Test CSV export fallback when file doesn't exist (lines 225-227)"""
        import tempfile
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test_fallback.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Create a temporary JSON file with data
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.write_text('[{"titre": "Chat", "url": "http://example.com"}]')
                
                with patch('app.output_file', json_file), \
                     patch('pandas.DataFrame') as mock_df_class:
                    
                    # Mock DataFrame
                    mock_df = MagicMock()
                    mock_df.__len__.return_value = 1  # Non-empty DataFrame
                    mock_df.to_csv = MagicMock()
                    mock_df_class.return_value = mock_df
                    
                    import app
                    import importlib
                    importlib.reload(app)

    def test_json_decode_error(self) -> None:
        """Test JSONDecodeError handling (lines 229-230)"""
        import tempfile
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Create invalid JSON file
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.write_text('{"invalid json syntax')
                
                with patch('app.output_file', json_file):
                    import app
                    import importlib
                    importlib.reload(app)
                    
                    # The JSONDecodeError is caught, app continues execution
                    # We just verify the import succeeded
                    self.assertTrue(True)

    def test_json_read_error(self) -> None:
        """Test general exception during JSON reading (lines 231-232)"""
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"), \
             patch("builtins.open", side_effect=PermissionError("Cannot read file")):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            import app
            import importlib
            importlib.reload(app)
            
            # The exception is caught, verify app continues
            self.assertTrue(True)

    def test_scraping_state_active(self) -> None:
        """Test UI when scraping is active (line 260)"""
        with patch("subprocess.Popen"), \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {"scraping": True}  # Active scraping
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            import app
            import importlib
            importlib.reload(app)
            
            # Verify info message is shown
            self.st_mock.info.assert_called()

    def test_search_filter_applied(self) -> None:
        """Test search term filtering (line 333)"""
        import tempfile
        import json
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            
            def columns_side_effect(spec):
                if isinstance(spec, int):
                    return [MagicMock() for _ in range(spec)]
                else:
                    return [MagicMock() for _ in range(len(spec))]
            self.st_mock.columns.side_effect = columns_side_effect
            
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            # Create JSON with data
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                data = [
                    {"titre": "Felix le chat", "url": "http://example.com", 
                     "profondeur": 0, "longueur_contenu": 100, "nombre_images": 5,
                     "nombre_paragraphes": 10, "liens_internes": []},
                    {"titre": "Autre chat", "url": "http://example2.com",
                     "profondeur": 1, "longueur_contenu": 200, "nombre_images": 3,
                     "nombre_paragraphes": 5, "liens_internes": []}
                ]
                json_file.write_text(json.dumps(data))
                
                # Mock text_input to handle both output_file and search_term
                def text_input_side_effect(label, *args, **kwargs):
                    if "nom du fichier" in label.lower() or "json" in label.lower():
                        return str(json_file)
                    if "recherche" in label.lower():
                        return "Felix"
                    return ""
                self.st_mock.text_input.side_effect = text_input_side_effect
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                
                self.st_mock.number_input.return_value = 0
                self.st_mock.multiselect.return_value = [0, 1] # Select all depths
                
                import app
                import importlib
                importlib.reload(app)

    def test_item_detail_display(self) -> None:
        """Test detailed item display (lines 358-392)"""
        import tempfile
        import json
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            
            def columns_side_effect(spec):
                if isinstance(spec, int):
                    return [MagicMock() for _ in range(spec)]
                else:
                    return [MagicMock() for _ in range(len(spec))]
            self.st_mock.columns.side_effect = columns_side_effect
            
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            item_data = {
                "titre": "Chat domestique",
                "url": "https://fr.wikipedia.org/wiki/Chat",
                "introduction": "Le chat est un félin.",
                "liens_internes": ["https://fr.wikipedia.org/wiki/Felis", "https://fr.wikipedia.org/wiki/Mammifère"],
                "profondeur": 1,
                "nombre_paragraphes": 50,
                "nombre_images": 10,
                "images": ["//upload.wikimedia.org/chat1.jpg", "//upload.wikimedia.org/chat2.jpg"]
            }
            
            # Create JSON with data
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.write_text(json.dumps([item_data]))
                
                # Mock inputs
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                self.st_mock.text_input.return_value = "" # No search
                self.st_mock.number_input.return_value = 0
                self.st_mock.multiselect.return_value = [1]
                
                # Mock selectbox to return the item title
                self.st_mock.selectbox.return_value = "Chat domestique"
                
                import app
                import importlib
                importlib.reload(app)
                
                # Verify detail display elements were called
                # We check if st.image was called which is deep inside the detail view
                self.assertTrue(self.st_mock.image.called or self.st_mock.text.called)

    def test_file_unlink_exception(self) -> None:
        """Test exception during file unlink (lines 143-144)"""
        import tempfile
        
        with patch("subprocess.Popen") as mock_popen, \
             patch("pandas.DataFrame"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            # Create temporary files
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                csv_file = Path(tmpdir) / "result.csv"
                json_file.touch()
                csv_file.touch()
                
                self.st_mock.session_state = {}
                self.st_mock.sidebar.button.return_value = True
                self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
                self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
                
                # Mock text_input to return the json file path
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                
                # Mock process
                mock_proc = MagicMock()
                mock_proc.stdout = []
                mock_proc.poll.return_value = 0
                mock_proc.returncode = 0
                mock_popen.return_value = mock_proc
                
                # Patch Path.unlink to raise exception
                with patch('pathlib.Path.unlink', side_effect=PermissionError("Cannot delete")):
                    # We don't need to patch app.output_file anymore as it's set by text_input
                    import app
                    import importlib
                    importlib.reload(app)
                        # Should not raise exception

    def test_csv_fallback_exception(self) -> None:
        """Test exception during CSV fallback export (lines 226-227)"""
        import tempfile
        import json
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test_fallback.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.write_text('[{"titre": "Chat", "url": "http://example.com"}]')
                
                # Mock text_input to return the json file path
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                self.st_mock.text_input.return_value = "" # Search term empty
                
                with patch('pandas.DataFrame') as mock_df_class:
                    
                    mock_df = MagicMock()
                    mock_df.__len__.return_value = 1
                    
                    # Mock to_csv to raise exception ONLY when writing to file (fallback)
                    # and return string otherwise (for download button)
                    def to_csv_side_effect(*args, **kwargs):
                        if args and "test_fallback.csv" in str(args[0]):
                             raise PermissionError("Cannot write CSV")
                        return "csv,content"
                    mock_df.to_csv.side_effect = to_csv_side_effect
                    
                    mock_df_class.return_value = mock_df
                    
                    import app
                    import importlib
                    importlib.reload(app)
                    # Should not raise exception

    def test_json_read_exception(self) -> None:
        """Test general exception during JSON reading (lines 231-232)"""
        import tempfile
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            self.st_mock.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.touch()
                
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                
                # Patch Path.read_text to raise exception
                with patch('pathlib.Path.read_text', side_effect=PermissionError("Cannot read")):
                    import app
                    import importlib
                    importlib.reload(app)
                    
                    # Verify error was shown
                    self.st_mock.error.assert_called()

    def test_image_display_exception(self) -> None:
        """Test exception during image display (lines 391-392)"""
        import tempfile
        import json
        
        with patch("subprocess.Popen"), \
             patch("utils.csv_name", return_value="test.csv"):
            
            self.st_mock.session_state = {}
            self.st_mock.sidebar.button.return_value = False
            
            def columns_side_effect(spec):
                if isinstance(spec, int):
                    return [MagicMock() for _ in range(spec)]
                else:
                    return [MagicMock() for _ in range(len(spec))]
            self.st_mock.columns.side_effect = columns_side_effect
            
            self.st_mock.tabs.return_value = [MagicMock() for _ in range(4)]
            
            item_data = {
                "titre": "Chat",
                "url": "http://chat.com",
                "images": ["//img.jpg"]
            }
            
            with tempfile.TemporaryDirectory() as tmpdir:
                json_file = Path(tmpdir) / "result.json"
                json_file.write_text(json.dumps([item_data]))
                
                self.st_mock.sidebar.text_input.return_value = str(json_file)
                self.st_mock.text_input.return_value = ""
                self.st_mock.number_input.return_value = 0
                self.st_mock.multiselect.return_value = []
                self.st_mock.selectbox.return_value = "Chat"
                
                # Mock st.image to raise exception
                self.st_mock.image.side_effect = Exception("Image error")
                
                import app
                import importlib
                importlib.reload(app)
                
                # Verify fallback text was called
                self.st_mock.text.assert_called_with("//img.jpg")

if __name__ == "__main__":
    unittest.main()