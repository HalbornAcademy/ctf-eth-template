from brownie import *

def deploy(state, deployer, player):
    Test.deploy({'from': deployer[9]})

# This function should return a tuple of 2 values
# - First value is a boolean, if the challenge was solved or not
# - Second value is a message to display on the CTF platform

# You can use the "state" to retrieve global state set by any other
# function including runnables
def solved(state, deployer, player):
    if Test[-1].balance() > 0:
        return True, "Solved!"
    else:
        return False, "Need more coins!"

#####################
# CONFIG
#####################
# --------------------------
# RPC & BLOCK_NUMBER:
# --------------------------
# It is used to fork from a testnet/mainnet RPC url from an specific BLOCK_NUMBER
# ex:
#   'RPC': 'https://rpc.ankr.com/eth'
#   'BLOCK_NUMBER': '1234567'
#
# --------------------------
# FLAGS:
# --------------------------
# You can specify custom flags for the "anvil" node, such as setting the default balance
# or disabling mining with `--no-mining`, etc
#
#     > These flags will affect only the player node instance
# ex:
#   'FLAGS': "--balance 10 --no-mining"
#
# --------------------------
# MNEMONIC
# --------------------------
# The mnemonic used to generate the player accounts, if not specified it is randomly generated
# ex:
#   'MNEMONIC': 'test test test test test test test test test test test junk'
#
# --------------------------
# RUNNABLES:
# --------------------------
# You can create custom functions that can be executed every x seconds,
# they take 3 arguments, the state, deployer and player accounts.
#
#        def check_for_low_balance(state, deployer, player):
#            state['low_balance'] = False
#            if player[0].balance < web3.toWei(1, 'ether'):
#                state['low_balance'] = True
# On the CONFIG file you can add runnables by storing a tuple of (function, seconds):
#      'RUNNABLES': [(check_for_low_balance, 10)],
#
# This will add the check_for_low_balance function to be executed every 10 seconds
#
# More Examples:
# For example when mining is disabled you could check for pending
# mempool txs and act on it modifying the "state" and reporting that the challenge
# is solved under "solved"
#
# --------------------------
# ALLOWED_RPC_METHODS
# --------------------------
#
# Does allow to specify methods that will be allowed on the player node.
# By default the following namespaces are enabled:
#
#   ["web3", "eth", "net", "debug", "txpool"]
#
# Refer to JSON RPC and https://book.getfoundry.sh/reference/anvil/
# ex,
#   'ALLOWED_RPC_METHODS': ["evm_mine"] # allowing mining blocks

CONFIG = {
    'RPC': '',
    'BLOCK_NUMBER': '',
    'FLAGS': '',
    'MNEMONIC': '',
    'RUNNABLES': [],
    'ALLOWED_RPC_METHODS': []
}