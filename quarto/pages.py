"""
Pages class.
"""
from pathlib import Path

from .reader import querypage, readlines, stylesheet, tidybody, urlpath
from .stanza import CSSPATH, icons, jump, klf, links, meta, nav

class Pages:
    """
    Find, read, and finish raw HTML files.
    """

    def __init__(self,folder='.'):
        folder = Path(folder).resolve()
        paths = folder.glob('ready/**/*.html')
        home = folder/'ready/index.html'

        self.defaults = querypage(home)
        self.folder = folder
        self.paths = (home,*sorted(set(paths) - {home}))

    home = property(lambda self: self.paths[0])

    def __call__(self,i): return self.generate(i,**self.options(i))
    def __getitem__(self,i): return '\n'.join(self(i))
    def __iter__(self): return ( self[i] for i in range(len(self)) )
    def __len__(self): return len(self.paths)
    def __repr__(self): return f"Quarto({self.folder})"

    def build(self,target='target'):
        """ None: Generate and save all pages to target folder. """
        folder,home,paths = self.folder, self.home, self.paths
        texts,vacuum,write = iter(self), self.vacuum, self.write

        homedir = home.parent
        target = folder/target
        print('Build',len(paths),'pages in',target)

        vacuum('.html',target)
        for path,text in zip(paths,texts):
            write(target / path.relative_to(homedir), text)

        print("What's done is done. Exeunt, quarto.")

    def catstyle(self,style,target='target'):
        """ None: Concatenate stylesheets and save to target folder. """
        folder,vacuum,write = self.folder, self.vacuum, self.write

        target = folder/target
        source = folder/'styles'/style
        csspath = target/CSSPATH
        print(f"Cat styles/{style}/*.css >",csspath.relative_to(folder))

        vacuum('.css',target)
        write(csspath,stylesheet(source))

        print(f"The style of this website is {style}.")

    def errors(self,target='target'):
        """ Tuple[str]: Check output for HTML errors. """
        raise NotImplementedError

    def generate(self,i,title='',**kwargs):
        """ Iterator[str]: Generate lines in page. """
        paths = self.paths

        path = paths[i]
        main = map(str.rstrip,readlines(path))
        title = str(title or page.stem)

        yield '<!doctype html>'
        yield '<html>'
        yield '<head>'
        yield from ('<title>',title,'</title>')
        yield from links(paths,i,**kwargs)
        yield from meta(paths,i,**kwargs)
        yield '</head>'
        yield '<body>'
        yield from nav(paths,i,**kwargs)
        yield from ('<main>',*main,'</main>')
        yield from icons(paths,i,**kwargs)
        yield from jump(paths,i,**kwargs)
        yield from klf(paths,i,**kwargs)
        yield '</body>'
        yield '</html>'

    def options(self,i):
        """ dict: Page options with home options as defaults. """
        defaults,paths = self.defaults, self.paths

        return { **defaults, **(querypage(paths[i]) or dict()) }

    def vacuum(self,suffix='.html',target='target'):
        """ None: Delete all files in target folder with selected suffix. """
        folder = self.folder

        target = folder/target
        pattern = f'**/*.{suffix.lstrip(".")}'
        if folder not in target.parents:
            raise ValueError(f'{target} not in {folder}')

        for path in target.glob(pattern):
            print('Delete',path)
            path.unlink()

    def write(self,path,text):
        """ None: Save text to file. """
        folder = self.folder

        path = folder/path
        if folder not in path.parents:
            raise ValueError(f'{path} not in {folder}')

        print('Write',path)
        path.parent.mkdir(exist_ok=True,parents=True)
        with open(path,'w') as file:
            print(text,file=file)
