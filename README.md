# Robert's Python Library
Python code a functions for copying into other programs.

Libraries
- [IO](./funcs/io)
- [Graphics](./funcs/graphics)
- [URL](./funcs/url)
- [Dev Stuff](./dev)


## Drop into Colab

```python
!git clone --depth=1 git://0x365/py-tools py_tools
!rm -rf ./py_tools/.git
!pip install -r requirements.txt
from py_tools.commons import *
```

## Paths
```python
import os

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ,"data", "sats")
if not os.path.exists(save_location):
    os.makedirs(save_location)
    # or
    raise Exception("This file does not exist")
```
