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
from erc20_pool.unittest import TestERC20PoolLimiter
from erc20_pool import Pool

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

class TestPoolLimit(TestERC20PoolLimiter):

    def test_deposit_limit(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = ERC20(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.approve(self.foo_address, self.accounts[0], self.pool_address, 1024)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.pool_address, self.accounts[0], self.foo_address, 513)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 0)

        c = Limiter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.set_limit(self.limiter_address, self.accounts[0], self.foo_address, 512, holder_address=self.pool_address)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        o = c.limit_of(self.limiter_address, self.foo_address, self.pool_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 512)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.pool_address, self.accounts[0], self.foo_address, 513)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 0)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.pool_address, self.accounts[0], self.foo_address, 512)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.pool_address, self.accounts[0], self.foo_address, 1)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 0)

        c = Limiter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.set_limit(self.limiter_address, self.accounts[0], self.foo_address, 513, holder_address=self.pool_address)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.deposit(self.pool_address, self.accounts[0], self.foo_address, 1)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)


if __name__ == '__main__':
    unittest.main()
