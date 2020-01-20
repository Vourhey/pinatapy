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

    def __error(self, res) -> dict:
        return {
                "status": res.status_code,
                "reason": res.reason,
                "text": res.text
                }

    def test_authentication(self) -> dict:
        url_suffix = "data/testAuthentication"
        res = requests.get(self.__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def add_hash_to_pin_queue(self, hash_to_pin, options=None):
        url_suffix = "pinning/addHashToPinQueue"
        h = self.headers
        h["Content-Type"] = "application/json"
        body = {
                "hashToPin": hash_to_pin
                }

        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def pin_file_to_ipfs(self, path_to_file, options=None):
        url_suffix = "pinning/pinFileToIPFS"

        files = {
                "file": open(path_to_file, "rb")
                }
        res = requests.post(self.__endpoint + url_suffix, files=files, headers=self.headers)

        if  res.status_code == 200:
            return res.json()

        return self.__error(res)

    def pin_hash_to_ipfs(self, hash_to_pin, options=None):
        url_suffix = "pinning/pinHashToIPFS"
        h = self.headers
        h["Content-Type"] = "application/json"

        body = {
                "hashToPin": hash_to_pin
                }
        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def pin_jobs(self, options=None):
        url_suffix = "pinning/pinJobs"

        res = requests.get(self.__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def pin_json_to_ipfs(self, json_to_pin, options=None):
        url_suffix = "pinning/pinJSONToIPFS"
        h = self.headers
        h["Content-Type"] = "application/json"

        res = requests.post(self.__endpoint + url_suffix, json=json_to_pin, headers=h)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def remove_pin_from_ipfs(self, hash_to_remove, options=None):
        url_suffix = "pinning/removePinFromIPFS"
        h = self.headers
        h["Content-Type"] = "application/json"

        body = {
                "ipfs_pin_hash": hash_to_remove
                }

        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

        if res.status_code == 200:
            return {"message": "Removed"}

        return self.__error(res)

    def pin_list(self, options=None):
        url_suffix = "data/pinList"

        res = requests.get(self.__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def user_pinned_data_total(self):
        url_suffix = "data/userPinnedDataTotal"

        res = requests.get(self.__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

