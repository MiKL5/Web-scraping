import sys
import unittest
import os
from   pathlib  import Path


def run_all_tests() -> None:
    # Ajouter le répertoire racine du projet au sys.path
    project_root = Path(__file__).parent.parent.resolve()
    sys.path.append(str(project_root))

    # Découvrir et exécuter les tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / "tests"
    suite = loader.discover(str(start_dir), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    if "--live" in sys.argv:
        os.environ["RUN_LIVE_TESTS"] = "1"
        sys.argv.remove("--live")
    run_all_tests()