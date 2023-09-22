# Articulo
Tiny library for html articles parcing.

## Usage
Basic usage
```python
from articulo import Articulo

# Step 1: initializing Articulo instance
article = Articulo('https://info.cern.ch/')

# Step 2: getting article properties. All properties resolves lazily.
print(article.title) # title property returns article title as a string
print(article.text) # text property returns article content as a string
print(article.markup) # markup property returns article content as an html markup string
```