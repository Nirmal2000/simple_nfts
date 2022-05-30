from http.cookies import SimpleCookie
from brownie import network, AdvancedCollectible, config
from scripts.AdvancedCollectible.utils import get_account, OPENSEA_URL, get_contract, fund_with_link

def main():
    account = get_account(id='fcc_account')
    advanced_collectible = AdvancedCollectible[-1]
    print(advanced_collectible.address)
    fund_with_link(advanced_collectible.address, account=account)

    advanced_collectible.createCollectible({'from':account}).wait(1)
