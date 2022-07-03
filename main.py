import json
import string
import secrets
from typing import Generator
from random import SystemRandom as RND
import re
import trotter
from tqdm import tqdm
from time import sleep
from hdwallet import HDWallet
from hdwallet.symbols import BTC
from btc_com import explorer as btc_explorer

# test key: 'L5EZftvrYaSudiozVRzTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# test mask: 'L5EZftvrYaSu****VRzTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# corresponding address: '1EUXSxuUVy2PC5enGXR1a3yxbEjNWMHuem'

# masked_key = 'L5EZftvrYaSu******zTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# masked_key = 'L5EZftvrYaSu************LNDoVn7H5HSfM9BAN6tMJX8oTWz6'
masked_key = 'L5EZftvrYa*udiozVRzTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'

# Masked_key should be like 'L5EZftvrYaSu****V*zTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# with asterisks replacing unknown characters. Positions of unknown characters MUST be known.


def complete_key(masked_key_string, missing_letters):
    # Usage: print(complete_key("secret_password_***_is_secret", 'swordfish'))
    for letter in missing_letters:
        masked_key_string = masked_key_string.replace('*', letter, 1)  # replace each asterisk with a letter once
    # print(f"masked_key_string: {masked_key_string}")
    return masked_key_string


def fetch_balance_for_btc_address(btc_address):
    # Get BTC balance from web API. This is rate limited
    address_info = btc_explorer.get_address(btc_address)
    sleep(.25)  # To play nice with the API Rate limit - recommend sleep(10)
    return address_info.balance, address_info.tx_count


def btc_address_from_private_key(my_secret, secret_type='WIF'):
    assert secret_type in ['WIF', 'classic', 'extended', 'mnemonic', 'mini']
    hdwallet = HDWallet(symbol=BTC)
    match secret_type:
        case 'WIF':
            hdwallet.from_wif(wif=my_secret)
        case 'classic':
            hdwallet.from_private_key(private_key=my_secret)
        case 'mnemonic':
            raise "Mnemonic secrets not implemented"
        case 'mini':
            raise "Mini private key not implemented"
        case 'extended':
            hdwallet.from_xprivate_key(xprivate_key=my_secret)
        case _:
            raise "I don't know how to handle this type."

    # Uncomment to print all Bitcoin HDWallet info
    # print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))

    return hdwallet.p2pkh_address()


if __name__ == '__main__':
    missing_length = masked_key.count('*')
    print(f"Looking for {missing_length} characters in {masked_key}")
    allowed_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" as keys are case-sensitive
    missing_letters_master_list = trotter.Amalgams(missing_length, allowed_characters)
    # print(missing_letters_master_list)
    # print(len(missing_letters_master_list))
    # print(missing_letters.index("abcdefghijkl"))

    for i in tqdm(range(len(missing_letters_master_list))):
        potential_key = complete_key(masked_key, missing_letters_master_list[i])
        try:
            address = btc_address_from_private_key(potential_key, secret_type='WIF')
            # print(address)
            balance, tx_count = fetch_balance_for_btc_address(address)
            print(f"key: {potential_key} address: {address} tx_count: {tx_count} balance: {balance}")
        except ValueError:
            # Address Checksum Failed
            pass


