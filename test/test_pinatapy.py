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

    def test_remove_pin_from_ipfs(self):
        pass

    def test_pin_list(self):
        options = {
                "status": "pinned"
                }
        res = self.pinata.pin_list(options)
        self.assertIn("rows", res)

    def test_user_pinned_data_total(self):
        res = self.pinata.user_pinned_data_total()
        self.assertIn("pin_count", res)

if __name__ == "__main__":
    unittest.main()

