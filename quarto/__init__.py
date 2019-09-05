#!/usr/bin/env python3

from collections.abc import Sequence
from datetime import datetime
from json import load as jload
from os.path import relpath
from pathlib import Path
from urllib.parse import quote, urljoin

CSSPATH = 'style.css'

def readlines(*paths):
    """ Iterator[str]: Lines of text file(s) without trailing whitespace. """
    for path in paths:
        with open(path) as lines:
            yield from map(str.rstrip,lines)

def savetext(path,text):
    """ None: Save a string to a text file. """
    print('Save',path)
    with open(path,'w') as file:
        file.write(text)

class Quarto(Sequence):

    def __init__(self,folder=''):
        folder = Path(folder).resolve()
        htmls = folder.glob('ready/**/*.html')
        home = folder/'ready/index.html'

        self.folder = folder
        self.htmls = (home,*sorted( x for x in htmls if x != home ))

    home = property(lambda self: self.htmls[0])

    def __getitem__(self,i): return '\n'.join(self.page(i))
    def __len__(self): return len(self.htmls)
    def __repr__(self): return f"Quarto({self.folder})"

    # Writers

    def write(self,outdir='output'):
        """ None: Build and save website. """
        folder,htmls,style = self.folder, self.htmls, self.style

        outdir = folder/outdir
        homedir = htmls[0].parent

        savetext(outdir/CSSPATH,style())
        for path,text in zip(htmls,self):
            path = outdir/path.relative_to(homedir)
            path.parent.mkdir(exist_ok=True,parents=True)
            savetext(path,text)

    # Helpers

    def jdata(self,i):
        """ dict: Page parameters if they exist. """
        here = self.htmls[i]

        path = here.with_suffix('.json')
        if path.is_file():
            with open(path) as file:
                return jload(file)

        return dict()

    def style(self):
        """ str: Concatenated stylesheets. """
        return '\n'.join(readlines(*sorted(self.folder.glob('style/*.css'))))

    def urlpath(self,i,path):
        """ str: URL-encoded relative path from page to local file. """
        htmls = self.htmls

        here,home = htmls[i], htmls[0]
        heredir,homedir = here.parent, home.parent

        return quote(relpath(homedir/path,start=heredir))

    # Generators

    def head(self,i,**kwargs):
        """ Iterator[str]: Lines in HTML <head> element. """
        htmls,urlpath = self.htmls, self.urlpath

        get = kwargs.get
        here = htmls[i]
        title = get('title',here.stem)
        baseurl = get('baseurl')
        favicon = get('favicon')
        metakeys = 'author description generator keywords'.split()
        metadata = zip(metakeys,map(get,metakeys))

        link = '<link rel="{}" href="{}">'.format
        meta = '<meta name="{}" content="{}">'.format

        yield '<head>'
        yield f'<title>{title}</title>'
        yield link('stylesheet',urlpath(i,CSSPATH))
        if baseurl:
            yield link('canonical',urljoin(baseurl,urlpath(0,here)))
            yield link('home',baseurl)
        if favicon:
            yield link('icon',urlpath(i,favicon))
        yield '<meta charset="utf-8">'
        yield from ( meta(k,v) for k,v in metadata if v )
        yield meta('viewport','width=device-width, initial-scale=1.0')
        yield '</head>'

    def linkbox(self,i,**kwargs):
        """ Iterator[str]: Link buttons. """
        htmls,urlpath = self.htmls, self.urlpath

        iconlinks = kwargs.get('iconlinks')
        prevpage = htmls[(i-1) % len(htmls)]
        nextpage = htmls[(i+1) % len(htmls)]

        atag = '<a href="{}">{}</a>'.format
        itag = '<img alt="{}" src="{}" height="16" width="32">'.format
        # Use CSS to change hard-coded default icon size

        yield '<section id="linkbox">'
        yield atag(urlpath(i,prevpage),'←prev')

        for alt,src,href in iconlinks:
            yield atag(href, itag(alt,urlpath(i,src)) if src else alt )

        yield atag(urlpath(i,nextpage),'next→')
        yield '</section>'

    def main(self,i,**kwargs):
        """ Iterator[str]: Main element. """
        yield from ('<main>',*readlines(self.htmls[i]),'</main>')

    def nav(self,i,**kwargs):
        """ Iterator[str]: Navigation within site. """
        htmls,urlpath = self.htmls, self.urlpath

        get = kwargs.get
        homename = get('homename')
        here,home,targets = htmls[i], htmls[0], htmls[1:]

        atag = '<a href="{}">{}</a>'.format
        boxtag = '<details><summary>{}</summary>'.format
        oboxtag = '<details open><summary>{}</summary>'.format

        yield '<nav>'
        yield f'<a href="{urlpath(i,home)}" id="home">{homename}</a>'

        newdirs = frozenset(home.parents)
        heredirs = frozenset(here.parents)
        for t in targets:
            boxdirs = newdirs
            newdirs = frozenset(t.parents)

            # Stop old <details> boxes and start new ones
            yield from ( '</details>' for _ in (boxdirs - newdirs) )
            for d in sorted(newdirs - boxdirs):
                yield oboxtag(d.stem) if (d in heredirs) else boxtag(d.stem)

            # Link to target OR mark "you are here"
            yield atag('#' if (t == here) else urlpath(i,t), t.stem)

        # Stop any leftover <details> boxes
        yield from ( '</details>' for _ in (newdirs - set(home.parents)) )

        yield '</nav>'

    def outro(self,i,**kwargs):
        """ Iterator[str]: Fine print. """

        get = kwargs.get
        now = datetime.now
        email = get('email')
        license = get('license')
        copyright = get('copyright')

        yield '<section id="outro">'
        if copyright:
            yield '<span id="copyright">'
            yield "© {} {}.".format(copyright,now().year)
            yield '</span>'
        if license:
            yield from ('<span id="license">','Licensed under a')
            yield '<a href="{url}" rel="license">{text}</a>'.format(**license)
            yield from ('license.','</span>')
        if email:
            yield from ('<address>',email,'</address>')
        yield '</section>'

    def page(self,i):
        """ Iterator[str]: All lines in page. """
        kwargs = {**self.jdata(0),**self.jdata(i)}

        yield '<!DOCTYPE html>'
        yield '</html>'
        yield from self.head(i,**kwargs)
        yield '<body>'
        yield from self.linkbox(i,**kwargs)
        yield from self.main(i,**kwargs)
        yield from self.nav(i,**kwargs)
        yield from self.outro(i,**kwargs)
        yield f'<a href="#" id="updog">{kwargs.get("updog") or "up"}</a>'
        yield '</body>'
        yield '</html>'
