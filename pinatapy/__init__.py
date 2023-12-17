"""Non-official Python library for Pinata.cloud"""

import os
import typing as tp

import requests
import json

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

    @staticmethod
    def _validate_destination_folder_name(path: str) -> str:
        """
        Validates the IPFS destination folder name is valid by removing 
        blankspaces and adding '/' to the end of the path
        """
        path = path.replace(" ", "")
        if not path.endswith("/"):
            path = path + "/"
        return path
    
    @staticmethod
    def _validate_path_to_file(path: str) -> str:
        """
        Validates the path to file is valid by removing '/' at the end 
        of the path.
        """
        path = path.replace(" ", "")
        if path.endswith("/"):
            path = path[:-1]
        return path

    def pin_file_to_ipfs(
            self,
            path_to_file: str,
            ipfs_destination_path: str = "/",
            save_absolute_paths: bool = True,
            options: tp.Optional[OptionsDict] = None,
    ) -> ResponsePayload:
        """
        Pin any file, or directory, to Pinata's IPFS nodes

        Args:
            path_to_file: local path of file/directory to upload to IPFS node
            ipfs_destination_path: destination path of file(s) on the IPFS node. 
                You can only set one destination path per call. 
                Pathway can be viewed in the Pinata Cloud Pin Manager (https://app.pinata.cloud/pinmanager).
                Ex: input => destination path
                    '' => /
                    'animal-nfts/' => /animal-nfts/
                    'retro-nfts/animals' => /retro-nfts/animals/
            save_absolute_paths: parameter to control filepaths cutting.
                Ex: input => destination path
                    true: /dir1/dir2/dir3/filename => /dir1/dir2/dir3/filename
                    false: /dir1/dir2/dir3/filename => filename
            options: optional parameters (pinataMetadata, pinataOptions)

        Returns:
            JSON response

        More: https://docs.pinata.cloud/pinata-api/pinning/pin-file-or-directory
        """
        url: str = API_ENDPOINT + "pinning/pinFileToIPFS"
        headers: Headers = {k: self._auth_headers[k] for k in ["pinata_api_key", "pinata_secret_api_key"]}
        payload: OptionsDict = {}
        dest_folder_name = (
            ipfs_destination_path
            if ipfs_destination_path == "/"
            else self._validate_destination_folder_name(ipfs_destination_path)
        )
        
        def get_all_files(directory: str) -> tp.List[str]:
            """get a list of absolute paths to every file located in the directory"""
            paths: tp.List[str] = []
            for root, dirs, files_ in os.walk(os.path.abspath(directory)):
                for file in files_:
                    paths.append(os.path.join(root, file))
            return paths

        def get_mutated_filepath(filepath: str, dest_folder_name: str, save_absolute_paths: bool, path_to_file: str, is_directory: bool = False):
            """transform filepath with dest_folder_name and absolute path saving rules"""
            if save_absolute_paths:
                return dest_folder_name + (filepath[:1].replace("/", "") + filepath[1:])  # remove first '/' if exists
            else:
                # can't pin directory into root and save directory's hierarchy
                if is_directory and dest_folder_name == "/":
                    dest_folder_name =  self._validate_path_to_file(path_to_file).split("/")[-1]
                return dest_folder_name + filepath.split(dest_folder_name)[-1]
        
        files: tp.List[str, tp.Any]

        # If path_to_file is a directory
        if os.path.isdir(path_to_file):
            all_files: tp.List[str] = get_all_files(path_to_file)
            files = [("file", (get_mutated_filepath(file, dest_folder_name, save_absolute_paths, path_to_file, is_directory=True), open(file, "rb"))) for
                     file in all_files]  # type: ignore
        # If path_to_file is a single file
        else:
            files = [("file", (get_mutated_filepath(path_to_file, dest_folder_name, save_absolute_paths, path_to_file),
                               open(path_to_file, "rb")))]  # type: ignore

        if options is not None:
            if "pinataMetadata" in options:
                pinataMetadata = options["pinataMetadata"]
                payload["pinataMetadata"] = pinataMetadata if type(pinataMetadata) == str else json.dumps(pinataMetadata)
            if "pinataOptions" in options:
                pinataOptions = options["pinataOptions"]
                payload["pinataOptions"] = pinataOptions if type(pinataOptions) == str else json.dumps(pinataOptions)

        response: requests.Response = requests.post(url=url, files=files, headers=headers, data=payload)
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
        """ Pin file to Pinata using its IPFS hash

        https://docs.pinata.cloud/pinata-api/pinning/pin-by-cid
        """
        payload: OptionsDict = {"pinataMetadata": {"name": filename}, "hashToPin": ipfs_hash}
        url: str = API_ENDPOINT + "/pinning/pinByHash"
        response: requests.Response = requests.post(url=url, json=payload, headers=self._auth_headers)
        return self._error(response) if not response.ok else response.json()  # type: ignore

    def pin_jobs(self, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """ Retrieves a list of all the pins that are currently in the pin queue for your user.

        More: https://docs.pinata.cloud/pinata-api/pinning/list-pin-by-cid-jobs
        """
        url: str = API_ENDPOINT + "pinning/pinJobs"
        payload: OptionsDict = options if options else {}
        response: requests.Response = requests.get(url=url, params=payload, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def pin_json_to_ipfs(self, json_to_pin: tp.Any, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """ pin provided JSON
        
        More: https://docs.pinata.cloud/pinata-api/pinning/pin-json
        """
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
        """ Removes specified hash pin

        More: https://docs.pinata.cloud/pinata-api/pinning/remove-files-unpin
        """
        url: str = API_ENDPOINT + f"pinning/unpin/{hash_to_remove}"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        response: requests.Response = requests.delete(url=url, data={}, headers=headers)
        return self._error(response) if not response.ok else {"message": "Removed"}

    def pin_list(self, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """ Returns list of your IPFS files based on certain filters.

        Ex: Filter by only 'pinned' files
            options = ({"status": "pinned"})
        Ex: Filter by 'pinned' files and files that contain a metadata 'name' of 'dogs-nfts'
            options = ({"status": "pinned", "metadata[name]": "dogs-nfts"})
        
        More: https://docs.pinata.cloud/pinata-api/data/query-files
        """
        url: str = API_ENDPOINT + "data/pinList"
        payload: OptionsDict = options if options else {}
        response: requests.Response = requests.get(url=url, params=payload, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def user_pinned_data_total(self) -> ResponsePayload:
        url: str = API_ENDPOINT + "data/userPinnedDataTotal"
        response: requests.Response = requests.get(url=url, headers=self._auth_headers)
        return response.json() if response.ok else self._error(response)  # type: ignore

    def generate_api_key(self, key_name: str, is_admin: bool, options: tp.Optional[OptionsDict] = None) -> ResponsePayload:
        """Generates Pinata API key. Can only be called by using an "Admin" key.
        If not an "admin" key is being created, the "permissions" option must be included.
        Returns three values: The API Key, the API Secret, and a JWT Bearer Token.
        More: https://docs.pinata.cloud/reference/post_users-generateapikey
        """
        url: str = API_ENDPOINT + "users/generateApiKey"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        payload: ResponsePayload = {"keyName": key_name}
        if is_admin:
            payload["permissions"] = {"admin": True}
        else:
            if (options is None) or (not "permissions" in options):
                raise Exception("Setting permissions is necessary! Check https://docs.pinata.cloud/reference/post_users-generateapikey")
            else:
                payload["permissions"] = options["permissions"]
                if "maxUses" in options:
                    payload["maxUses"] = options["maxUses"]
        response: requests.Response = requests.post(url=url, json=payload, headers=headers)
        return response.json() if response.ok else self._error(response)

    def revoke_api_key(self, api_key: str) -> ResponsePayload:
        """Revokes Pinata API key. Can only be called by using an "Admin" key.
        ATTENTION: This method will returns "Revoked" even if there is no such key exists.
        """
        url: str = API_ENDPOINT + "users/revokeApiKey"
        headers: Headers = self._auth_headers
        headers["Content-Type"] = "application/json"
        payload: ResponsePayload = {"apiKey": api_key}
        response: requests.Response = requests.put(url=url, json=payload, headers=headers)
        return self._error(response) if not response.ok else {"message": "Revoked"}