# webgen
A Python library for generating and manipulating html, css and javascript files.

## Example
### Hello World Page
```python
from webgen import dom, filegen as fg

html = dom.HTML()
head = dom.Head()
body = dom.Body()
# To add head and body elements to html we pass them as parameters while calling html
html(head, body)

title = dom.Title('Hello World')
head(title)

# To add one element to another we can also do it on initialization
paragraph = dom.P('Hello World!')
body(dom.Div(paragraph))

# When we want to create an HTML file, we first initialize it with following parameters:
#   1) Path to file ('' means local directory)
#   2) Name of our file
#   3) Our dom.HTML instance
homepage = fg.HTML('', 'helloworld', html)

# To create our file we use the build() method
homepage.build()

# We can also automatically open the file after it's built
homepage.openhtml()

```

This will give us an html file with following contents: 
```html
<!doctype html>
<html>
<head>
<title>Hello World</title>
</head>

<body>
<div>
<p>Hello World!</p>
</div>
</body>
</html>

```
