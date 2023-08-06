# bitcoinprice

Simply the easiest way to incorporate the current Bitcoin price into your application. 

### Install: 

```bash 
pip install bitcoinprice
```

### Usage:

Get the full price details:

```python

import bitcoinprice 

print(bitcoinprice.get_price('btc'))

```

Sample Output:
```
{'high': '8036.30', 'last': '8018.00', 'timestamp': '1511121769', 'bid': '8015.01', 'vwap': '7829.96', 'volume': '8105.21128436', 'low': '7675.00', 'ask': '8018.00', 'open': '7775.55'}
```

Simple price:

```python

import bitcoinprice 

print(bitcoinprice.get_price_simple('btc'))

```

Sample Output:
```
8018.00

```

# Coin Types: BTC, LTC, ETH 

By default, the price is returned in USD. To see euros add the parameter:

```bash
import bitcoinprice 

print(bitcoinprice.get_price_simple('btc')
print(bitcoinprice.get_price_simple('ltc')

```
# Currancy: Euro 

By default, the price is returned in USD. To see euros add the parameter:

```bash
import bitcoinprice 

print(bitcoinprice.get_price_simple('btc', 'eur'))
print(bitcoinprice.get_price_simple('eth', 'eur'))
print(bitcoinprice.get_price('ltc', 'eur'))

```
## Test

```bash
python -m unittest -v tests/testbitcoinprice.py
```

