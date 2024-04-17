# URL Shortcuts
Python code a functions for copying into other programs.

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