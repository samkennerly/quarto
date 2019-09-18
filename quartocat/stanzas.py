"""
Each function in this module generates a group of lines.
Quartocat joins these lines with newline characters to build a page.

Inputs
    paths   Tuple[Path]: Absolute paths to raw pages, home first.
    i       int: Which page are we generating?
    kwargs  All other inputs must be optional keyword arguments.
"""
from datetime import datetime
from itertools import chain
from posixpath import join as urljoin

from .readers import readlines, urlpath

CSSPATH = "style.css"
YEAR = datetime.now().year


def generate(paths, i, **kwargs):
    """ Iterator[str]: All lines of a single page. """
    chainit = chain.from_iterable
    body = (nav, main, icons, jump, klf, last)

    yield "<!DOCTYPE html>"
    yield "<html>"
    yield from head(paths, i, **kwargs)
    yield "<body>"
    yield from chainit(x(paths, i, **kwargs) for x in body)
    yield "</body>"
    yield "</html>"


def head(
    paths,
    i,
    author="",
    base_url="",
    description="",
    favicon="",
    generator="",
    keywords="",
    title="",
    **kwargs
):
    """ Iterator[str]: Page <head>. Not displayed, but used by browsers. """
    home, page = paths[0], paths[i]

    yield "<head>"
    yield "<title>"
    yield title or page.stem.replace("_", " ")
    yield "</title>"

    link = '<link rel="{}" href="{}">'.format
    yield link("stylesheet", urlpath(page, home.parent / CSSPATH))
    if base_url:
        yield link("home", base_url)
        yield link("canonical", urljoin(base_url, urlpath(home, page)))
    if favicon:
        yield link("icon", urlpath(page, home.parent / favicon))

    meta = '<meta name="{}" content="{}">'.format
    yield '<meta charset="utf-8">'
    yield meta("viewport", "width=device-width, initial-scale=1.0")
    if author:
        yield meta("author", author)
    if description:
        yield meta("description", description)
    if generator:
        yield meta("generator", generator)
    if keywords:
        yield meta("keywords", keywords)

    yield "</head>"


def icons(paths, i, icon_links=(), **kwargs):
    """ Iterator[str]: #icons section with link buttons. """
    home, page = paths[0], paths[i]

    atag = '<a href="{}" rel="{}">{}</a>'.format
    image = '<img alt="{}" src="{}" height=32 width=32 title="{}">'.format

    yield '<section id="icons">'
    yield atag(urlpath(page, paths[(i - 1) % len(paths)]), "prev", "<<")

    for alt, src, href in icon_links:
        src = urlpath(page, home.parent / src)
        yield atag(href, "external", image(alt, src, alt))

    yield atag(urlpath(page, paths[(i + 1) % len(paths)]), "next", ">>")
    yield "</section>"


def jump(paths, i, updog="top of page", **kwargs):
    """ Iterator[str]: #jump section. Traditionally used for intrusive ads. """
    yield '<section id="jump">'
    yield '<a href="#">{}</a>'.format(updog)
    yield "</section>"


def klf(paths, i, copyright="", email="", license="", license_url="", **kwargs):
    """ Iterator[str]: #klf section with copyright, license, and email. """
    yield '<section id="klf">'
    if copyright:
        copyright = "© {} {}.".format(copyright, YEAR)
        yield from ('<span id="copyright">', copyright, "</span>")
    if license_url:
        liclink = '<a href="{}" rel="license">{}</a>'.format
        license = liclink(license_url, license or "LICENSE")
    if license:
        yield from ('<span id="license">', license, "</span>")
    if email:
        yield from ("<address>", email, "</address>")
    yield "</section>"


def last(paths, i, generator="", js_sources=(), **kwargs):
    """ Iterator[str]: #last section. External JavaScripts go here. """
    yield '<section id="last">'
    yield from map('<script src="{}" async></script>'.format, js_sources)
    if generator:
        yield 'built by a <a href="{}">quartocat</a>'.format(generator)
    yield "</section>"


def main(paths, i, **kwargs):
    """ Iterator[str]: <main> element from raw HTML file. """
    yield from ("<main>", *map(str.rstrip, readlines(paths[i])), "</main>")


def nav(paths, i, home_name="home", **kwargs):
    """ Iterator[str]: <nav> element with links to all pages in site. """
    home, page, targets = paths[0], paths[i], paths[1:]

    atag = '<a href="{}">{}</a>'.format
    heretag = '<a href="#" id="here">{}</a>'.format
    hometag = '<a href="{}" id="home">{}</a>'.format
    openbox = "<details open><summary>{}</summary>".format
    shutbox = "<details><summary>{}</summary>".format

    yield "<nav>"
    yield hometag(urlpath(page, home), home_name)

    newdirs = frozenset(home.parents)
    pagedirs = frozenset(page.parents)
    for t in targets:
        context = newdirs
        newdirs = frozenset(t.parents)

        # End old <details> boxes and start new ones
        yield from ("</details>" for _ in (context - newdirs))
        for d in sorted(newdirs - context):
            yield openbox(d.stem) if (d in pagedirs) else shutbox(d.stem)

        # Current page gets a special "you are here" link
        name = t.stem.replace("_", " ")
        yield heretag(name) if (t == page) else atag(urlpath(page, t), name)

    yield from ("</details>" for _ in (newdirs - frozenset(home.parents)))
    yield "</nav>"
