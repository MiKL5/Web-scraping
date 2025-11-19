import unittest
from pathlib import Path
import sys
import subprocess
import json
import tempfile

class TestEndToEnd(unittest.TestCase):
    def test_run_spider_process(self):
        """
        Exécute le spider en tant que sous-processus (comme le fait app.py) et vérifie qu'il produit un JSON valide.
        Nous limitons le crawl à 1 élément pour être rapide.
        """
        project_root = Path(__file__).resolve().parents[1]
        spider_path = project_root / 'wikipedia' / 'spiders' / 'feliscrawler_spider.py'
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_json:
            output_file = Path(tmp_json.name)
            
        # S'assurer que le fichier est fermé avant que Scrapy n'écrive dedans
        
        cmd = [
            "scrapy", "runspider", str(spider_path),
            "-O", str(output_file),
            "-s", "DEPTH_LIMIT=1",
            "-s", "CLOSESPIDER_PAGECOUNT=1", # Arrêter après 1 page
            "-s", "LOG_LEVEL=ERROR" # Garder la sortie propre
        ]
        
        try:
            # Lancer le spider
            result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                self.fail(f"Spider failed with return code {result.returncode}.\nStderr: {result.stderr}")
            
            # Vérifier si le fichier existe et a du contenu
            self.assertTrue(output_file.exists(), "Output JSON file was not created")
            
            content = output_file.read_text(encoding='utf-8')
                
            self.assertTrue(len(content) > 0, "Output JSON file is empty")
            
            try:
                data = json.loads(content)
                self.assertIsInstance(data, list, "JSON root should be a list")
                self.assertGreater(len(data), 0, "JSON list should not be empty")
                
                first_item = data[0]
                self.assertIn('titre', first_item)
                self.assertIn('url', first_item)
                # On s'attend à ce que la page 'Chat' soit l'url de départ, donc le titre doit être 'Chat'
                self.assertEqual(first_item['titre'], 'Chat')
                
            except json.JSONDecodeError:
                self.fail(f"Invalid JSON produced: {content}")
                
        finally:
            # Nettoyer
            if output_file.exists():
                output_file.unlink()

if __name__ == '__main__':
    unittest.main()
