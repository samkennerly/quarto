from collections.abc import Mapping
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from posixpath import join as urljoin
from urllib.parse import quote


class Quarto(Mapping):

    CSSPATH = "style.css"

    def __init__(self, folder="."):
        self.home = Path(folder).resolve() / "index.html"
        self._options = None
        self._paths = None

    folder = property(lambda self: self.home.parent)

    # Magic methods

    def __call__(self, page):
        return self.generate(page, **self.querypage(page, **self.options))

    def __getitem__(self, page):
        return "\n".join(self(page))

    def __iter__(self):
        return iter(self.paths)

    def __len__(self):
        return len(self.paths)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.home.parent)

    # Commands

    @classmethod
    def apply(cls, style, target):
        """ Cat stylesheets from style folder to target folder. """
        CSSPATH, stylecat = cls.CSSPATH, cls.stylecat

        target = Path(target)
        outpath = target / CSSPATH
        print("Apply", style, "to", outpath)

        if not target.is_dir():
            raise NotADirectoryError(target)

        with open(outpath, "w") as file:
            file.write(stylecat(style))

        print("The style of", target, "is", style)

    def build(self, target):
        """ Generate each page and write to target folder. """
        home, items = self.home, self.items

        source = home.parent
        target = Path(target)
        print("Build", len(self), "pages from", source, "to", target)

        if not target.is_dir():
            raise NotADirectoryError(target)

        for path, text in self.items():
            path = target / path.relative_to(source)
            print("Save", path)
            path.parent.mkdir(exist_ok=True, parents=True)
            with open(path, "w") as file:
                file.write(text)

        print("What's done is done. Exeunt", type(self).__name__)

    def convert(self, source):
        """ None: Import pages from preprints folder. """
        raise NotImplementedError

    @classmethod
    def delete(cls, suffix, target):
        """ None: Remove files with suffix from target folder. """
        search = Path(target).rglob
        pattern = "*." + suffix.lstrip(".")
        for path in search(pattern):
            print("Delete", path)
            path.unlink()

    @classmethod
    def errors(cls, target):
        """ List[str]: Errors detected in pages in target folder. """
        raise NotImplementedError

    # HTML generators

    def generate(self, page, title="", **kwargs):
        """ Iterator[str]: All lines in page. """
        page = self.home.parent / page

        yield '<!DOCTYPE html>'
        yield '<html>'

        yield '<head>'
        yield '<title>'
        yield title or page.stem.replace('_', " ")
        yield '</title>'
        yield from self.links(page, **kwargs)
        yield from self.meta(page, **kwargs)
        yield '</head>'

        yield '<body>'
        yield '<main>'
        yield from map(str.rstrip,self.readlines(page))
        yield '</main>'
        yield from self.nav(page, **kwargs)
        yield from self.icons(page, **kwargs)
        yield from self.jump(page, **kwargs)
        yield from self.klf(page, **kwargs)
        yield '</body>'

        yield '</html>'

    def icons(self, page, icon_links=(), **kwargs):
        """
        Iterator[str]: Links drawn with JPEGs, PNGs, ICOs or even GIFs.
        Consider SVGs so there's no scaling glitch. (I love it.)
        """
        home, paths, urlpath = self.home, self.paths, self.urlpath

        page = home.parent / page
        index = paths.index(page)
        nextpage = paths[(index + 1) % len(paths)]
        prevpage = paths[(index - 1) % len(paths)]

        atag = '<a href="{}" rel="{}">{}</a>'.format
        image = '<img alt="{}" src="{}" height=32 width=32 title="{}">'.format

        yield '<section id="icons">'
        yield atag(urlpath(page, prevpage), "prev", "◄")

        for alt, src, href in icon_links:
            src = urlpath(page, home.parent / src)
            yield atag(href, "", image(alt, src, alt))

        yield atag(urlpath(page, nextpage), "next", "►")
        yield "</section>"

    def jump(self, page, js_sources=(), updog="", **kwargs):
        """
        Iterator[str]: And I know, reader, just how you feel.
        You got to scroll past the pop-ups to get to what's real.
        """
        jstag = '<script src="{]" async></script>'.format
        uptag = '<a href="#" id="updog">{}</a>'.format

        yield '<section id="jump">'
        yield from map(jstag, js_sources)
        if updog:
            yield uptag(updog)
        yield "</section>"

    def klf(self, page, copyright="", email="", generator="", license=(), **kwargs):
        """
        Iterator[str]: Copyright, license, and final elements.
        They're justified, and they're ancient. I hope you understand.
        """
        addrtag = "<address>{}</address>".format
        spantag = '<span id="{}">\n{}\n</span>'.format
        genlink = 'built by a <a href="{}" rel="generator">quarto</a>'.format
        liclink = '<a href="{}" rel="license">{}</a>'.format

        yield '<section id="klf">'
        if copyright:
            yield spantag("copyright", copyright)
        if license:
            yield spantag("license", liclink(*license))
        if email:
            yield addrtag(email)
        if generator:
            yield spantag("quarto", genlink(generator))
        yield "</section>"

    def links(self, page, base_url="", favicon="", **kwargs):
        """ Iterator[str]: <link> tags in page <head>. """
        CSSPATH, home, urlpath = self.CSSPATH, self.home, self.urlpath

        page = home.parent / page
        linktag = '<link rel="{}" href="{}">'.format

        yield linktag("stylesheet", urlpath(page, home.parent / CSSPATH))
        if base_url:
            yield linktag("home", base_url)
            yield linktag("canonical", urljoin(base_url, urlpath(home, page)))
        if favicon:
            yield linktag("icon", urlpath(page, home.parent / favicon))

    def meta(self, page, author="", description="", keywords=(), **kwargs):
        """ Iterator[str]: <meta> tags in page <head>. """
        metatag = '<meta name="{}" content="{}">'.format

        yield '<meta charset="utf-8">'
        if author:
            yield metatag("author", author)
        if description:
            yield metatag("description", description)
        if keywords:
            yield metatag("keywords", ",".join(keywords))
        yield metatag("viewport", "width=device-width, initial-scale=1.0")

    def nav(self, page, home_name="home", **kwargs):
        """ Iterator[str]: <nav> element with links to other pages. """
        home, paths, urlpath = self.home, self.paths, self.urlpath

        page = home.parent / page
        targets = paths[1:]

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

        yield from ("</details>" for _ in (newdirs - set(home.parents)))
        yield "</nav>"

    # Cached properties

    @property
    def options(self):
        """ dict: Home page options from index.json file. """
        home, options, querypage = self.home, self._options, self.querypage

        if options is None:
            options = querypage(home)
            self._options = options

        return options

    @property
    def paths(self):
        """ Tuple[Path]: Absolute path to each page in home folder. """
        home, paths = self.home, self._paths

        if paths is None:
            paths = home.parent.rglob("*.html")
            paths = (home, *sorted(x for x in paths if x != home))
            self._paths = paths

        return paths

    # File methods

    @classmethod
    def querypage(cls, page, **kwargs):
        """ dict: Page options, if any. Kwargs are default values. """
        path = Path(page).with_suffix(".json")

        if path.is_file():
            with open(path) as file:
                kwargs.update(jsonload(file))

        return kwargs

    @classmethod
    def readlines(cls, *paths):
        """ Iterator[str]: Raw lines from text file(s). """
        for path in paths:
            with open(path) as lines:
                yield from lines

    @classmethod
    def stylecat(cls, style):
        """ str: Concatenated CSS files from style folder. """
        return "".join(cls.readlines(*sorted(Path(style).rglob("*.css"))))

    def tidycopy(self, page, target):
        """ None: Save clean page to target folder. Requires HTML Tidy > 5. """
        folder = self.folder

        page = folder / page
        outpath = Path(target) / page.relative_to(folder)
        command = 'tidy -ashtml -bare -clean -gdoc -quiet --show-body-only yes'
        command = (*command.split(), '-output', str(outpath), str(page))

        # tidy returns status 0 even if input does not exist
        if not page.exists():
            raise FileNotFoundError(page)

        print('Save', outpath)
        outpath.parent.mkdir(exist_ok=True,parents=True)
        ran = run(command,capture_output=True)

        # print tidy warnings; raise tidy errors
        status, errs = ran.returncode, ran.stderr.decode()
        if status == 1:
            print(errs,file=stderr)
        elif status:
            raise ChildProcessError('Tidy: ' + errs)

    @classmethod
    def urlpath(cls, page, path):
        """ str: URL-encoded relative path from page to local file. """
        return quote(relpath(path, start=Path(page).parent))
