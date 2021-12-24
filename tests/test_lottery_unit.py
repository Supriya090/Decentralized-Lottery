from eth_account import account
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 1 usd = 2, 000 eth
    # usdEntryFee is 50
    # 50 usd = 50/2000 = 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_starter():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()

    #Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(
            {"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})

    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    # Assert
    assert lottery.lottery_state() == 2
