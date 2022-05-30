from os import link
from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract, interface, AdvancedCollectible
from web3 import Web3

LOCAL_BC_ENV = ['development', 'ganache-local']
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = ['pub', 'shiab_inu', 'st_bernard']

def get_breed(b):
    return BREED_MAPPING[b]

def get_account(index=None, id=None):
    if index is not None:        
        return accounts[index]
    if network.show_active() in LOCAL_BC_ENV:
        account = accounts[0]
        return account
    if id:
        return accounts.load(id)

contract_to_mock = {    
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
    'AdvancedCollectible':AdvancedCollectible,
}

def deploy_mocks():
    account = get_account()
    print("deploying mocks...")    
    MockV3Aggregator.deploy(18, Web3.toWei(2000, 'ether'), {'from':account})
    lk = LinkToken.deploy({'from':account})
    VRFCoordinatorMock.deploy(lk.address, {'from':account})
    print("deployed mocks...") 

def get_contract(contract_name):
    
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BC_ENV:
        if len(contract_type) == 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config['networks'][network.show_active()][contract_name]

        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

def fund_with_link(contract_addr, account=None, link_token=None, amount=100000000000000000): #0.1 link
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    print("funding..")
    tx = link_token.transfer(contract_addr, amount, {'from': account})    
    tx.wait(1)