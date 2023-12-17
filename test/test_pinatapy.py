import unittest
import os

from pinatapy import PinataPy


class TestPinataPy(unittest.TestCase):
    def setUp(self) -> None:
        api_key = os.environ.get("PINATA_API_KEY")
        secret_key = os.environ.get("PINATA_SECRET_API_KEY")
        if api_key and secret_key:
            self.pinata = PinataPy(api_key, secret_key)
        else:
            raise ValueError("No API keys in environment variables")

    def test_remove_pin_from_ipfs(self) -> None:
        pass

    def test_pin_list(self) -> None:
        options = {"status": "pinned"}
        res = self.pinata.pin_list(options)
        self.assertIn("rows", res)

    def test_user_pinned_data_total(self) -> None:
        res = self.pinata.user_pinned_data_total()
        self.assertIn("pin_count", res)
    
    def test_generate_admin_api_key(self) -> None:
        res = self.pinata.generate_api_key(key_name="test_admin_key", is_admin=True)
        self.assertIn("pinata_api_key", res)

    def test_generate_api_key_exception(self) -> None:
        with self.assertRaises(Exception) as exception_context:
            self.pinata.generate_api_key(key_name="test_key", is_admin=False, options={"maxUses": 1})
        self.assertEqual(
            str(exception_context.exception),
            "Setting permissions is necessary! Check https://docs.pinata.cloud/reference/post_users-generateapikey"
        )
    
    def test_generate_api_key_with_permissions(self) -> None:
        res = self.pinata.generate_api_key(key_name="test_key_with_permissions", is_admin=False, options={"permissions": {"endpoints": {"pinning": {"pinFileToIPFS": True, "unpin": True}}}})
        self.assertIn("pinata_api_key", res)

if __name__ == "__main__":
    unittest.main()
