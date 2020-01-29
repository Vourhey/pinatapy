import unittest
import os

from pinatapy import PinataPy


class TestPinataPy(unittest.TestCase):

    def setUp(self):
        self.PINATA_API_KEY = os.environ.get("PINATA_API_KEY")
        self.PINATA_SECRET_API_KEY = os.environ.get("PINATA_SECRET_API_KEY")
        self.pinata = PinataPy(self.PINATA_API_KEY, self.PINATA_SECRET_API_KEY)

    def test_test_authentication(self):
        response = self.pinata.test_authentication()
        expected = {
                "message": "Congratulations! You are communicating with the Pinata API!"
                }

        self.assertEqual(response, expected)

if __name__ == "__main__":
    unittest.main()

