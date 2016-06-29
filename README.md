Congabonga Google Music Plugin
========================

Implements google music support. Requires Premium account.

Installation
------------
```
python3 setup.py bdist_wheel
```
then copy the wheel file in dist to `~/.local/share/congabonga/plugins/`

Configure
---------
Eit `~/.config/congabonga/library.cfg` and add
```
[gmusic]
username = <google username>
password = <google password>
```

