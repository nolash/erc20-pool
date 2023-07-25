pragma solidity ^0.8.0;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier: AGPL-3.0-or-later
// File-Version: 1
// Description: Voting contract using ERC20 tokens as shares

contract SwapPool {
	address registry;
	address quoter;
	uint256 feePpm;
	address feeAddress;
	uint256 public totalSupply;
	mapping ( address => uint256 ) fees;
	
	constructor(address _tokenRegistry) {
		registry = _tokenRegistry;
	}

	function deposit(address _token, uint256 _value) public {
		bool r;
		bytes memory v;

		allowedToken(_token, registry);

		(r, v) = _token.call(abi.encodeWithSignature('transferFrom(address,address,uint256)', msg.sender, this, _value));
		require(r, "ERR_TOKEN");
		r = abi.decode(v, (bool));
		require(r, "ERR_TRANSFER");
	}

	function getFee(uint256 _value) private view returns (uint256) {
		uint256 fee;
		
		fee = _value * feePpm;
		fee /= 1000000;

		return fee;
	}

	function getQuote(address _outToken, address _inToken, uint256 _value) private returns (uint256) {
		bool r;
		bytes memory v;
		uint256 quote;

		if (quoter == address(0x0)) {
			return _value;
		}

		(r, v) = quoter.call(abi.encodeWithSignature('valueFor(address,address,uint256)', _outToken, _inToken, _value));
		require(r, "ERR_QUOTER");
		quote = abi.decode(v, (uint256));
		return quote;
	}

	function withdraw(address _outToken, address _inToken, uint256 _value) public {
		bool r;
		bytes memory v;
		uint256 netValue;
		uint256 balance;
		uint256 fee;

		fee = getFee(_value);
		netValue = _value - fee;
		netValue = getQuote(_outToken, _inToken, netValue);

		(r, v) = _outToken.call(abi.encodeWithSignature("balanceOf(address)", this));
		require(r, "ERR_TOKEN");
		balance = abi.decode(v, (uint256));
		require(balance >= netValue + fee, "ERR_BALANCE");

		deposit(_inToken, _value);

		(r, v) = _outToken.call(abi.encodeWithSignature('transferFrom(address,address,uint256)', this, msg.sender, netValue));
		require(r, "ERR_TOKEN");
		r = abi.decode(v, (bool));
		require(r, "ERR_TRANSFER");
		
		if (feeAddress != address(0)) {
			fees[_outToken] += fee;
		}
	}

	function withdraw(address _token, uint256 _value) public returns (uint256) {

	}

	function allowedToken(address _token, address _registry) private {
		bool r;
		bytes memory v;

		if (_registry == address(0)) {
			return;
		}
		
		(r, v) = _registry.call(abi.encodeWithSignature('have(address)', _token));
		require(r, "ERR_REGISTRY");
		r = abi.decode(v, (bool));
		require(r, "ERR_UNAUTH_TOKEN");
	}
}
