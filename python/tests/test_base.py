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

# local imports
from erc20_pool.unittest import TestERC20Pool
from erc20_pool import Pool
#from evm_tokenvote.unittest.base import hash_of_foo
#from evm_tokenvote import Voter
#from evm_tokenvote import ProposalState


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

class TestPoolBase(TestERC20Pool):

    def test_deposit(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.approve(self.foo_address, self.accounts[0], self.voter_address, 1024)
        self.rpc.do(o)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.voter_address, self.accounts[0], self.foo_address, 1024)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.balance_of(self.foo_address, self.voter_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 1024)


    def test_swap(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.approve(self.foo_address, self.accounts[0], self.voter_address, 1024)
        self.rpc.do(o)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.voter_address, self.accounts[0], self.foo_address, 1024)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[1], conn=self.conn)
        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.approve(self.bar_address, self.accounts[1], self.voter_address, 768)
        self.rpc.do(o)

        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.approve(self.foo_address, self.accounts[1], self.voter_address, 768)
        self.rpc.do(o)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.swap(self.voter_address, self.accounts[1], self.foo_address, self.bar_address, 768)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.balance_of(self.foo_address, self.accounts[1], sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 768)


if __name__ == '__main__':
    unittest.main()
