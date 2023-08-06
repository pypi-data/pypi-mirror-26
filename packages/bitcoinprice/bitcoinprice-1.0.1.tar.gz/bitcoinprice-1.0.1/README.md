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

print(bitcoinprice.get_price())

```

Sample Output:
```
{'high': '8036.30', 'last': '8018.00', 'timestamp': '1511121769', 'bid': '8015.01', 'vwap': '7829.96', 'volume': '8105.21128436', 'low': '7675.00', 'ask': '8018.00', 'open': '7775.55'}
```

Simple price:

```python

import bitcoinprice 

print(bitcoinprice.get_price_simple())

```

Sample Output:
```
8018.00

```

## Test

```bash
python -m unittest -v tests/testbitcoinprice.py
```

