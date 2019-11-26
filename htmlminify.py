import htmlmin
import os

def minify(path):
    """write the minified html to the original file"""
    with open(path, 'r') as page:
        page_con = page.read()
    print("Minifying %s" % path)
    minified = htmlmin.minify(page_con)
    with open(path, 'w') as writer:
        writer.write(minified)

for root, dirs, files in os.walk("dist"):
    for thing in files:
        if thing.endswith(".html"):
            minify(os.path.join(root, thing))