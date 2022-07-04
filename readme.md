## Recover missing characters from a BTC key, without GPU.

Use randomization or brute force to recover a damaged BTC key. 

Does not convert every possible private key to an address. Instead, for speed, only tests the checksum of potential keys to see if the checksum is valid.

Supports compressed WIF keys. 

### Requirements:

Have a damaged BTC key with a few characters missing.

#### Benchmarks on a 2.9 GHz Dual-Core Intel Core i5:

| Missing Characters | Maximum Time To Recover |
|--------------------|-------------------------|
| 4                  | 4 minutes               |
| 5                  | 2 hours                 |
| 6                  | 74 hours                |

### Todo:

- Add multithreading support to fully utilize CPU.
