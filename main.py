# import json
# import secrets
import string
# from typing import Generator
# from random import SystemRandom as RND
# import re
import argparse
import sys

import trotter
from tqdm import tqdm
from time import sleep
from hdwallet import HDWallet
from hdwallet.symbols import BTC
from btc_com import explorer as btc_explorer

# test key: 'L5EZftvrYaSudiozVRzTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# test mask: 'L5EZftvrYaSudiozVRzTqLcHLNDo***H5HSfM9BAN6tMJX8oTWz6'
# test key:  'ef235aacf90d9f4aadd8c92e4b2562e1d9eb97f0df9ba3b508258739cb013db2'
# test mask: 'ef235aacf90d9f***dd8c92e4b2562e1d9eb97f0df9ba3b508258739cb013db2'
# corresponding address: '1EUXSxuUVy2PC5enGXR1a3yxbEjNWMHuem'

# Masked_key should be like 'L5EZftvrYaSu****V*zTqLcHLNDoVn7H5HSfM9BAN6tMJX8oTWz6'
# with asterisks replacing unknown characters. Positions of unknown characters MUST be known.


def write_to_log(data):
    with open("output_log.txt", "a") as file:
        file.write(data + '\n')


def complete_key(masked_key_string, missing_letters):
    # Usage: print(complete_key("secret_password_***_is_secret", 'swordfish'))
    for letter in missing_letters:
        masked_key_string = masked_key_string.replace('*', letter, 1)  # replace each asterisk with a letter once
    # print(f"masked_key_string: {masked_key_string}")
    return masked_key_string


def fetch_balance_for_btc_address(btc_address):
    # Get BTC balance from web API. This is rate limited
    address_info = btc_explorer.get_address(btc_address)
    sleep(1.25)  # To play nice with the API Rate limit - recommend sleep(10)
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


def parse_arguments():
    cli_argument_parser = argparse.ArgumentParser(
        description='Recover incomplete or damaged BTC private keys',
        epilog="© Pranab Salian, 2022 - All rights reserved."
    )
    cli_argument_parser.add_argument("--maskedkey", help="private key with unknown characters replaced by *", metavar="MY**KEY", default=None)
    cli_argument_parser.add_argument("--address", help="the target BTC address if known", default=None)
    cli_argument_parser.add_argument("--fetchbalances", help="display BTC balance for potential addresses (slower)", action='store_true', default=False)
    cli_argument_parser.add_argument("--mode", help="sequential or random", default='sequential', choices=['sequential', 'random'])
    # cli_argument_parser.add_argument("--resetthreshold", type=int, help="number of times to retry before skipping", default=3)
    # cli_argument_parser.add_argument("--silent", help="do not output to stdout", action='store_true', default=False)
    # cli_argument_parser.add_argument("--verbose", help="extra-detailed output to stdout", action='store_true', default=False)

    namespace_arguments = cli_argument_parser.parse_args()
    # cli_argument_parser.print_help()  # Uncomment to review the args

    # Exit if no masked key was provided
    if namespace_arguments.maskedkey is None:
        cli_argument_parser.print_help()
        cli_argument_parser.exit("Error: No masked key was provided.")

    return namespace_arguments


# Having cli_arguments as a global, defined at module level
# seems most compatible with multiprocessing and windows
cli_arguments = parse_arguments()

if __name__ == '__main__':
    masked_key = cli_arguments.maskedkey
    target_address = cli_arguments.address
    fetch_balances = cli_arguments.fetchbalances
    mode = cli_arguments.mode
    missing_length = masked_key.count('*')
    key_length = len(masked_key)
    print(f"Looking for {missing_length} characters in {masked_key} to match address {target_address}")
    match key_length:
        case 51 | 52:
            secret_type = 'WIF'
            allowed_characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'  # Base 58 Alphabet w/o 0, O, I
        case 64:
            # Hex
            secret_type = 'classic'
            allowed_characters = string.digits + "ABCDEF"
        case 111:
            # Extended Private Key
            secret_type = 'extended'
            allowed_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        case _:
            # Unknown Length
            secret_type = 'unhandled'
            allowed_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits

    missing_letters_master_list = trotter.Amalgams(missing_length, allowed_characters)
    # print(missing_letters_master_list)
    # print(len(missing_letters_master_list))
    # print(missing_letters.index("abcdefghijkl"))
    #

    try:
        # print(missing_letters_master_list)
        max_loop_length = len(missing_letters_master_list)
    except OverflowError:
        max_loop_length = sys.maxsize
        if mode == 'sequential':
            print(f"Warning: Some letters will not be processed in sequential mode because "
                  f"the possible space is too large. Try random mode.")

    for i in tqdm(range(max_loop_length)):
        if mode == 'sequential':
            potential_key = complete_key(masked_key, missing_letters_master_list[i])
        elif mode == 'random':
            # random_index = secrets.randbelow(len(missing_letters_master_list))  # OverflowError
            # random_index = secrets.choice(missing_letters_master_list)  # OverflowError
            potential_key = complete_key(masked_key, missing_letters_master_list.random())

        try:
            # This will fail with a ValueError if the potential key checksum
            address = btc_address_from_private_key(potential_key, secret_type=secret_type)

            # print(potential_key, ':', address)
            if target_address:
                # We wish to match the address with an expected output address
                if address != cli_arguments.address:
                    continue

            print(f"key: {potential_key} address: {address}")
            if fetch_balances:
                # We wish to fetch BTC account balances from the internet
                balance, tx_count = fetch_balance_for_btc_address(address)
                print(f"tx_count: {tx_count} balance: {balance}")

            write_to_log(f"key: {potential_key} address: {address}")

        except ValueError:
            # Address Checksum Failed
            pass


