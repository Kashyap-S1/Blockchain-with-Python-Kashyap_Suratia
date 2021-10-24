This is a simple wallet that can send either testnet bitcoin or testnet ethereum crytpocurrencies to any counterpart address that in a network.The wallet user hd-wallet-derive php library, bit Python Bitcoin library and web3.py Python Ethereum library.It is comprised of 3 functions:

1.  derive_wallets: Uses mnemonics and hd-wallet-derive php libary to generate 3 children wallets for 3 Crypto currency networks Bitcoin (BTC), Bitcoin-testnet (BTCTEST), Ethereum (ETH)

2.  priv_key_to_account: Returns the address of a wallet given its corresponding private key

3.  create_tx: creates a transaction for a wallet

4.  send_tx: call create_tx, sign the transaction, then send it to the designated network

                Sample Usage:

5.  open a new windows cmd while in the project folder
6.  run command python to open python shell
7.  Within the python shell, run from wallet import \*

The project uses hd-wallet-derive php library , therefore the system must have PHP installed
Istallation instructions are as follows:

1. cd into the project folder and clone the library by git clone https://github.com/dan-da/hd-wallet-derive
2. open git bash as an Administrator
3. cd into hd-wallet-derive
4. php -r "readfile('https://getcomposer.org/installer');" | php
5. php composer.phar install

For python dependecies, the project is run under python virtual environment,
to get started run pip3 install -r requirements.txt to install all the required dependeicies

                                    SAMPLE TRANSACTIONS

Funding one of the BTCTEST wallet addresses(n2CwrS7A9m2KFXzNR9iP8T48B1a3tGhxcZ), results to image image1.png.

Addresses for the generated testnet addresses is shown on image2.png

sending a transaction into another testnet address,
send_tx(BTCTEST,btc_acc,'mx57HViz23LDXTLHSb8jpBgKpDrdiAv7Lg',0.00002), for the result is captured on image3.png.
