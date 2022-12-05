# Halborn ETH CTF Template

## Requirements

- Brownie
- Docker (optional)

## Description

To create a new challenge use this repository as a base:

- It is a standard brownie project folder with `/contracts` and a default `brownie-config.yaml` config for you to modify.
- The `scripts/private` folder can be used to store solutions or walkthroughs.
- The challenge details that will be displayed on the ctf page can be found under `challenge.yml` and should be edited acordingly.
- If the challenge does make use of real chain data, aka forking, you can define the information under the CONFIG variable of the `scripts/challenge.py` file.

There are 2 `challenge.py` files, used to deploy and manage the challenge, one under `scripts` and the other under `scripts/private`. The former, called PUBLIC will be exposed to the player as part of the CTF challenge files. It allows to set the configuration and settings for the player node instance, the one the player will connect to.

> If you need private deployments or perform private runnable actions you can modify the `scripts/private/challenge.py` file instead. This file will be hidden from the player and never exposed on the CTF platform.

All functions, including runnables, defined under `challenge.py` take 3 arguments by default:

```
- deployer: Those accounts should be used to deploy the challenge, you can think of them as being
            the "admin" accounts. They will be restricted by default, even if
            the player is capable of obtaining the private key, sending
            any transaction from those addresses will cause an exception on the backend.

            You MUST set a MNEMONIC under scripts/private/challenge.py (CONFIG["MNEMONIC"])
            default: 10 accounts

- player:   Those accounts are randomly generated unless specified under
            scripts/challenge.py (CONFIG) by setting the MNEMONIC.
            default: 10 accounts

- state:    This is a dictionary container that allows you to store anything you would require
            in any other function, such as runnables or "solved". For example, you could be using
            the state variable under a runnable to check for certain condition to be meet. Once this
            condition in met you could set an entry under the state variable to some value and check
            it under the "solved" function to display a different message, or solve the challenge.
```

> You can set the default balance by changing the FLAGS of the CONFIG either on the PUBLIC or PRIVATE config, depending if you want different balance on the deployer accounts or the player accounts.

## Developing

- Create/copy your contracts under `contracts` and develop your deployment scripts

- Execute the following command under a separated terminal to start the development environment. This environment will run the deployment scripts and take all the configurations as the real platform would doo. Runnables are also supported and executed:

```
./dev.py
```

Once you see the following without any error, the dev environment is ready to play and the deployment was successful.

```
================================
DEPLOYMENT READY

{
    "Test": [
        "0xaE5971a1b501755d2c830f59609b90CD6aa08eD7"
    ]
}

MNEMONIC: away despair village call pipe cement banner motor tomato know pitch crime
================================
```

> Notice that the reported addresses are the ones the player will be given on the CTFd platform and the mnemonic is the player mnemonic.

- Connect to `http://127.0.0.1:8545` or run `brownie console` on the same folder. (Use the player mnemonic if your RPC client does not fetch the accounts)
- On the terminal that the `dev.py` script was executed you can check if the challenge was solved by pressing the return key: 
    - The dev environment will take care of sending the correct state, deployment and player accounts.

```
================================
Check solved? <RETURN>

Running 'scripts/challenge.py::solved'...
[
    false,
    "Need more coins!"
]
Check solved?
```

- Modify the `challenge.yml`

# Check container

Once the challenge is fully coded it is a good idea to make sure the docker image does build and deploys the challenge successfully:

```
cd public
docker build . -t challenge-dev
docker run -p 8545:80 --rm challenge-dev
```

If no errors are shown the challenge is ready!

- Try to run the solve script against the `http://127.0.0.1:8545` instance created by the previous docker run.
- Get details with `curl http://127.0.0.1:8545/details`

# Tricks

You can disable mining by calling this method:

```
web3.provider.make_request("evm_setAutomine", [False])
```