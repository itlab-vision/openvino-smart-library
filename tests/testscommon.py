import unittest
import sys

class CommonTestCase(unittest.TestCase):
    
    def test_check_python_major_version(self):
        self.assertGreaterEqual(sys.version_info.major, 3)
        
    def test_check_python_minor_version(self):
        self.assertGreaterEqual(sys.version_info.minor, 6)
        
if __name__ == '__main__':
    unittest.main()