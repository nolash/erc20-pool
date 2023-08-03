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
from erc20_limiter import Limiter

# local imports
from erc20_pool.quote import DecimalQuote
from erc20_pool.unittest.quote import TestDecimalQuote

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

class TestQuote(TestDecimalQuote):

    def setUp(self):
        super(TestQuote, self).setUp()
        self.tokens = {}
        self.publish_token('Foo token', 'FOO', 14)
        self.publish_token('Bar token', 'BAR', 18)
        self.publish_token('Baz token', 'BAZ', 11)

    def publish_token(self, name, symbol, decimals):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        self.symbol = name
        self.name = symbol
        self.decimals = decimals
        (tx_hash, o) = c.constructor(self.accounts[0], self.name, self.symbol, self.decimals, expire=0)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        address = r['contract_address'] 
        logg.debug('published "{}" ("{}") on address {} with hash {}'.format(name, symbol, address, tx_hash))
        self.tokens[symbol] = address


    def test_quote(self):
        c = DecimalQuote(self.chain_spec)
        o = c.value_for(self.quoter_address, self.tokens['FOO'], self.tokens['FOO'], 10**18, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 10**18)

        o = c.value_for(self.quoter_address, self.tokens['FOO'], self.tokens['BAR'], 10**18, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 10**14)

        o = c.value_for(self.quoter_address, self.tokens['FOO'], self.tokens['BAZ'], 10**18, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 10**21)


if __name__ == '__main__':
    unittest.main()
