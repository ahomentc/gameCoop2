pragma solidity ^0.5.0;

contract Org
{
	mapping(uint => address payable) private userAddresses;

	// Maybe make this a payable that costs 0 but gets the user's address
	// Or have an option for user to enter their address or click to add it and if click then do above.
	// So first line would be a new function similar to below but with payable
	function addUserAddress(uint userId, address payable userAddress) public
	{
		userAddresses[userId] = userAddress;
	}

	function deposit() payable public {
    }

	function getBal() public view returns (uint) {
        return address(this).balance;
    }

    // called by user to withdraw the money they have
    // percentage: percentage of total money user gets. In the format 30.25
    function withdraw(uint percentage) public
    {
        uint balance = getBal();
        require(balance > 0);
    	// multiply by 100 because passed in as 30.25% and need to account 
		uint amountToSend = ( balance * 100 * percentage ) / 10000;
		msg.sender.transfer(amountToSend);
    }

    // not called by user that is recieving money... happens in background
    // percentage: percentage of total money user gets. In the format 30.25
	function distributeToIndividual(uint userId, uint percentage) public
	{
		uint amountToSend = ( getBal() * 100 * percentage ) / 10000;
		address payable userAdr = userAddresses[userId];
		userAdr.transfer(amountToSend);
	}

	// distribute to multiple users... also happens in the background
	// userIds: list of ids to distribute to
	// userPercentages: list of percentages to give to those ids
	// userIds AND userPercentages MUST BE IN THE SAME ORDER
	function distributeToMultiple(uint[] memory userIds, uint[] memory userPercentages ) public
	{
	    uint balance = getBal();
		for(uint i=0; i<userIds.length; i++)
		{
			uint userId = userIds[i];
			uint percentage = userPercentages[i];
			uint amountToSend = ( balance * 100 * percentage ) / 10000;
			address payable userAdr = userAddresses[userId];
			userAdr.transfer(amountToSend);
		}
	}
}