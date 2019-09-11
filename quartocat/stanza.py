"""
Each function in this module generates a group of lines.

INPUTS
    paths   Tuple[Path]: Absolute paths to raw pages, home first.
    i       int: Which page are we generating?
    kwargs  All other inputs must be optional keyword arguments.

OUTPUTS
    Iterable[str]: Lines of HTML. (Newline characters will be added later.)
"""
from datetime import datetime
from posixpath import join as urljoin

from .reader import readlines, urlpath

CSSPATH = "style.css"
YEAR = datetime.now().year

def generate(paths, i, title="", **kwargs):
    """ Iterator[str]: All lines in page. """

    yield "<!DOCTYPE html>"
    yield "<html>"
    yield from head(paths, i, **kwargs)
    yield "<body>"
    yield from nav(paths, i, **kwargs)
    yield from main(paths, i, **kwargs)
    yield from icons(paths, i, **kwargs)
    yield from klf(paths, i, **kwargs)
    yield from last(paths, i, **kwargs)
    yield from js(paths, i, **kwargs)
    yield "</body>"
    yield "</html>"

def head(paths,
    i,
    author='',
    baseurl="",
    description='',
    favicon='',
    generator='',
    keywords='',
    title='',
    **kwargs):
    """
    Iterator[str]: <head> element.
    """
    home, page = paths[0], paths[i]

    link = '<link rel="{}" href="{}">'.format
    meta = '<meta name="{}" content="{}">'.format

    yield '<head>'

    yield '<title>'
    yield title or page.stem.replace('_',' ')
    yield '</title>'

    yield link("stylesheet", urlpath(page, home.parent / CSSPATH))
    if baseurl:
        yield link("home", baseurl)
        yield link("canonical", urljoin(baseurl, urlpath(home, page)))
    if favicon:
        yield link("icon", urlpath(page, home.parent / favicon))

    yield '<meta charset="utf-8">'
    yield meta("viewport", "width=device-width, initial-scale=1.0")
    yield meta("author", author)
    yield meta("description", description)
    yield meta("generator", generator)
    yield meta("keywords", keywords)

    yield '</head>'

def icons(paths, i, iconlinks=(), **kwargs):
    """ Iterator[str]: <section id="icons"> lines. """
    home, page = paths[0], paths[i]

    atag = '<a href="{}" rel="{}">{}</a>'.format
    image = '<img alt="{}" src="{}" height=32 width=32 title="{}">'.format

    yield '<section id="icons">'
    yield atag(urlpath(page, paths[(i - 1) % len(paths)]), "prev", "«")

    for alt, src, href in iconlinks:
        src = urlpath(page, home.parent / src)
        yield atag(href, "external", image(alt, src, alt))

    yield atag(urlpath(page, paths[(i + 1) % len(paths)]), "next", "»")
    yield "</section>"

def js(paths, i, javascripts=(), **kwargs):
    """ Iterator[str]: Client-side JavaScript goes here. """
    yield from javascripts

def klf(paths, i, copyright="", email="", license="", license_url="", **kwargs):
    """ Iterator[str]: <section id="klf"> lines. """

    liclink = '<a href="{}" rel="license">{}</a>'.format
    spantag = '<span id="{}">{}</span>'.format

    yield '<section id="klf">'
    if copyright:
        yield spantag('copyright', "© {} {}.".format(copyright,YEAR))
    if license_url:
        license = liclink(license_url, license or "LICENSE")
    if license:
        yield spantag(license)
    if email:
        yield from ('<address>', email, '</address>')
    yield "</section>"


def last(paths, i, updog="", **kwargs):
    """ Iterator[str]: Any last words? """
    yield f'<a href="#" id="last">{updog}</a>'


def main(paths, i, **kwargs):
    """ Iterator[str]: Main element. """
    page = paths[i]

    yield '<main>'
    yield from map(str.rstrip, readlines(page))
    yield '</main>'


def nav(paths, i, homename="home", **kwargs):
    """ Iterator[str]: <nav> element lines. """
    home, page, targets = paths[0], paths[i], paths[1:]

    atag = '<a href="{}">{}</a>'.format
    heretag = '<a href="#" id="here">{}</a>'.format
    hometag = '<a href="{}" id="home">{}</a>'.format
    openbox = "<details open><summary>{}</summary>".format
    shutbox = "<details><summary>{}</summary>".format

    yield "<nav>"
    yield hometag(urlpath(page,home), homename)

    newdirs = frozenset(home.parents)
    pagedirs = frozenset(page.parents)
    for t in targets:
        context = newdirs
        newdirs = frozenset(t.parents)

        # End old <details> boxes and start new ones
        yield from ('</details>' for _ in (context - newdirs))
        for d in sorted(newdirs - context):
            yield openbox(d.stem) if (d in pagedirs) else shutbox(d.stem)

        # Current page gets a special "you are here" link
        name = t.stem.replace('_',' ')
        yield heretag(name) if (t == page) else atag(urlpath(page,t),name)

    yield from ('</details>' for _ in (newdirs - frozenset(home.parents)))
    yield "</nav>"
