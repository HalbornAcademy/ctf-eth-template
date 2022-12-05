#! /usr/bin/env python3

import os
import subprocess
from dataclasses import dataclass
from brownie import *
import eth_account
from eth_account.hdaccount import generate_mnemonic

from scripts.challenge import CONFIG as _PUBLIC_CONFIG
from scripts.private.challenge import CONFIG as _PRIVATE_CONFIG

import threading
import time
import socket
import json

from brownie.network.account import LocalAccount

INTERNAL_PORT = 8555
PLAYER_PORT = 8545
PLAYER_MNEMONIC = None

PROJECT = None

def wait_for_port(port: int, host: str = 'localhost', timeout: float = 5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port: Port number.
        host: Host address on which the port should exist.
        timeout: In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the port {} on host {} to start accepting '
                                   'connections.'.format(port, host)) from ex

def accounts_from_mnemonic(mnemonic, count=1, offset=0):

    _accounts = []

    for i in range(offset, offset + count):
        w3account = eth_account.Account.from_mnemonic(
            mnemonic, passphrase='', account_path=f"m/44'/60'/0'/0/{i}"
        )

        account = LocalAccount(w3account.address, w3account, w3account.key)
        _accounts.append(account)

    return _accounts



@dataclass
class AnvilData:
    port: str
    mnemonic: str
    rpc: str
    block: str
    extra: str


def anvil_run(data: AnvilData):
    cmd = f'anvil --accounts 10 --port {data.port} --block-base-fee-per-gas 0 --chain-id 1337'
    _args = cmd.split(' ')

    _args.append('--mnemonic')
    _args.append(data.mnemonic)

    if data.rpc != '':
        _args.append('--fork-url')
        _args.append(data.rpc)

    if data.block != '':
        _args.append('--fork-block-number')
        _args.append(data.block)

    if data.extra != '':
        _args.extend(data.extra.split(' '))

    process = subprocess.Popen(
        args=_args,
        stdout=subprocess.DEVNULL
    )

    return process

def ganache_run(data: AnvilData):
    _cmd = f'ganache-cli --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --hardfork istanbul --miner.blockGasLimit 12000000 -p "{data.port}"'
    _args = _cmd.split(' ')

    _args.append('--wallet.mnemonic')
    _args.append(data.mnemonic)

    if data.rpc != '':
        _args.append('--fork.url')
        _args.append(data.rpc)

    if data.block != '':
        _args.append('--fork.blockNumber')
        _args.append(data.block)

    if data.extra != '':
        _args.extend(data.extra.split(' '))

    process = subprocess.Popen(
        args=_args,
        stdout=subprocess.DEVNULL
    )

    return process


def run_main():
    data = AnvilData(
        port=INTERNAL_PORT,
        mnemonic=_PRIVATE_CONFIG.get('MNEMONIC'),
        rpc=_PUBLIC_CONFIG.get('RPC', ''),
        block=_PUBLIC_CONFIG.get('BLOCK_NUMBER', ''),
        extra=_PRIVATE_CONFIG.get('extra', ''),
    )
    try:
        p = anvil_run(data)
    except FileNotFoundError:
        p = ganache_run(data)

    p.wait()


def run_player():
    global PLAYER_MNEMONIC
    player_mnemonic = _PUBLIC_CONFIG.get("MNEMONIC", '').strip()
    if player_mnemonic == '':
        player_mnemonic = generate_mnemonic(12, "english")
    
    PLAYER_MNEMONIC = player_mnemonic
    data = AnvilData(
        port=PLAYER_PORT,
        mnemonic=player_mnemonic,
        rpc=f'http://127.0.0.1:{INTERNAL_PORT}',
        block='',
        extra=_PUBLIC_CONFIG.get('extra', ''),
    )
    try:
        p = anvil_run(data)
    except FileNotFoundError:
        p = ganache_run(data)

    p.wait()


STATE = {}

def deploy():
    global STATE, PROJECT, PLAYER_MNEMONIC
    network.connect()
    PROJECT = project.load('.')

    STATE = {}
    
    deployer = accounts_from_mnemonic(_PRIVATE_CONFIG.get('MNEMONIC'), count=10) 
    player = accounts_from_mnemonic(PLAYER_MNEMONIC, count=10) 

    project.run('private/challenge', 'deploy', [STATE, deployer, player])
    project.run('challenge', 'deploy', [STATE, deployer, player])

    def wrap(function, every):
        def wrapped_function(*args):
            function(*args)
            threading.Timer(every, wrapped_function, [*args]).start()
        return wrapped_function

    for _runnable in _PRIVATE_CONFIG.get('RUNNABLES', []) + _PUBLIC_CONFIG.get('RUNNABLES', []):
        _f, _every = _runnable
        wrap(_f, _every)(STATE, deployer, player)

def dump_project_deploy():
    global PROJECT
    obj = {}
    for key in PROJECT.keys():
        obj[key] = []
        for v in PROJECT[key]:
            obj[key].append(str(v))
    return obj

if __name__ == '__main__':

    threading.Thread(target=run_main, args=[]).start()
    wait_for_port(INTERNAL_PORT)

    threading.Thread(target=run_player, args=[]).start()
    wait_for_port(PLAYER_PORT)

    deploy()
    print('================================')
    print("DEPLOYMENT READY")
    print()
    print(json.dumps(dump_project_deploy(), indent=4))
    print()
    print(f'MNEMONIC: {PLAYER_MNEMONIC}')
    print('================================')



    while True:
        input('Check solved?')
        deployer = accounts_from_mnemonic(_PRIVATE_CONFIG.get('MNEMONIC'), count=10) 
        player = accounts_from_mnemonic(PLAYER_MNEMONIC, count=10) 
        result = project.run('challenge', 'solved', [STATE, deployer, player])
        print(json.dumps(result, indent=4))
