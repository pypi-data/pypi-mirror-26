Windows RBS Parser
==================

Parses windows diagnostics rbs files.

Currently supported are version 3 and 5 files (starting with UTCRBES3 and UTCRBES5).
Not all parts of the file structure are currently known, but the content of each
item can be extracted.

Example
-------

```python
from rbs_parser import RBSFile

with RBSFile("events10.rbs") as rbs:
        for item in rbs:
            print('#####################')
            print("Offset: 0x{0:x} {0}".format(item.offset))
            print("Size: 0x{0:x} {0}".format(item.size))
            print("Data:", item.uncompressed.decode())
```

Dependencies
------------

Tested and developed with python3.
Dependes on my [helperlib](https://pypi.python.org/pypi/helperlib/0.4.1).