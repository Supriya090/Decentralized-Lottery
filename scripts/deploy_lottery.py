from scripts.helpful_scripts import get_account
from brownie import Lottery


def deploy_lottery():
    account = get_account(id="testnet-account")
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed")
    )


def main():
    deploy_lottery()
