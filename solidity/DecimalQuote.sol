pragma solidity ^0.8.0;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier: AGPL-3.0-or-later
// File-Version: 1
// Description: ACL-enabled ERC20 token swap for tokens with compatible properties.

contract DecimalQuote {
	// Implements TokenQuote
	function valueFor(address _outToken, address _inToken, uint256 _value) public returns(uint256) {
		uint8 dout;
		uint8 din;
		uint256 d;
		bool r;
		bytes memory v;

		(r, v) = _outToken.call(abi.encodeWithSignature("decimals()"));
		require(r, "ERR_TOKEN_OUT");
		dout = abi.decode(v, (uint8));

		(r, v) = _inToken.call(abi.encodeWithSignature("decimals()"));
		require(r, "ERR_TOKEN_IN");
		din = abi.decode(v, (uint8));

		if (din == dout) {
			return _value;
		}

		if (din > dout) {
			d = din - dout;
			d = 10 ** d;
			return _value / d;
		} else {
			d = dout - din;
			d = 10 ** d;
			return _value * d;
		}	
	}
}
