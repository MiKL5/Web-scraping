import unittest
import os
import sys

def run_all_tests():
    # Set up the path to include the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(project_root)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)

if __name__ == '__main__':
    run_all_tests()
