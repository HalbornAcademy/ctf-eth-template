from brownie import *

# A method returning a list of accounts restricted to use
# during challenge solving
def restricted_accounts:
    return [accounts[9]]

# Deploys the challenge using brownie
# You have 10 accounts already funded to deploy the challenge

def deploy():
    Test.deploy({'from': accounts[9]})

# This function should return a tuple of 2 values
# - First value is a boolean, if the challenge was solved or not
# - Second value is a message to display on the CTF platform

def solved():
    if Test[-1].balance() > 0:
        return True, "Solved!"
    else:
        return False, "Need more coins!"
