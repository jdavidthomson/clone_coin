#####################
# Clone Coin Script #
#####################

The purpose of this script is to take the bitcoin reference client and make a new "cryptocurrency".

This is done by following these steps:
1) Run GenesisH0 with appropriate params
2) Put the params spit out by GenesisH0 into the chainparams.cpp file
3) Setup the dependencies for building bitcoind
4) Build the binary for the cloned coin
5) Start the cloned coin in two or more instances
6) Get a new address using RPC commands
7) Generate 1 block using RPC commands 
8) Mine 100 more blocks using CGMiner
9) Deploy the blockchain to three or more servers

Notes:
1) The parameters inside of the bitcoin reference client stay the same - half lilfe of coins is still the same, difficulty adjustment period stays the same

Requirements:
python-pip: sudo apt install python-pip
libssl-dev: sudo apt install libssl-dev 
