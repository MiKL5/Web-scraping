# **Tests de FelisCrawler**
## **Vue d'ensemble**
FelisCrawler dispose d'une **suite de tests complète** garantissant la pérennité du scraper face aux évolutions de Wikipédia.
**Statistiques**
* **51 tests** au total
* **100%** de couverture de code
* **100%** de taux de réussite
* **1 test** désactivé par défaut (live test)
**Technologies**
* `unittest` 👉 Framework de tests Python
* `pytest` 👉 Lanceur et plugin de couverture
* `pytest-cov` 👉 Mesure de couverture
* `unittest.mock` 👉 Mocking pour isolation
___
## **Installation**
### **Installer les dépendances de test**
```bash
pip install -r requirements.txt
```
Les dépendances de test incluses :
```bash
pytest>=7.0.0
pytest-cov>=4.0.0
```
___
## **Lancer les tests**
### **Commande de base**
```bash
# Tous les tests (sauf live)
python run_tests.py

# Avec verbosité
python run_tests.py -v
```
### **Tests avec couverture**
```bash
# Couverture complète
pytest --cov=. --cov-report=term-missing

# Couverture HTML (navigable)
pytest --cov=. --cov-report=html
open htmlcov/index.html  # macOS
```
### **Tests live (réseau requis)**
```bash
# Inclure les tests live
python run_tests.py --live
```
### **Tests par catégorie**
```bash
# Tests d'intégrité uniquement
python -m unittest tests.test_integrity

# Tests de structure
python -m unittest tests.test_structure

# Tests UI
python -m unittest tests.test_app_ui

# Test spécifique
python -m unittest tests.test_integrity.TestfeliscrawlerSpiderIntegrity.test_parse_page_integrity
```
___
## **Types de tests**
### **1. Tests d'intégrité** (`test_integrity.py`)
#### **Objectif** : Vérifier que le spider extrait tous les champs avec les bons types
#### **Ce qui est testé**  
✅ Présence de tous les champs requis (`titre`, `url`, `profondeur`, etc.)  
✅ Types de données corrects (string, int, list)  
✅ Valeurs non nulles pour champs critiques  
✅ Format des URLs  
✅ Méthode `parse_start_url` (🆕 v2.0)

<details>
<summary>Exemple de test</summary>

```python
def test_parse_page_integrity(self) -> None:
    """Vérifie que tous les champs sont présents et bien typés."""
    response = # ... création d'une réponse mock
    results = list(self.spider.parse_page(response))
    
    item = results[0]
    self.assertIsInstance(item['titre'], str)
    self.assertIsInstance(item['profondeur'], int)
    # ...
```

</details>
<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_integrity
```

</details>

___
### **2. Tests de structure HTML** (`test_structure.py`)
#### **Objectif** 👉 Détecter les changements de structure HTML de Wikipédia  
⚠️ **Attention** 👉 Il effectue un **crawl en direct** sur Wikipedia à chaque lancement

#### **Ce qui est testé**  
✅ Titre extrait correctement  
✅ Paragraphes trouvés (> 0)  
✅ Images détectées  
✅ Liens internes présents  
✅ Sélecteurs XPath/CSS fonctionnels

#### **Pourquoi c'est important** 👉 Si Wikipédia change sa structure HTML, ce test échoue immédiatement  

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_structure
```

</details>
<details>
<summary>Exemple d'output</summary>

```
[SUCCESS] Live structure test passed for https://fr.wikipedia.org/wiki/Chat
  - Title found: Chat
  - Paragraphs: 142
  - Images: 38
```

</details>

___
### **3. Tests de structure live** (`test_live_structure.py`)
**Objectif** 👉 Identique à `test_structure.py` mais **désactivé par défaut**  
**Différence** 👉 Nécessite le flag `--live` pour s'exécuter  
**Utilité** 👉 Tests optionnels nécessitant une connexion internet  
**Commande**
```bash
python run_tests.py --live
```
___
**Décorateur utilisé**
```python
@unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS"), 
                     "Tests live désactivés par défaut")
```
___
### **4. Tests de cas limites** (`test_edge_cases.py`)
**Objectif** 👉 Simuler des pages problématiques  
**Scénarios testés**  
❌ le titre manquant (`<h1>` absent)  
❌ Le contenu vide (aucun paragraphe)  
❌ L'URL mal formée  
❌ L'encodage spécial

<details>
<summary>Exemple de test</summary>

```python
def test_missing_title(self) -> None:
    """Tester le comportement quand le titre h1 est manquant."""
    html = "<html><body><p>Pas de titre</p></body></html>"
    # Vérifier que le fallback fonctionne
    self.assertEqual(item['titre'], "Je n'ai pas trouvé le titre")
```
</details>

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_edge_cases
```

</details><hr>

### **5. Tests de navigation** (`test_navigation.py`)
**Objectif** 👉 Valider les règles de filtrage des liens  
**Ce qui est testé**  
✅ Les liens pertinents acceptés (`/wiki/Chat`, `/wiki/Félin`)  
❌ Les liens exclus (`/wiki/Fichier:`, `/wiki/Spécial:`)  
✅ Les règles regex correctes  
✅ Le link extractor configuré

<details>
<summary>Exemple de test</summary>

```python
def test_allowed_links(self) -> None:
    """Teste que les liens pertinents sont extraits."""
    response = # ... mock avec liens
    links = self.link_extractor.extract_links(response)
    # Vérifier que /wiki/Chat est extrait
```
</details>

<details>
<summary>Commande</summary>


```bash
python -m unittest tests.test_navigation
```

</details><hr>


### **6. Tests end-to-end** (`test_e2e.py`)
**Objectif** 👉 Tester le spider en conditions réelles (subprocess)  
**Ce qui est testé**  
✅ Le lancement du spider via `scrapy runspider`  
✅ La génération du fichier JSON  
✅ Le format du JSON valide  
✅ Le code de sortie = 0

**Particularité** : Utilise `subprocess.Popen` pour lancer Scrapy  

<details>
<summary>Exemple de test</summary>

```python
def test_e2e_scraping(self) -> None:
    """Teste le spider en lançant un vrai subprocess."""
    cmd = ["scrapy", "runspider", "wikipedia/spiders/feliscrawler_spider.py", ...]
    process = subprocess.Popen(cmd, ...)
    # Vérifier génération du fichier
```
</details>

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_e2e
```

</details><hr>

### **7. Tests UI Streamlit** (`test_app_ui.py`)
**Objectif** 👉 Tester l'interface Streamlit sans lancer l'app  
**Techniques utilisées**
* **Mocking complet** de Streamlit
* **Importation dynamique** de `app.py`
* **Mock de pandas.DataFrame** pour éviter les effets de bord

**Ce qui est testé**  
✅ L'import de `app.py` sans erreur  
✅ La configuration de page appelée  
✅ Le bouton de scraping fonctionnel  
✅ Les visualisations chargées  
✅ Le filtrage des données  
✅ La gestion d'erreurs (codes retour, FileNotFoundError, JSON invalide) 🆕  
✅ Le nettoyage fichiers avant scraping 🆕  
✅ L'état scraping actif 🆕  
✅ Le filtrage par recherche textuelle 🆕

<details>
<summary>Exemple</summary>

```python
def test_app_import(self) -> None:
    with patch("streamlit") as st_mock:
        import app
        st_mock.set_page_config.assert_called()
```
</details>
<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_app_ui
```

</details>

___
### **8. Tests des composants UI** (`test_components.py`)
**Objectif** 👉 Tester les composants Streamlit isolément  

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_components
```

</details>

___
### **9. Tests de configuration** (`test_settings.py`)
**Objectif** 👉 Vérifier les paramètres Scrapy  
**Ce qui est testé**  
✅ `DEPTH_LIMIT` défini  
✅ `ROBOTSTXT_OBEY=True`  
✅ User-Agent configuré

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_settings
```

</details>

___
### **10. Tests utilitaires** (`test_utils.py`)
**Objectif** 👉 Tester les fonctions helper  
**Exemple**  👉 Fonction `csv_name()`
```python
def test_csv_name_json(self) -> None:
    """Teste la conversion .json -> .csv"""
    self.assertEqual(csv_name("data.json"), "data.csv")
```
**Commande**
```bash
python -m unittest tests.test_utils
```
___
### **11. Tests middlewares** (`test_middlewares.py`) 🆕
**Objectif** 👉 Tester les middlewares Scrapy  
**Ce qui est testé**  
✅ `process_spider_output` yield correctement  
✅ `process_spider_exception` retourne None  
✅ `process_exception` (downloader) retourne None

<details>
<summary>Commande</summary>

```bash
python -m unittest tests.test_middlewares
```

</details>

___
## **📈 Couverture de code**
### **État actuel**
```
Name                                       Stmts   Miss  Cover    Missing
---------------------------------------------------------------------------
app.py                                       247      0   100%
utils.py                                       7      0   100%
wikipedia/__init__.py                          0      0   100%
wikipedia/items.py                             3      0   100%
wikipedia/middlewares.py                      34      0   100%
wikipedia/pipelines.py                         6      0   100%
wikipedia/settings.py                         11      0   100%
wikipedia/spiders/__init__.py                  0      0   100%
wikipedia/spiders/feliscrawler_spider.py      25      0   100%
---------------------------------------------------------------------------
TOTAL                                        333      0   100%   ✅ PARFAIT
```
### **Générer le rapport HTML**
```bash
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m
coverage html
open     htmlcov/index.html
```
### **Les objectifs**
✅ **Atteint**        👉 100% global  
✅ **100% sur**       👉 Tout le projet !
___

<details>
<summary>Écrire de nouveaux tests</summary>

### **Structure d'un test**
```python
import unittest
from pathlib import Path
import sys

# Ajouter le projet au path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from wikipedia.spiders.feliscrawler_spider import feliscrawlerSpider

class TestNouveauTest(unittest.TestCase):
    def setUp(self) -> None:
        """Exécuté avant chaque test."""
        self.spider = feliscrawlerSpider()
    
    def test_ma_fonctionnalite(self) -> None:
        """Description claire du test."""
        # Arrange
        expected = "valeur attendue"
        
        # Act
        result = self.spider.ma_methode()
        
        # Assert
        self.assertEqual(result, expected)
    
    def tearDown(self) -> None:
        """Exécuté après chaque test."""
        pass

if __name__ == '__main__':
    unittest.main()
```
### **Bonnes pratiques**
1. **Naming**           👉 `test_<ce_qui_est_testé>`
2. **Docstrings**       👉 Toujours décrire le test
3. **Isolation**        👉 Un test = une assertion principale
4. **Mock**             👉 Isoler les dépendances externes
5. **Reproductibilité** 👉 Pas de dépendance temporelle
### **Assertions communes**
```python
# Égalité
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Type
self.assertIsInstance(obj, type)

# Booléens
self.assertTrue(condition)
self.assertFalse(condition)

# Nullité
self.assertIsNone(obj)
self.assertIsNotNone(obj)

# Collections
self.assertIn(item, collection)
self.assertGreater(a, b)

# Exceptions
with self.assertRaises(ValueError):
    fonction_qui_doit_echouer()
```

</details>

___

<details>
<summary>CI/CD</summary>

### **Configuration GitHub Actions (exemple)**
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python run_tests.py
    
    - name: Coverage
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

</details>

___
## **🔧 Troubleshooting**
### **Les tests échouent**
#### **Problème** 👉 `ModuleNotFoundError`
```bash
# Solution
pip install -r requirements.txt
```
#### **Problème** 👉 `test_structure.py` échoue
```bash
# Cause probable : Wikipedia a changé sa structure HTML
# Vérifier les sélecteurs XPath dans feliscrawler_spider.py
```
#### **Problème** 👉 Tests UI échouent avec erreur pandas
```bash
# Solution : Vérifier que numpy est compatible
pip install --upgrade pandas numpy
```
### **Les tests live ne s'exécutent pas**
```bash
# S'assurer d'utiliser le flag --live
python run_tests.py --live

# Vérifier la connexion internet
ping fr.wikipedia.org
```
___
## **📚 Ressources**
[unittest Documentation](https://docs.python.org/3/library/unittest.html)  
[pytest Documentation](https://docs.pytest.org/)  
[Scrapy Testing](https://docs.scrapy.org/en/latest/topics/testing.html)  
[Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

<!-- <hr><div align="center">

**Dernière mise à jour** : 2025-11-26   -->
<!-- **Version** : 1.0 -->