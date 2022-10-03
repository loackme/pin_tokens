# pin_tokens

A Python script to pin Tezos tokens on IPFS.
The data are retrieved through [Teztok](https://www.teztok.com/).

## Dependencies

Install the python dependencies.

```
python3 -m pip install -r requirements.txt
```

## Pinning tokens

Here's a breakdown of the parameters of the script:

### `--wallet`

Wallet of the creator/collector

### `--role`

Pinning tokens created by the `creator`'s or collected by the `collector`'s wallet.

### `--KT`

Contract on which the tokens were minted, comma separated. You can also use these shortcuts instead of the contract addresses:  
`akaswap`, `fxhash`, `hicetnunc`, `kalamint`, `rarible`, `typed`, `versum`

### `--service_type`, `--api_key` and `--api_secret`

This script allows you to pin tokens using different services.
- [Pinata](https://app.pinata.cloud/) `pinata`: see https://nftbiker.xyz/pin for instructions on how to generate an api key.
- [Infura](https://infura.io/) `infura`: once you have created an account, create a new IPFS project. In the project settings, look for 'PROJECT ID' and 'PROJECT SECRET'. That's what you need to use as `api_key` and `api_secret` respectively.
- [NFT.Storage](https://nft.storage/) `nftstorage`: once you have created an account, go to https://nft.storage/manage/ to create an `api_key`. `api_secret` is not required.
- [Filebase](https://filebase.com/) `filebase`: once you have created an account, create a bucket and go to https://console.filebase.com/keys to generate a token for this bucket. Use this token as `api_key`. `api_secret` is not required.
- Local Node `ipfs`: You can also use these scripts to pin to your own locally-running IPFS node. `api_key` and `api_secret` are not required.


Example:
```
python3 pin_tokens.py --wallet tz1NgN7FCrSzs4vfMroKXyKE32WsReYD4WPd --role creator --KT versum --service_type infura --api_key <key> --api_secret <secret>
```
