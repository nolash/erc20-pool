SOLC = /usr/bin/solc

all:
	$(SOLC) --bin SwapPool.sol --evm-version byzantium | awk 'NR>3' > SwapPool.bin
	$(SOLC) --abi SwapPool.sol --evm-version byzantium | awk 'NR>3' > SwapPool.json
	$(SOLC) --metadata SwapPool.sol --evm-version byzantium | awk 'NR>3' > SwapPool.metadata.json
	truncate -s -1 SwapPool.bin

install: all
	cp -v *.json ../python/erc20_pool/data/
	cp -v *.bin ../python/erc20_pool/data/

