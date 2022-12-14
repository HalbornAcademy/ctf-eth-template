from brownie import *

def deploy(state, deployer, player):
    pass

#####################
# CONFIG
#####################
# --------------------------
# FLAGS:
# --------------------------
# You can specify custom flags for the "anvil" node, such as setting the default balance
# or disabling mining with `--no-mining`, etc
#
#     > These flags will affect only the deployer node instance
# ex:
#   'FLAGS': "--balance 10 --no-mining"
#
# --------------------------
# MNEMONIC
# --------------------------
# The mnemonic used to generate the deployer accounts.
#    > It MUST be specified
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
# Does allow to specify methods that will be allowed on the player node but without exposing that information.
#
#   ["web3", "eth", "net", "debug", "txpool"]
#
# Refer to JSON RPC and https://book.getfoundry.sh/reference/anvil/
# ex,
#   'ALLOWED_RPC_METHODS': ["evm_mine"] # allowing mining blocks

CONFIG = {
    'FLAGS': '',
    'MNEMONIC': 'salad wrong armed concert evolve clock alter pledge run scout person essay', # ex: salad wrong armed concert evolve clock alter pledge run scout person essay
    'RUNNABLES': [],
    'ALLOWED_RPC_METHODS': []
}