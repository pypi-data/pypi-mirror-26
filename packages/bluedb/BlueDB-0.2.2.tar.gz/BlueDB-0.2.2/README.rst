BlueDB v0.2
*******************

::
>>> from BlueDB import Blue
>>> database = Blue('database')
>>> database['key'] = {'nested key': 'nested value'}
>>> print(database['key']['nested key'])
nested value
>>> database['key']['nested key'] = 'new value'
>>> print(database)
{'key': {'nested key': 'new value'}}
