from collections.abc import Mapping
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from posixpath import join as urljoin
from subprocess import run
from urllib.parse import quote


class Pages(Mapping):
    """
    Pages(folder=".")

    Generate web pages from HTML fragments.

    Pages is a callable, ordered, immutable Mapping.
    Keys are absolute Path objects to text files with .html suffix.
    Values are HTML strings generated lazily and never cached.

    Initialize Pages with a folder containing .html files.
    Pages searches recursively for .html files in that folder.
    Each file is used as the <main> element of one HTML page.

    Pages accepts absolute or relative paths as str or pathlib.Path objects.
    An index.html file must exist. All other files are optional.

    Page options (title, description, etc.) may be stored in JSON files.
    Options must have the same path as their page, but with a .json suffix.
    If index.json exists, its values are defaults for all missing page options.

    Call help(Pages) for more information.
    """

    CSSPATH = "style.css"

    def __init__(self, folder="."):
        self.home = self.validpath(folder) / "index.html"
        self._options = None
        self._paths = None

    folder = property(lambda self: self.home.parent)

    # Magic methods

    def __call__(self, page):
        """ Iterator[str]: Lines of finished page. """
        return self.generate(page, **self.querypage(page, **self.options))

    def __getitem__(self, page):
        """ str: Finished page as one big string. """
        return "\n".join(self(page))

    def __iter__(self):
        """ Iterable[Path]: Absolute Path to each main element. """
        return iter(self.paths)

    def __len__(self):
        """ int: Number of main elements found. """
        return len(self.paths)

    def __repr__(self):
        """ str: Printable representation of self. """
        return "{}({})".format(type(self).__name__, self.home.parent)

    # Commands

    @classmethod
    def apply(cls, style, target):
        """ None: Cat stylesheets from style folder to target folder. """
        stylecat = cls.stylecat
        csspath = cls.validpath(target) / cls.CSSPATH

        print("Save", csspath)
        with open(csspath, "w") as file:
            file.write(stylecat(style))

    def build(self, target):
        """ None: Generate each page and write to target folder. """
        folder = self.folder
        target = self.validpath(target)
        items = self.items

        for path, text in items():
            path = target / path.relative_to(folder)
            print("Save", path)
            path.parent.mkdir(exist_ok=True, parents=True)
            with open(path, "w") as file:
                file.write(text)

    def clean(self, ready):
        """ None: Save cleaned page bodies to ready folder. """
        tidycopy = self.tidycopy
        folder = self.folder
        ready = self.validpath(ready)
        paths = self.paths

        for dirty in paths:
            clean = ready / dirty.relative_to(folder)
            print("Save", clean)
            clean.parent.mkdir(exist_ok=True, parents=True)
            tidycopy(dirty, clean)

    @classmethod
    def delete(cls, suffix, target):
        """ None: Remove files with selected suffix and any empty folders. """
        target = cls.validpath(target)

        pattern = "*." + suffix.lstrip(".")
        for path in target.rglob(pattern):
            print("Delete", path)
            path.unlink()

    # HTML generators

    def generate(self, page, title="", **kwargs):
        """ Iterator[str]: All lines in page. """
        page = self.home.parent / page

        yield "<!DOCTYPE html>"
        yield "<html>"

        yield "<head>"
        yield "<title>"
        yield title or page.stem.replace("_", " ")
        yield "</title>"
        yield from self.links(page, **kwargs)
        yield from self.meta(page, **kwargs)
        yield "</head>"

        yield "<body>"
        yield "<main>"
        yield from map(str.rstrip, self.readlines(page))
        yield "</main>"
        yield from self.nav(page, **kwargs)
        yield from self.icons(page, **kwargs)
        yield from self.jump(page, **kwargs)
        yield from self.klf(page, **kwargs)
        yield "</body>"

        yield "</html>"

    def icons(self, page, icon_links=(), next_name="", prev_name="", **kwargs):
        """
        Iterator[str]: Links drawn with JPEGs, PNGs, ICOs or even GIFs.
        Consider SVGs so there's no scaling glitch. (I love it.)
        """
        home, paths, urlpath = self.home, self.paths, self.urlpath

        base = home.parent
        page = base / page
        i, n = paths.index(page), len(paths)
        atag = '<a href="{}" rel="{}">{}</a>'.format
        imgtag = '<img alt="{}" src="{}" height=32 width=32 title="{}">'.format

        yield '<section id="icons">'

        if prev_name:
            yield atag(urlpath(page, paths[(i - 1) % n]), "prev", prev_name)

        for alt, src, href in icon_links:
            src = urlpath(page, base / src)
            yield atag(href, "external", imgtag(alt, src, alt))

        if next_name:
            yield atag(urlpath(page, paths[(i + 1) % n]), "next", next_name)

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
            href = "#" if (t == page) else urlpath(page, t)
            yield atag(href, t.stem.replace("_", " "))

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
        readlines, validpath = cls.readlines, cls.validpath

        return "".join(readlines(*sorted(validpath(style).rglob("*.css"))))

    @classmethod
    def tidycopy(cls, dirty, clean):
        """ None: Clean raw HTML page and save. Requires HTML Tidy >= 5. """
        dirty, clean = Path(dirty), Path(clean)

        # tidy returns status 0 even if input does not exist
        if not dirty.exists():
            raise FileNotFoundError(dirty)

        cmds = "tidy -ashtml -bare -clean -quiet --show-body-only yes".split()
        cmds = (*cmds, "-output", str(clean), str(dirty))
        status = run(cmds).returncode
        if status and (status != 1):
            raise ChildProcessError("Tidy returned {}".format(status))

    @classmethod
    def urlpath(cls, page, path):
        """ str: URL-encoded relative path from page to local file. """
        return quote(relpath(path, start=Path(page).parent))

    @classmethod
    def validpath(cls, path):
        """ Path: Absolute path. Raise error if path does not exist. """
        path = Path(path).resolve()
        if not path.exists():
            raise FileNotFoundError("No such file or folder: {}".format(path))

        return path
