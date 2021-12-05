// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Lottery is Ownable{
 
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE{
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) {
        usdEntryFee = 50*(10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable{
        require(lottery_state = LOTTERY_STATE.OPEN, "Should be open to enter");
        //$50 minimum
        require(msg.value >= getEntranceFee(),"Not enough ETH!");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256){
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;    //18 decimals
        // $50, $2,000 / ETH
        // 50/2,000
        // 50 * 100000 / 2000
        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner{
        require(lottery_state = LOTTERY_STATE.CLOSED, "Can't start a new lottery yet");
        lottery_state = LOTTERY_STATE.OPEN;
    }
    function endLottery() public{}


}