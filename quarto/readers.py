"""
File readers and path finders.
"""
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from urllib.parse import quote

def querypage(page):
    """ dict or None: Page options if they exist. """
    path = page.with_suffix('.json')
    if path.is_file():
        with open(path) as file:
            return jsonload(file)

def readlines(*paths):
    """ Iterator[str]: Read lines from text file(s). """
    for path in paths:
        with open(path) as lines:
            yield from lines

def stylesheet(folder):
    """ str: Concatenated stylesheets from sorted CSS files in a folder. """
    return ''.join(readlines(*sorted(Path(folder).glob('**/*.css'))))

def tidybody(page):
    """ str: Cleaned elements of page <body>. """
    raise NotImplementedError

def urlpath(page,path):
    """ str: URL-encoded relative path from page to local file. """
    return quote(relpath(path,start=page.parent))
