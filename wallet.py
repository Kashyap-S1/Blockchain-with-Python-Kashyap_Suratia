import subprocess
import json
from dotenv import load_dotenv
import os
import subprocess 
import json

from dotenv import load_dotenv

from constants import *
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from bit import *
from web3 import Web3
from eth_account import Account 

from web3.middleware import geth_poa_middleware
from web3 import Web3


# to establish connection with ethereum local network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

load_dotenv()
# Loads mnemonic and as an environment variable
mnemonic=os.getenv("mnemonic")


def derive_wallets(mnemonic, coin, numderive):
    """Function to derive children wallets based on mnemonic phrase input,
      Use the subprocess library to call the php file script from Python"""
    command = f'php ./derive -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' 
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# coin object to hold child wallets
coins = {"eth", "btc-test", "btc"}
numderive = 3
#creates keys dictionarry
keys = {}
for coin in coins:
    keys[coin]= derive_wallets(os.getenv('mnemonic'), coin, numderive=3)

# Creating a private keys object
eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']


print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(keys, indent=4, sort_keys=True))


def priv_key_to_account(coin, priv_key):
    """A function that returns the address of a wallet given its corresponding private key"""
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


eth_acc = priv_key_to_account(ETH,eth_PrivateKey)
btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)


def create_tx(coin, account, to, amount):
    """function that creates the transaction for a  wallet (it only signs the order)"""
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "to": to,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId": w3.net.chainId 
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)]) 


def send_tx(coin, account, to, amount):
    """call create_tx, sign the transaction, then send it to the designated network"""
    if coin == ETH: 
        raw_tx = create_tx(coin,account, to, amount)
        sign = account.signTransaction(raw_tx)
        result = w3.eth.sendRawTransaction(sign.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        trx_btctest= create_tx(coin,account,to,amount)
        sign_trx_btctest = account.sign_transaction(trx_btctest)
        from bit.network import NetworkAPI
        NetworkAPI.broadcast_tx_testnet(sign_trx_btctest)       
        return sign_trx_btctest
       