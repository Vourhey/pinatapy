# -*- coding: utf-8 -*-

"""
Non-official Python library for Pinata.cloud
"""

import requests
from pathlib import Path

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

    """
    Options (optional):
    {
        "host_nodes": [
            "/ip4/host_node_1_external_IP/tcp/4001/ipfs/host_node_1_peer_id",
            "/ip4/host_node_2_external_IP/tcp/4001/ipfs/host_node_2_peer_id",
            .
            .
            .
        ],
        "pinataMetadata": {
            "name": (optional) - This is a custom name you can have for referencing your pinned content. This will be displayed in the Pin explorer "name" column if provided,
            "keyvalues": {
                "customKey": "customValue",
                "customKey2": "customValue2"
            }
        }
    }
    """
    def add_hash_to_pin_queue(self, hash_to_pin, options=None):
        url_suffix = "pinning/addHashToPinQueue"
        h = self.headers
        h["Content-Type"] = "application/json"
        body = {
                "hashToPin": hash_to_pin
                }

        if options is not None:
            if "host_nodes" in options:
                body["host_nodes"] = options["host_nodes"]
            if "pinataMetadata" in options:
                body["pinataMetadata"] = options["pinataMetadata"]

        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    # TODO
    # path_to_file may be a path to a directory. In this case pin_file_to_ipfs must pin files recursively
    def pin_file_to_ipfs(self, path_to_file, options=None):
        url_suffix = "pinning/pinFileToIPFS"
        if type(path_to_file) is str: path_to_file = Path(path_to_file)
        if path_to_file.is_dir():
            files = [("file",(str(file), open(file, "rb"))) for file in path_to_file.glob('**/*') if not file.is_dir()]
        else:
            files = {
                    "file": open(path_to_file, "rb")
                    }

        if options is not None:
            if "pinataMetadata" in options:
                files["pinataMetadata"] = options["pinataMetadata"]
            if "pinataOptions" in options:
                files["pinataOptions"] = options["pinataOptions"]

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

        if options is not None:
            if "host_nodes" in options:
                body["host_nodes"] = options["host_nodes"]
            if "pinataMetadata" in options:
                body["pinataMetadata"] = options["pinataMetadata"]

        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    """
    https://pinata.cloud/documentation#PinJobs
    """
    def pin_jobs(self, options=None):
        url_suffix = "pinning/pinJobs"

        payload = {}
        if options is not None:
            payload = options
        res = requests.get(self.__endpoint + url_suffix, params=payload, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def pin_json_to_ipfs(self, json_to_pin, options=None):
        url_suffix = "pinning/pinJSONToIPFS"
        h = self.headers
        h["Content-Type"] = "application/json"

        body = {
                "pinataContent": json_to_pin
                }

        if options is not None:
            if "pinataMetadata" in options:
                body["pinataMetadata"] = options["pinataMetadata"]
            if "pinataOptions" in options:
                body["pinataOptions"] = options["pinataOptions"]

        res = requests.post(self.__endpoint + url_suffix, json=body, headers=h)

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

    """
    https://pinata.cloud/documentation#PinList
    """
    def pin_list(self, options=None):
        url_suffix = "data/pinList"

        payload = {}
        if options is not None:
            payload = options
        res = requests.get(self.__endpoint + url_suffix, params=payload, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

    def user_pinned_data_total(self):
        url_suffix = "data/userPinnedDataTotal"

        res = requests.get(self.__endpoint + url_suffix, headers=self.headers)

        if res.status_code == 200:
            return res.json()

        return self.__error(res)

