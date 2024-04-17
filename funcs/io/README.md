# IO Shortcuts
Python code a functions for copying into other programs.


## .npy Files
```python
import numpy as np

# Input
numpy_array = np.load(file_name)
# If numpy array is dtype=object
numpy_array = np.load(file_name, allow_pickle=True)

# Output
np.save(file_name, numpy_array)
```

## .json Files

```python
import json

# Input
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

# Output
def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
```

## Image Files

```python
from PIL import Image
import numpy as np

def tiff_input(image_file):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(image_file)
    im.show()
    return np.array(img)
```

## .csv Files

```python
import csv

# Input
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f, delimter=' ')
        output = []
        for row in read_obj:
            try:
                temp = []
                for item in row:
                    temp.append(eval(row))
                output.append(temp)
            except:
                try:
                    output.append(eval(row))
                except:
                    try:
                        output.append(row)
                    except:
                        output = row    
    f.close()
    return output

# Output
def csv_output(file_name, data_send):
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return
```