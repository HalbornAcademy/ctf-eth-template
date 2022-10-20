from brownie import *

# Used for save_accounts and restrict_accounts
from ctf import *

# Deploys the challenge using brownie
# You have 10 accounts already funded to deploy the challenge

# save_accounts does save the account nonces to restrict
# the usage on solved function
@save_accounts(accounts)
def deploy():
    Test.deploy({'from': accounts[9]})

# This function should return a tuple of 2 values
# - First value is a boolean, if the challenge was solved or not
# - Second value is a message to display on the CTF platform

# restrict_accounts does verify that the given accounts have not been used
# otherwise the challenge is considered unsolved
@restrict_accounts([accounts[9]])
def solved():
    if Test[-1].balance() > 0:
        return True, "Solved!"
    else:
        return False, "Need more coins!"
