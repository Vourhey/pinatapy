# -*- coding: utf-8 -*-

"""
Non-official Python library for Pinata.cloud
"""

import requests


class PinataPy:
    __endpoint = "https://api.pinata.cloud/"

    def __init__(self, pinata_api_key, pinata_secret_api_key):
        self.API_KEY = pinata_api_key
        self.SECRET_KEY = pinata_secret_api_key

        self.headers = {
                "pinata_api_key": self.API_KEY,
                "pinata_secret_api_key": self.SECRET_KEY
                }

    def __error(self, code: int) -> dict:
        return {
                "message": "Response status {}".format(code)
                }

    def test_authentication(self) -> dict:
        url_suffix = "data/testAuthentication"
        res = requests.get(__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        r = {
                "message": "Response status {}".format(res.status_code)
                }
        return self.__error(r.status_code)

    def add_hash_to_pin_queue(self, hash_to_pin, options=None):
        url_suffix = "pinning/addHashToPinQueue"
        res = requests.post(__endpoint + url_suffix, data=body, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(r.status_code)

    def pin_file_to_ipfs(self, path_to_file, options=None):
        url_suffix = "k"
        pass

    def pin_hash_to_ipfs(self, hash_to_pin, options=None):
        pass

    def pin_jobs(self, options=None):
        pass

    def pin_json_to_ipfs(self, json_to_pin, options=None):
        pass

    def remove_pin_from_ipfs(self, hash_to_remove, options=None):
        pass

    def pin_list(self, options=None):
        pass

    def user_pinned_data_total(self):
        pass
