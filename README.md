# Robert's Python Library
Python code a functions for copying into other programs.

## Setup new python file for local storage

Make sure 'dev_setup.py' has been executed first.  
Will also require the load_json function below.

```python
json_data = load_json("local-data-path.json")
save_path = json_data["path"]

open_file_name = "/eq_indonesia_social_media.txt"
```


## Load and save json files

```python
import json

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)
```

## Get Paths
```python
input_file = "../active.txt"

# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location_upper = save_location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),".." ,"data", "sats")
if not os.path.exists(save_location):
    os.makedirs(save_location)
```

## In linux to open url

```python
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    
link = "https://example.com"

response = requests.get(link)

print(response.txt)
```

## Using beautiful soup

Open from url as above
```python
soup = BeautifulSoup(response, "html.parser")
```

Open from html file
```python
with open(save_path+open_file_name) as response:
	soup = BeautifulSoup(response, "html.parser")
```

Get URLs
```python
links = soup.find_all('a', href=True)
for i in range(len(links)):
	link = str(links[i]['href'])
```


### Matrix Reshape (matrix_reshape.py)
```python
coords, z = matrix_reshape_from_flat(grid_data, coord_dims, comp2d=True, plot_dims=[])
```

Inputs a matrix ```grid_data``` with dimensions M,N where there are N-1 coordinates given and 1 value at each coordinate. ```z``` output therefore has N-1 dimensions. Coords contains the corresponding values based on the input coordinates for each axis of ```z```.
