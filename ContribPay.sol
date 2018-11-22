pragma solidity ^0.4.2;

// Maybe implement some sort of ERC20 token for each organization.

contract ContribPay
{
	Organization[] organizations;

	function createNewOrg
	{

	}

	function removeOrg
	{

	}
}

contract Org
{
	uint org_id;
	mapping(uint => User) public idToUser;
	// mapping(uint => address) public idToUserAddress; don't think this will work


	function joinOrg(uint id)
	{
		User new_user = new User(id);
		idToUser[id] = User;
	}

	function deposit(uint256 amount) payable external  // maybe public instead of external. External less gass but can't be accessed internally. Public can do both.
	{
		// Ether is automatically transfered to this contract
		require(msg.value == amount);
	}

	function getBalance() public view returns (uint256) 
	{
        return address(this).balance;
    }

    // param: [[id,wei]]
	function Payout(uin256[][] payments) public returns (bool success)
	{
		for(uint i = 0; i < payments.length; i++)
		{
			idToUser[payments[i][0]].transfer(payments[i][1]);
			// idToUserAddress[payments[i][0]].transfer(payments[i][1]); 
			// ^^ don't think this will work. But it'd be straight to user address with no User contract used
		}
		return true;
	}
}

contract User
{
	uint user_id;
	// address recieveAddress;

	function User(uint _id) public 
	{
		user_id = id;
	}

	function getId public view returns (uint)
	{
		return user_id;
	}

	// send the ether stored in this contract
	function sendToAddress(uint256 amount) public
	{
		// recieveAddress.transfer(amount);
		// or in javascript: await web3.eth.sendTransaction({ from: accounts[0], to: accounts[1], value: 10**18 });
		// so maybe store a list of the user addresses and the org addresses in the database

		msg.sender.transfer(address(this).balance);
	}

	function getBalance() public view returns (uint)
	{
		return this.balance;
    }
}