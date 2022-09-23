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

Pinning tokens created by `creator`'s or collected by `collector`'s wallet.

### `--KT`

Contract(s) on which the tokens were minted, comma separated. You can also use the shortcuts `hicetnunc`, `fxhash`, `typed`, `versum` instead of their respective contracts.

### `--service_type`, `--api_id` and `--api_key`

This script allows you to pin tokens using different services.
- Pinata `pinata`: see https://nftbiker.xyz/pin for instructions on how to generate an api key.
- Infura `infura`: once you have created an account on https://infura.io/, create a new IPFS project. In the project settings, look for 'PROJECT ID' and 'PROJECT SECRET'. That's what you need to use as 'api_key' and 'api_secret' respectively.
- Local Node `ipfs`: You can also use these scripts to pin to your own locally-running IPFS node. Note that pinning the generator (last step) can take a very long time, depending on your node and the size of the artwork.


Example:
```
python3 pin_tokens.py --wallet tz1NgN7FCrSzs4vfMroKXyKE32WsReYD4WPd --role creator --KT versum --service_type infura --api_id <id> --api_key <key>
```
