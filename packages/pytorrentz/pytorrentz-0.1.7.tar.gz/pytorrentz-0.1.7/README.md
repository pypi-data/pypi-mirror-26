Basic Python module for searching torrentz.eu -- based on https://github.com/dannvix/torrentz-magdl

**To install:**

```$ pip install pytorrentz```

Usage:
```python
>>> import pytorrentz

# Get list of torrents
# Optional args:
#   quality -- 'any' | 'good' | 'verified'
#   order   -- 'peers' | 'size' | 'date' | 'rating'
#   limit   -- Maximum number of results to return
>>> search = pytorrentz.search('example query', quality='good', order='peers', limit=20)

>>> import webbrowser
>>> magnet = search[0].get_magnet_uri()
>>> webbrowser.open(magnet)
```

**Torrent class properties:**
```
Torrent.sha1
Torrent.title
Torrent.date
Torrent.size
Torrent.seeds
Torrent.peers
```
