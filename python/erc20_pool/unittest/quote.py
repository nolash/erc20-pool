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
from erc20_limiter.unittest import TestLimiter

# local imports
from erc20_pool.quote import DecimalQuote

logg = logging.getLogger(__name__)

class TestDecimalQuote(EthTesterCase):

    def setUp(self):
        super(TestDecimalQuote, self).setUp()
        self.conn = RPCConnection.connect(self.chain_spec, 'default')

        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = DecimalQuote(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.constructor(self.accounts[0])
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        self.quoter_address = to_checksum_address(r['contract_address'])
        logg.debug('published quoter {}'.format(self.quoter_address))
