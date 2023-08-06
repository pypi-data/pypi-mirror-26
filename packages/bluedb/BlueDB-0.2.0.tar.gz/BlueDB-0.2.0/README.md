# BlueDB
*use my database, is good!*

## Examples
```python
from BlueDB import *

db = Blue('database')

db['key'] = 'value'
print(db['key'])

db['key'] = {}
db['key']['another key'] = 'another value'
print(db)
db['key']['another key'] = 'yet another value'
print(db)

>>> value
>>> {'key': {'another key': 'another value'}}
>>> {'key': {'another key': 'yet another value'}}
```
