# standard imports
import unittest
import logging
import os
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from chainlib.eth.block import block_latest
from hexathon import same as same_hex
from eth_erc20 import ERC20
from giftable_erc20_token import GiftableToken
from eth_interface.unittest import TestERC165

# local imports
from erc20_pool.unittest import TestERC20Pool
from erc20_pool import Pool

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

TestERC165.add_interface_check('9493f8b2')
TestERC165.add_interface_check('0d7491f8')

class TestPoolInterface(TestERC20Pool, TestERC165):

    def test_interface(self):
        self.address = self.pool_address
        pass


if __name__ == '__main__':
    unittest.main()

