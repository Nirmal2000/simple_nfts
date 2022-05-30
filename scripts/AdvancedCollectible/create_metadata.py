from http.cookies import SimpleCookie
from brownie import network, AdvancedCollectible, config
from pyparsing import col
from requests import request
import requests
from scripts.AdvancedCollectible.utils import get_account, OPENSEA_URL, get_contract, fund_with_link, get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json

def main():
    if len(AdvancedCollectible) == 0:
        account = get_account(id='fcc_account')
        advanced_collectible = AdvancedCollectible.deploy(
            get_contract("vrf_coordinator"),
            get_contract('link_token'),
            config['networks'][network.show_active()]['keyhash'],
            config['networks'][network.show_active()]['fee'],
            {'from':account},
            publish_source = True
        )
    
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print("Number of minted NFTs :",number_of_collectibles)

    for tok_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdtoBreed(tok_id))
        metadata_fn = f'./metadata/{network.show_active()}/{tok_id}-{breed}.json'
        collectible_md = metadata_template
        if Path(metadata_fn).exists():
            print("exists...!!")
        else:
            print(f"Creating metadata {metadata_fn}")
            collectible_md['name'] = breed
            collectible_md['description'] = f"noice {breed}"
            img_path = f"./img/" + breed.lower().replace('_','-') + '.png'
            image_uri = upload_to_ipfs(img_path)
            collectible_md['image'] = image_uri
            with open(metadata_fn,'w') as file:
                json.dump(collectible_md, file)
            upload_to_ipfs(metadata_fn)


def upload_to_ipfs(img_path):
    with Path(img_path).open('rb') as fp:
        print(img_path)
        img_bin = fp.read()
        ipfs_url = 'http://127.0.0.1:5001'
        ep = '/api/v0/add'
        rsp = requests.post(ipfs_url + ep, files={'files':img_bin})
        ipfs_hash = rsp.json()['Hash']
        fn = img_path.split('/')[-1:][0]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}/?filename={fn}"
        print(img_uri)
        return img_uri


