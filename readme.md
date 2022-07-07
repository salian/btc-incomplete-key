## Recover missing characters from an incomplete BTC key, without GPU.

Use randomization or brute force to recover a damaged BTC key. 

Does not convert every possible private key to an address. Instead, for speed, only tests the checksum of potential keys to see if the checksum is valid.

Supports compressed WIF keys. 

### Requirements:

Say you have a damaged BTC key with a few characters missing.

Mask the BTC key to the correct expected length, with asterisks (`*`) to indicate the number and positions of missing characters.

For example if you have a hex key which should be 64 characters, and you are missing the _first five_ characters. Your masked key should then start with 5 asterisks (*) indicating the 5 missing characters and their locations. 

Eg. `*****aacf90d9f4aadd8c92e4b2562e1d9eb97f0df9ba3b508258739cb013db2`

#### Benchmarks 

#### On a 2.9 GHz Dual-Core Intel Core i5:
(_Needs to be updated for Hex and WIF keys_)

| Missing Characters | Maximum Time To Recover a WIF Key |
|--------------------|-----------------------------------|
| 4                  | 4 minutes                         |
| 5                  | 2 hours                           |
| 6                  | 74 hours                          |

### Examples

#### Recover a WIF key with an unknown address

`main.py --maskedkey=L5EZftvrYaSudiozVRzTqLcHLNDo***H5HSfM9BAN6tMJX8oTWz6`

#### Recover a WIF key with a known address

`main.py --maskedkey=L5EZftvrYaSudiozVRzTqLcHLNDo***H5HSfM9BAN6tMJX8oTWz6 --address=1EUXSxuUVy2PC5enGXR1a3yxbEjNWMHuem`

#### Recover a Hex key with a known address

`main.py --maskedkey=ef235aacf90d9f***dd8c92e4b2562e1d9eb97f0df9ba3b508258739cb013db2 --address=1EUXSxuUVy2PC5enGXR1a3yxbEjNWMHuem`

#### Try your luck at recovering a WIF key with many unknown letters

If missing more than 10 characters, use the _random_ mode to try randomly generated guesses instead of brute-forcing through a sequential list. In a GPU world, this gives CPU users a shot, if they are lucky, to beat the GPUs processing the keyspace sequentially.

`main.py --maskedkey=L5EZftvrYaSudiozVRzTqLcHLNDo***H5HSfM9BAN6tMJX8oTWz6 --address=1EUXSxuUVy2PC5enGXR1a3yxbEjNWMHuem --mode=random`

### Installation

#### Requires Python 3.10 or above

If you don't have Python 3.10 or above, download and install it from the official website: https://www.python.org/downloads/

#### Virtual Environment

Download all the project files from github into a directory, or pull them using git.

#### Virtual Environment and Dependencies

##### Create a new virtual environment 

In your Terminal or Command prompt, navigate to the project folder and create a Virtual Environment.
For more about virtual environments, consult the documentation: https://docs.python.org/3/library/venv.html

`python -m venv /path/to/new/virtual/environment`

##### Activate your new virtual environment 

###### On Mac/Linux: 
In the Terminal `source <path_to_venv>/bin/activate`

###### On Windows:
In cmd.exe:

`<venv>\Scripts\activate.bat`

In Powershell:

`<venv>\Scripts\Activate.ps1`


##### Install the dependencies within your virtual environment.

`pip install -r requirements.txt`

This should install all the required libraries within the virtual environment, without cluttering your system installation of python.

#### Run the program 

Run the program from within the virtual environment with dependencies installed

Navigate to the project folder which contains `main.py` and run

`python main.py --help`

If the installation went correctly, this should show a help screen with the allowed command-line options.

### Arguments Reference

```
usage: main.py [-h] [--maskedkey MY**KEY] [--address ADDRESS]
               [--fetchbalances]

Recover incomplete or damaged BTC private keys

options:
  -h, --help           show this help message and exit
  --maskedkey MY**KEY  private key with unknown characters replaced by *
  --address ADDRESS    the target BTC address if known
  --fetchbalances      display BTC balance for potential addresses (slower)
```

