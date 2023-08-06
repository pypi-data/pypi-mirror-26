#### To install:
`$ pip install pyzooqle`

#### Usage
```python
>>> import pyzooqle
>>> s = pyzooqle.search('search query')
>>> s
[
<Torrent(title='result 1')>,
<Torrent(title='result 2')>
]
>>> s[0].title
u'result 1'
>>> s[0].size
123.4
>>> s[0].seeds
234
>>> s[0].leechers
456
>>> s[0].magnet
u'magnet:?xt=urn:btih:......'
```
#### Optional parameters
See zooqle.py for all permissible values for these parameters.
```python
pyzooqle.search('search query',
                sort=SORT.ADDED,
                order=ORDER.DESCENDING)
```
