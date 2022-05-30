from http.cookies import SimpleCookie
from brownie import network, AdvancedCollectible, config
from scripts.AdvancedCollectible.utils import get_account, OPENSEA_URL, get_contract, fund_with_link


def main():
    account = get_account(id='fcc_account')
    
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract('link_token'),
        config['networks'][network.show_active()]['keyhash'],
        config['networks'][network.show_active()]['fee'],
        {'from':account},
        publish_source = config['networks'][network.show_active()].get('verify', False)
    )
    print(advanced_collectible.address)
    fund_with_link(advanced_collectible.address, account=account)
    advanced_collectible.createCollectible({'from':account}).wait(1)
    print("New token has been created!")