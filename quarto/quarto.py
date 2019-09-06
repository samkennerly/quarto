from collections.abc import Sequence
from datetime import datetime
from json import load as jload
from os.path import relpath
from pathlib import Path
from urllib.parse import quote, urljoin

CSSPATH = 'style.css'

def readjson(path):
    """ dict or list: Read JSON file. """
    with open(path,'r') as file:
        return jload(file)

def readlines(*paths):
    """ Iterator[str]: Read lines from text file(s). """
    for path in paths:
        print('Read',path)
        with open(path,'r') as file:
            yield from file

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

        self.defaults = readjson(home.with_suffix('.json'))
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

    # Readers

    def style(self,name='doctoral'):
        """ str: Concatenated stylesheets. """
        folder = self.folder

        style = folder/'styles'/name
        paths = sorted(style.glob('*.css'))
        if not paths:
            raise FileNotFoundError('No *.css files in',style)

        return ''.join(readlines(*paths))

    def tidy(self,cmd):
        raise NotImplementedError

    def urlpath(self,i,path):
        """ str: URL-encoded relative path from page to local file. """
        htmls = self.htmls

        here,home = htmls[i], htmls[0]
        heredir,homedir = here.parent, home.parent

        return quote(relpath(homedir/path,start=heredir))

    def variables(self,i):
        """ dict: Page variables. Fill missing values with defaults. """
        defaults,htmls = self.defaults, self.htmls

        path = htmls[i].with_suffix('.json')
        pagevars = readjson(path) if path.is_file() else dict()

        return {**defaults,**pagevars}

    # Generators

    def body(self,i,**kwargs):
        linkbox,main,nav,outro = self.linkbox,self.main,self.nav,self.outro

        updog = kwargs.get('updog') or 'top of page'
        yield '<body>'
        yield from linkbox(i,**kwargs)
        yield from main(i,**kwargs)
        yield from nav(i,**kwargs)
        yield from outro(i,**kwargs)
        yield f'<a href="#" id="updog">{updog}</a>'
        yield '</body>'

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

        iconlinks = kwargs.get('iconlinks',[ ])
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
        htmls = self.htmls

        yield '<main>'
        yield from map(str.rstrip,readlines(htmls[i]))
        yield '</main>'

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
        body,head,variables = self.body, self.head, self.variables

        pagevars = variables(i)
        yield '<!DOCTYPE html>'
        yield '<html>'
        yield from head(i,**pagevars)
        yield from body(i,**pagevars)
        yield '</html>'
