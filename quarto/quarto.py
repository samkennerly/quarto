from pathlib import Path
from sys import stderr as STDERR

from .readers import querypage, readlines, stylesheet, tidybody
from .stanzas import CSSPATH, icons, jump, klf, links, meta, nav

class Quarto:

    def __init__(self,folder='.'):
        folder = Path(folder).resolve()
        pages = folder.glob('ready/**/*.html')
        home = folder/'ready/index.html'

        self.defaults = querypage(home)
        self.folder = folder
        self.pages = (home,*sorted(set(paths) - {home}))

    def __call__(self,i): return self.generate(i,**self.options(i))
    def __getitem__(self,i): return '\n'.join(self(i))
    def __iter__(self): return map(self,range(len(self)))
    def __len__(self): return len(self.pages)
    def __repr__(self): return f"Quarto({self.folder})"

    def apply(self,style='doctoral',target='target'):
        """ None: Clean target folder. Build pages and stylesheet. """

        self.vacuum('.html')
        self.build(target)

        self.vacuum('.css')
        self.catstyle(style,target)

        print(*self.errors,file=STDERR,sep='\n')
        print("What's done is done.")

    def build(self,target='target'):
        """ None: Generate and save all pages to target folder. """
        folder,pages,texts = self.folder, self.pages, iter(self)

        base = pages[0].parent
        target = folder/target

        print('Build',len(pages),'pages')
        for page,text in zip(pages,texts):
            write(target / page.relative_to(base), text)

    def catstyle(self,style,target='target'):
        """ None: Concatenate stylesheets and save to target folder. """
        folder,write = self.folder, self.write

        csspath = folder/target/CSSPATH
        styledir = folder/'styles'/style

        print('Cat CSS files in',styledir)
        write(csspath,stylesheet(styledir))

    def errors(self,target='target'):
        """ Tuple[str]: Check output for HTML errors. """
        raise NotImplementedError

    def generate(self,i,title='',**kwargs):
        """ Iterator[str]: Generate lines in page. """
        pages = self.pages

        page = pages[i]

        yield '<!doctype html>'
        yield '<html>'

        yield '<head>'
        yield f'<title>{title or page.stem}</title>'
        yield from links(pages,i,**kwargs)
        yield from meta(pages,i,**kwargs)
        yield '</head>'

        yield '<body>'
        yield from nav(pages,i,**kwargs)
        yield '<main>'
        yield from map(str.rstrip,readlines(page))
        yield '</main>'
        yield from iconbox(pages,i,**kwargs)
        yield from jump(pages,i,**kwargs)
        yield from klf(pages,i,**kwargs)
        yield '</body>'

        yield '</html>'

    def options(self,i):
        """ dict: Page options with home options as defaults. """
        defaults,page = self.defaults, self.pages[i]

        return { **defaults, **(querypage(page) or dict()) }

    def vacuum(self,suffix='.html',target='target'):
        """ None: Delete target files with selected suffix. """
        folder = self.folder

        target = folder/target
        pattern = f'**/*.{suffix.lstrip(".")}'
        if folder not in target.parents:
            raise ValueError(f'{target} not in {folder}')

        print('Vacuum',pattern,'files from',target)
        for path in target.glob(pattern):
            print('Delete',path)
            path.unlink()

    def write(self,path,text):
        """ None: Save text to file. """
        folder = self.folder

        path = folder/path
        if folder not in path.parents:
            raise ValueError(f'{path} not in {folder}')

        print('Save',path)
        path.parent.mkdir(exist_ok=True,parents=True)
        with open(path,'w') as file:
            print(text,file=file)
