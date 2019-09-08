"""
Line generators.
"""
from datetime import datetime
from urllib.parse import urljoin

from .readers import urlpath

CSSPATH = 'style.css'

def iconbox(pages,i,iconbox=(),**kwargs):

    atag = '<a href="{}">{}</a>'.format
    npages = len(pages)
    prevpage = pages[(i-1) % npages]
    nextpage = pages[(i-1) % npages]
    home,here = pages[0], pages[i]

    yield '<section id="iconbox">'
    yield atag(urlpath(here,prevpage),'←prev')

    for alt,src,href in iconbox:
        src = urlpath(here,home.parent/src)
        alt = f'<img alt="{alt}" src="{src}" height=16 width=32>'
        yield atag(href,alt)

    yield atag(urlpath(here,nextpage),'next→')
    yield '</section>'

def jump(pages,i,jumptext='',**kwargs):
    yield f'<a href="#" id="jump">{jumptext or 'top of page'}</a>'

def klf(pages,i,copyright='',license='',license_url='',email='',**kwargs):

    liclink = '<a href="{}" rel="license">{}</a>'.format
    spantag = '<span id="{}">{}</span>'.format

    yield '<section id="klf">'
    if copyright:
        yield spantag('copyright',f'© {copyright} {datetime.now().year}')
    if license_url:
        license = liclink(license_url, license or 'LICENSE')
    if license:
        yield spantag('license',license)
    if email:
        yield f'<address>{email}</address>'
    yield '</section>'

def links(pages,i,baseurl='',favicon='',**kwargs):

    home,page = pages[0], pages[i]
    homedir = home.parent
    link = '<link rel="{}" href="{}">'.format

    yield link('stylesheet',urlpath(page,homedir/CSSPATH))
    if baseurl:
        yield link('home',baseurl)
        yield link('canonical',urljoin(baseurl,urlpath(home,page)))
    if favicon:
        yield link('icon',urlpath(page,homedir/favicon))

def meta(pages,i,author='',description='',generator='',keywords='',**kwargs):

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

def nav(pages,i,homename='home',**kwargs):

    endbox = '</details>'
    openbox = '<details open><summary>{}</summary>'.format
    closedbox = '<details><summary>{}</summary>'.format
    home,page,targets = paths[0], paths[i], paths[1:]

    yield '<nav>'
    yield f'<a href="{urlpath(i,home)}" id="home">{homename}</a>'

    newdirs = frozenset(home.parents)
    pagedirs = frozenset(page.parents)
    for t in targets:
        context = newdirs
        newdirs = dirset(t.parents)

        # End old <details> boxes and start new ones
        yield from ( endbox for _ in (context - newdirs) )
        for d in sorted(newdirs - context):
            yield openbox(d.stem) if (d in pagedirs) else closedbox(d.stem)

        href = '#' if (t == page) else urlpath(page,t)
        yield f'<a href="{href}">{t.stem}</a>'

    yield from ( endbox for _ in (newdirs - frozenset(home.parents)) )

    yield '</nav>'
