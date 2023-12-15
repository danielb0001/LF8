import unittest
import logging
import sys

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, stream=sys.stdout)

class HalloWelt:
    def __init__(self):
        self.message = 'Hallo Welt!'
        logging.info("Objekt erzeugt... {}".format(self.message))

class HalloWeltTestCase(unittest.TestCase):
    def test_passes_hallo_welt(self):
        logging.info("Test erfolgreich")
        hw = HalloWelt()
        self.assertEqual('Hallo Welt!', hw.message)

if __name__=='__main__':
    unittest.main()

