import json, requests, sys, subprocess

"""  IPFSPinner class coded by odbol for fx_hash_utils
https://github.com/loackme/fx_hash_utils/commit/634a558a03d113c537aaa06066b517acc93a3ba0
"""

class IPFSPinner:
    """Pins hashes to a specific service, like Infura, Pinata, or your own locally-running IPFS node."""

    def __init__(self, ipfs_service_type, api_key, api_secret):
        """Creates a new IPFSPinner for the given service type.

         Parameters
        ----------
        ipfs_service_type : str
            one of "pinata", "ipfs" (for a locally-running IPFS node), or "infura"
        api_key : str
            the API key for the service (not needed for "ipfs")
        api_secret : str
            the API secrete for the service (not needed for "ipfs")
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.ipfs_service_type = ipfs_service_type

    def pinToken(self, token):
        name = token['name']
        print(f'Pinning {name}...')
        if not(token['metadata_uri'] is None):
            ipfs_hash = token['metadata_uri'][7:]
            self.pin(ipfs_hash,name,"Metadata")
        if not(token['artifact_uri'] is None):
            ipfs_hash = token['artifact_uri'][7:]
            self.pin(ipfs_hash,name,"Artifact")
        if not(token['display_uri'] is None):
            ipfs_hash = token['display_uri'][7:]
            self.pin(ipfs_hash,name,"Display")
        if not(token['thumbnail_uri'] is None):
            ipfs_hash = token['thumbnail_uri'][7:]
            self.pin(ipfs_hash,name,"Thumbnail")
        print("\n")


    def pin(self, ipfs_hash, name, type_data):
        if self.ipfs_service_type == 'pinata':
            self.pinataRequest(ipfs_hash, name, type_data)
        elif self.ipfs_service_type == 'ipfs':
            self.pinIpfsLocalNode(ipfs_hash, name, type_data)
        elif self.ipfs_service_type == 'infura':
            self.infuraRequest(ipfs_hash, name, type_data)
        else:
            raise Exception('Unknown IPFS service type')

    def pinataRequest(self, ipfs_hash,name, type_data):
        url_pin = "https://api.pinata.cloud/pinning/pinByHash"
        headers = {
            'content-type': 'application/json',
            'pinata_api_key': self.api_key,
            'pinata_secret_api_key': self.api_secret
        }
        body = {
            'pinataMetadata' : {
                'name' : f'{name} {type_data}',
            },
            'hashToPin' : ipfs_hash
        }
        r = requests.post(url_pin, data=json.dumps(body), headers=headers)
        if r.status_code == 200:
            print(f'{type_data} pinned')
        else:
            print(f'Error pinning {type_data}: {r.status_code}')

    def pinIpfsLocalNode(self, ipfs_hash, name, type_data):
        result = subprocess.call(["ipfs", "pin", "add", ipfs_hash])
        if result == 0:
            print(f'{type_data} pinned')
        else:
            print(f'Error pinning IPFS hash. Error code {result}')

    def infuraRequest(self, ipfs_hash, name, type_data):
        url_pin = "https://ipfs.infura.io:5001/api/v0/pin/add"
        params = {'arg': ipfs_hash}
        r = requests.post(url_pin, params=params, auth=(self.api_key, self.api_secret))
        if r.status_code == 200:
            print(f'{type_data} pinned')
        else:
            print(f'Error pinning {type_data}: {r.status_code}')
