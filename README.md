# Halborn ETH CTF Template

## Requirements

- Docker
- Brownie

## Description

To create a new challenge use this repository as a base:

- The `public` folder will be copied into the challenge container and all players will have access to all files present there.
- The `private` folder can be used to store solutions or walkthroughs.


The `public/scripts/challenge.py` does contain a minimal example of the required functions to:

- Deploy a new challenge
- Check if the challenge was solved


If the challenge does make use of real chain data, aka forking, you can define the `RPC` and `BLOCK_NUMBER` under `public/Dockerfile`.

The challenge details that will be displayed on the ctf page can be found under `challenge.yml` and should be edited acordingly.


## Developing

- Add a new network on brownie:

```
brownie networks add ctf dev host="http://127.0.0.1:8545" chainid=1337
```

- Create/copy your contracts under `public/contracts`
- Launch your `ganache-cli` or `anvil`:


```
# Ganache
ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --miner.blockGasLimit 12000000

# Anvil
anvil --block-base-fee-per-gas 0 -a 10
```

If you need to fork a network:

```
# Ganache
ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --miner.blockGasLimit 12000000 --fork.url $RPC --fork.blockNumber $BLOCK_NUMBER

# Anvil
anvil --block-base-fee-per-gas 0 -a 10 -f $RPC --fork-block-number $BLOCK_NUMBER
```

- If you did fork the network make sure the same information is under `public/Dockerfile`


- `cd public` and run the brownie console:

```
brownie console --network dev
```

- Inside the console deploy the challenges:

```
>>> run('challenge', 'deploy')
```

- Verify if the challenge is solved:

```
>>> run('challenge', 'solved')
(False, "Need more coins!")
```

You can create your own solution script under `public/scripts/script_name.py` and execute it under the console with:

```
>>> run('script_name')
```

An example can be the following:

```
# public/scripts/solve.py

from brownie import *

def main():
    a[0].transfer(Test[-1], 10)
```

> Remember to move the solution script to `private` when done


Deploying, checking solved, solving and verifying:

```
>>> run('challenge', 'deploy')
>>> run('challenge', 'solved')
(False, "Need more coins!")
>>> run('solve')
>>> run('challenge', 'solved')
(True, "Solved!")
```

- Modify the `challenge.yml`