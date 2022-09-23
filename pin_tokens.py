import json, requests, sys, getopt
from ipfs_utils import IPFSPinner

shortcuts = {
    'hicetnunc': 'KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton',
    'versum': 'KT1LjmAdYQCLBjwv4S2oFkEzyHVkomAf5MrW',
    'fxhash': 'KT1U6EHmNxJTkvaWJ4ThczG4FSDaHC21ssvi,KT1KEa8z6vWXDJrVqtMrAeDVzsvxat3kHaCE',
    'typed': 'KT1J6NY5AU61GzUX51n59wwiZcGJ9DrNTwbK'
}

def do_teztok_request(wallet,KT,role):
    url = "https://unstable-do-not-use-in-production-api.teztok.com/v1/graphql/"
    query = f"""query{{tokens(
        where: {{
            fa2_address: {{_in: {parseKT(KT)}}},
            {parseRole(role,wallet)}
        }}
        ) {{
            name
            metadata_uri
            artifact_uri
            display_uri
            thumbnail_uri
        }}
    }}"""
    return requests.post(url, json={'query': query})

def parseKT(KT):
    for s in shortcuts:
        KT = KT.replace(s,shortcuts[s])
    KT = [kt for kt in KT.split(",") if kt[:2] == 'KT']
    if len(KT) > 0:
        return '["' + '","'.join(KT) + '"]'
    else:
        raise Exception('No valid contract')

def parseRole(role,wallet):
    if role == 'collector':
        return f'holdings: {{holder_address: {{_eq: "{wallet}"}}}}'
    elif role == 'creator':
        return f'artist_address: {{_eq: "{wallet}"}}'
    else:
        raise Exception('Invalid role')

def main(argv):
    wallet = ''
    KT = ''
    role = ''
    api_key = ''
    api_secret = ''
    service_type = 'infura'

    try:
        opts, args = getopt.getopt(argv, "w:c:r:k:s:t:",["wallet=","KT=","role=","api_key=","api_secret=","service_type="])

    except:
        print("Error in arguments: pin_creations.py --wallet <wallet> --role [creator|collector] --KT <KT> --service_type [pinata|ipfs|infura] --api_key <api_key> --api_secret <api_secret>")

    for opt, arg in opts:
        if opt in ['-w', '--wallet']:
            wallet = arg
        elif opt in ['-c', '--KT']:
            KT = arg
        elif opt in ['-r', '--role']:
            role = arg
        elif opt in ['-k', '--api_key']:
            api_key = arg
        elif opt in ['-s', '--api_secret']:
            api_secret = arg
        elif opt in ['-t', '--service_type']:
            service_type = arg

    pinner = IPFSPinner(service_type, api_key, api_secret)
    r = do_teztok_request(wallet,KT,role)
    if r.status_code == 200:
        binary = r.content
        output = json.loads(binary)
        if 'data' in output:
            tokens = output['data']['tokens']
            for token in tokens:
                pinner.pinToken(token)
            if len(tokens) == 0:
                print('No token found')
        else:
            print('No data')
    else:
        print(f'Teztok request: error {r.status_code}')

main(sys.argv[1:])
