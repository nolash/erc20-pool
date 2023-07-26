# standard imports
import logging
import os
import enum

# external imports
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.eth.contract import (
    ABIContractEncoder,
    ABIContractDecoder,
    ABIContractType,
    abi_decode_single,
)
from chainlib.eth.jsonrpc import to_blockheight_param
from chainlib.eth.error import RequestMismatchException
from chainlib.eth.tx import (
    TxFactory,
    TxFormat,
)
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.block import BlockSpec
from hexathon import (
    add_0x,
    strip_0x,
)
from chainlib.eth.cli.encode import CLIEncoder

# local imports
from erc20_pool.data import data_dir

logg = logging.getLogger()


class Pool(TxFactory):

    __abi = None
    __bytecode = None

    def constructor(self, sender_address, name, symbol, decimals, declaration=None, accounts_registry=None, tx_format=TxFormat.JSONRPC, version=None):
        code = self.cargs(name, symbol, decimals, declaration=declaration, accounts_registry=accounts_registry, version=version)
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.finalize(tx, tx_format)


    @staticmethod
    def cargs(name, symbol, decimals, declaration=None, accounts_registry=None, version=None):
        if declaration == None:
            declaration = ZERO_CONTENT
        if accounts_registry == None:
            accounts_registry = ZERO_ADDRESS
        code = Pool.bytecode(version=version)
        enc = ABIContractEncoder()
        enc.string(name)
        enc.string(symbol)
        enc.uint256(decimals)
        enc.bytes32(declaration)
        enc.address(accounts_registry)
        args = enc.get()
        code += args
        logg.debug('constructor code: ' + args)
        return code


    @staticmethod
    def gas(code=None):
        return 4000000


    @staticmethod
    def abi():
        if Pool.__abi == None:
            f = open(os.path.join(data_dir, 'SwapPool.json'), 'r')
            Pool.__abi = json.load(f)
            f.close()
        return Pool.__abi


    @staticmethod
    def bytecode(version=None):
        if Pool.__bytecode == None:
            f = open(os.path.join(data_dir, 'SwapPool.bin'))
            Pool.__bytecode = f.read()
            f.close()
        return Pool.__bytecode


    def deposit(self, contract_address, sender_address, token_address, value, tx_format=TxFormat.JSONRPC, id_generator=None):
        enc = ABIContractEncoder()
        enc.method('deposit')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(token_address)
        enc.uint256(value)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format, id_generator=id_generator)
        return tx


    def swap(self, contract_address, sender_address, token_address_out, token_address_in, value, tx_format=TxFormat.JSONRPC, id_generator=None):
        enc = ABIContractEncoder()
        enc.method('withdraw')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(token_address_out)
        enc.address(token_address_in)
        enc.uint256(value)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format, id_generator=id_generator)
        return tx



