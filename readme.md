## Recover missing characters from a BTC key, without GPU.

Use randomization or brute force to recover a damaged BTC key. 

Does not convert every possible private key to an address. Instead, for speed, only tests the checksum of potential keys to see if the checksum is valid.

Supports compressed WIF keys. 

### Requirements:

Have a damaged BTC key with a few characters missing.

#### Benchmarks 

#### On a 2.9 GHz Dual-Core Intel Core i5:

| Missing Characters | Maximum Time To Recover a WIF Key |
|--------------------|-----------------------------------|
| 4                  | 4 minutes                         |
| 5                  | 2 hours                           |
| 6                  | 74 hours                          |

### Usage:

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

