# NuDB
## Install
```bash
pip install nudb
```

## Usage

## Format
+ GAIS record(text)
	+ Field start with '@'
	+ field and value are separated by ':'
	+ field-value pairs are seprated by '\n'
	+ For example:
	```python
	data = "@id:1\n@name:First\n@url:http://www.google.com"
	```
+ JSON

## Import
```python
from nudb import NuDB

nudb = NuDB()
```

## Connect to NuDB
```python
nudb.connect('host', 'port', 'db')
```

## Put record
```python
# json format
result = nudb.rput(data, 'json')

# text format
result = nudb.rput(data, 'text', recBeg)
```

## Put record by file
```python
# json format
result = nudb.fput(filePath, 'json')

# text format
result = nudb.fput(filePath, 'text', recBeg)
```

## Get record by rid
```python
result = nudb.rget(rid)
```

## Delete record by rid
```python
result = nudb.rdel(rid)
```

## Update record by rid
```python
# json format
result = nudb.rupdate(rid, data, 'json')

# text format
result = nudb.rupdate(rid, data, 'text')
```

## Search
```python
result = nudb.search(query)
```
