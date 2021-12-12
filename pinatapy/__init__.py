"""Non-official Python library for Pinata.cloud"""

import os
import typing as tp

import requests

# Custom tpe hints
ResponsePayload = tp.Dict[str, tp.Any]
OptionsDict = tp.Dict[str, tp.Any]
Headers = tp.Dict[str, str]

# global constants
API_ENDPOINT: str = "https://api.pinata.cloud/"


class PinataPy:
    """A pinata api client session object"""

    def __init__(self, pinata_api_key: str, pinata_secret_api_key: str) -> None:
        self._auth_headers: Headers = {
            "pinata_api_key": pinata_api_key,
            "pinata_secret_api_key": pinata_secret_api_key,
        }

    @staticmethod
    def _error(response: requests.Response) -> ResponsePayload:
        """Construct dict from response if an error has occurred"""
        return {"status": response.status_code, "reason": response.reason, "text": response.text}

    def pin_file_to_ipfs(self, path_to_file: str, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """
        Pin any file, or directory, to Pinata's IPFS nodes

        More: https://docs.pinata.cloud/api-pinning/pin-file
        """
        url: str = API_ENDPOINT + "pinning/pinFileToIPFS"
        headers: Headers = self._auth_headers

        def get_all_files(directory: str) -> tp.List[str]:
            """get a list of absolute paths to every file located in the directory"""
            paths: tp.List[str] = []
            for root, dirs, files_ in os.walk(os.path.abspath(directory)):
                for file in files_:
                    paths.append(os.path.join(root, file))
            return paths

        files: tp.Dict[str, tp.Any]

        if os.path.isdir(path_to_file):
            all_files: tp.List[str] = get_all_files(path_to_file)
            files = {"file": [(file, open(file, "rb")) for file in all_files]}
        else:
            files = {"file": open(path_to_file, "rb")}

        if options is not None:
            if "pinataMetadata" in options:
                headers["pinataMetadata"] = options["pinataMetadata"]
            if "pinataOptions" in options:
                headers["pinataOptions"] = options["pinataOptions"]
        response: requests.Response = requests.post(url=url, files=files, headers=headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def pin_hash_to_ipfs(self, hash_to_pin: str, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """WARNING: This Pinata API method is deprecated. Use 'pin_hash_to_ipfs' instead"""
        url: str = API_ENDPOINT + "pinning/addHashToPinQueue"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        body = {"hashToPin": hash_to_pin}
        if options is not None:
            if "host_nodes" in options:
                body["host_nodes"] = options["host_nodes"]
            if "pinataMetadata" in options:
                body["pinataMetadata"] = options["pinataMetadata"]
        response: requests.Response = requests.post(url=url, json=body, headers=headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def pin_to_pinata_using_ipfs_hash(self, ipfs_hash: str, filename: str) -> ResponsePayload:
        """
        Pin file to Pinata using its IPFS hash

        https://docs.pinata.cloud/api-pinning/pin-by-hash
        """
        payload: OptionsDict = {"pinataMetadata": {"name": filename}, "hashToPin": ipfs_hash}
        url: str = API_ENDPOINT + "/pinning/pinByHash"
        response: requests.Response = requests.post(url=url, json=payload, headers=self._auth_headers)
        return self._error(response) if not response.ok else response.json()  # type: ignore

    def pin_jobs(self, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """
        Retrieves a list of all the pins that are currently in the pin queue for your user.

        More: https://docs.pinata.cloud/api-pinning/pin-jobs
        """
        url: str = API_ENDPOINT + "pinning/pinJobs"
        payload: OptionsDict = options if options else {}
        response: requests.Response = requests.get(url=url, params=payload, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def pin_json_to_ipfs(self, json_to_pin: tp.Any, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """pin provided JSON"""
        url: str = API_ENDPOINT + "pinning/pinJSONToIPFS"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        payload: ResponsePayload = {"pinataContent": json_to_pin}
        if options is not None:
            if "pinataMetadata" in options:
                payload["pinataMetadata"] = options["pinataMetadata"]
            if "pinataOptions" in options:
                payload["pinataOptions"] = options["pinataOptions"]
        response: requests.Response = requests.post(url=url, json=payload, headers=headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def remove_pin_from_ipfs(self, hash_to_remove: str) -> ResponsePayload:
        """Removes specified hash pin"""
        url: str = API_ENDPOINT + "pinning/removePinFromIPFS"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        body = {"ipfs_pin_hash": hash_to_remove}
        response: requests.Response = requests.post(url=url, json=body, headers=headers)
        return self._error(response) if not response.ok else {"message": "Removed"}

    def pin_list(self, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """https://pinata.cloud/documentation#PinList"""
        url: str = API_ENDPOINT + "data/pinList"
        payload: OptionsDict = options if options else {}
        response: requests.Response = requests.get(url=url, params=payload, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def user_pinned_data_total(self) -> ResponsePayload:
        url: str = API_ENDPOINT + "data/userPinnedDataTotal"
        response: requests.Response = requests.get(url=url, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore
