# Halborn ETH CTF Template

## Requirements

- Brownie
- Docker (optional)

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

- Create/copy your contracts under `public/contracts`
- Launch your `ganache-cli` or `anvil`, make sure to use the same mnemonic as the server:

```
# Ganache
ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --miner.blockGasLimit 12000000 --wallet.mnemonic "test test test test test test test test test test test junk"

# Anvil
anvil --block-base-fee-per-gas 0 -a 10 --mnemonic "test test test test test test test test test test test junk"
```

If you need to fork a network:

```
# Ganache
ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --miner.blockGasLimit 12000000 --fork.url $RPC --fork.blockNumber $BLOCK_NUMBER --wallet.mnemonic "test test test test test test test test test test test junk"

# Anvil
anvil --block-base-fee-per-gas 0 -a 10 -f $RPC --fork-block-number $BLOCK_NUMBER --mnemonic "test test test test test test test test test test test junk"
```

- If you did fork the network make sure the same information is under `public/Dockerfile`


- `cd public` and run the brownie console:

```
brownie console
```

- Inside the console deploy the challenge:

```
>>> run('challenge', 'deploy')
```

- Verify if the challenge was solved:

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


Once the challenge is fully coded it is a good idea to make sure the docker image does build and deploys the challenge successfully:

```
cd public
docker build . -t challenge-dev
docker run --rm challenge-dev
```

If no errors are shown the challenge is ready!

