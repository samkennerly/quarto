"""
Quarto builds each page in groups of lines called "stanzas."
Each function in this module generates one stanza.

INPUTS
    paths   Tuple[Path]: Absolute paths to raw pages, home first.
    i       int: Which page are we generating?
    kwargs  All other inputs must be optional keyword arguments.

OUTPUTS
    Iterable[str]: Lines of HTML. (Newline characters will be added later.)
"""
from datetime import datetime
from urllib.parse import urljoin

from .reader import urlpath

CSSPATH = 'style.css'

def icons(paths,i,iconlinks=(),**kwargs):
    """ Iterator[str]: <section id="icons"> lines. """

    atag = '<a href="{}">{}</a>'.format
    npaths = len(paths)
    prevpath = paths[(i-1) % npaths]
    nextpath = paths[(i-1) % npaths]
    home,here = paths[0], paths[i]

    yield '<section id="icons">'
    yield atag(urlpath(here,prevpath),'←prev')

    for alt,src,href in iconlinks:
        src = urlpath(here,home.parent/src)
        alt = f'<img alt="{alt}" src="{src}" height=16 width=32>'
        yield atag(href,alt)

    yield atag(urlpath(here,nextpath),'next→')
    yield '</section>'

def jump(paths,i,jumptext='top of page',**kwargs):
    """ Iterator[str]: <section id="jump"> lines. """

    yield '<section id="jump">'
    yield f'<a href="#">{jumptext}</a>'
    yield '</section>'

def klf(paths,i,copyright='',license='',license_url='',email='',**kwargs):
    """ Iterator[str]: <section id="klf"> lines. """

    spantag = '<span id="{}">\n{}\n</span>'.format

    yield '<section id="klf">'
    if copyright:
        yield spantag('copyright',f'© {copyright} {datetime.now().year}')
    if license_url:
        license = license or 'LICENSE'
        license = f'<a href="{license_url}" rel="license">{license}</a>'
    if license:
        yield spantag('license',license)
    if email:
        yield f'<address>{email}</address>'
    yield '</section>'

def links(paths,i,baseurl='',favicon='',**kwargs):
    """ Iterator[str]: <link> tags for page <head>. """

    home,here = paths[0], paths[i]
    homedir = home.parent
    link = '<link rel="{}" href="{}">'.format

    yield link('stylesheet',urlpath(here,homedir/CSSPATH))
    if baseurl:
        yield link('home',baseurl)
        yield link('canonical',urljoin(baseurl,urlpath(home,here)))
    if favicon:
        yield link('icon',urlpath(here,homedir/favicon))

def meta(paths,i,author='',description='',generator='',keywords='',**kwargs):
    """ Iterator[str]: <meta> tags for page <head>. """

    meta = '<meta name="{}" content="{}">'.format

    yield '<meta charset="utf-8">'
    yield meta('viewport','width=device-width, initial-scale=1.0')
    if author:
        yield meta('author',author)
    if description:
        yield meta('description',description)
    if generator:
        yield meta('generator',generator)
    if keywords:
        yield meta('keywords',keywords)

def nav(paths,i,homename='home',**kwargs):
    """ Iterator[str]: <nav> element lines. """
    home,here,targets = paths[0], paths[i], paths[1:]

    yield '<nav>'
    yield f'<a href="{urlpath(here,home)}" id="home">{homename}</a>'

    endbox = '</details>'
    openbox = '<details open><summary>{}</summary>'.format
    shutbox = '<details><summary>{}</summary>'.format
    newdirs = frozenset(home.parents)
    heredirs = frozenset(here.parents)

    for t in targets:
        context = newdirs
        newdirs = frozenset(t.parents)

        # End old <details> boxes and start new ones
        yield from ( endbox for _ in (context - newdirs) )
        for d in sorted(newdirs - context):
            yield openbox(d.stem) if (d in heredirs) else shutbox(d.stem)

        # Current page gets a special "you are here" link
        if t == here:
            yield f'<a href="#" id="here">{here.stem}</a>'
        else:
            yield f'<a href="{urlpath(here,t)}">{t.stem}</a>'

    yield from ( endbox for _ in (newdirs - frozenset(home.parents)) )
    yield '</nav>'
