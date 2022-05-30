from http.cookies import SimpleCookie
from brownie import network, SimpleCollectible
from scripts.AdvancedCollectible.utils import get_account

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def main():
    account = get_account(id='fcc_account')
    print(account)
    simple_collectible = SimpleCollectible.deploy({'from':account})
    tx = simple_collectible.createCollectible(sample_token_uri, {'from':account})
    tx.wait(1)
    print(f"Noice, it's here {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}")