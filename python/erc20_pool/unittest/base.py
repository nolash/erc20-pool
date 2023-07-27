# standard imports
import logging
import time

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from chainlib.eth.address import to_checksum_address
from giftable_erc20_token.unittest import TestGiftableToken
from eth_erc20 import ERC20
from chainlib.eth.block import block_latest
from eth_accounts_index.unittest import TestAccountsIndex
from eth_accounts_index.registry import AccountRegistry
from giftable_erc20_token import GiftableToken

# local imports
from erc20_pool import Pool

logg = logging.getLogger(__name__)

hash_of_foo = '2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae'
hash_of_bar = 'fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9'
hash_of_baz = 'baa5a0964d3320fbc0c6a922140453c8513ea24ab8fd0577034804a967248096'


class TestERC20Pool(TestGiftableToken):

    expire = 0

    def setUp(self):
        super(TestERC20Pool, self).setUp()

        self.foo_address = self.address
        self.bar_address = self.publish_giftable_token('Bar Token', 'BAR', 16)
        self.baz_address = self.publish_giftable_token('Baz Token', 'BAZ', 16)
        self.initial_supply_bar = 1 << 20
        self.initial_supply_baz = 1 << 15

        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.mint_to(self.bar_address, self.accounts[0], self.accounts[1], self.initial_supply_bar)
        self.conn.do(o)
        o = receipt(tx_hash)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        (tx_hash, o) = c.mint_to(self.baz_address, self.accounts[0], self.accounts[2], self.initial_supply_baz)
        self.conn.do(o)
        o = receipt(tx_hash)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        c = Pool(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.constructor(self.accounts[0], "Big Pool", "BIG", 16)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        self.pool_address = to_checksum_address(r['contract_address'])
        logg.debug('published bar token {}, baz token {}'.format(self.bar_address, self.baz_address))
        logg.debug('published pool on address {} with hash {}'.format(self.pool_address, tx_hash))
