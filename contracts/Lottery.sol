// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract Lottery{

    address payable[] public players;
    uint256 public usdEntryFee;

    constructor(){
        usdEntryFee = 50*(10**18);

    }

    function enter() public payable{
        //$50 minimum
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256){

    }
    function startLottery() public{}
    function endLottery() public{}


}