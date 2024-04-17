# Robert's Python Library
Python code a functions for copying into other programs.

Libraries
- [IO](./funcs/io)
- [URL](./funcs/url)
- [Dev Stuff](./dev)


## Paths
```python
import os

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ,"data", "sats")
if not os.path.exists(save_location):
    os.makedirs(save_location)
    # or
    raise Exception("This file does not exist")
```
