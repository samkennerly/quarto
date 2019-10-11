from collections.abc import Mapping
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from posixpath import join as urljoin
from subprocess import run
from urllib.parse import quote, urlsplit

HOMEPAGE = "index.html"
PAGEPATHS = "pages.txt"
QUARTOHOME = "https://github.com/samkennerly/quarto"
STYLESHEET = "style.css"


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

    def __init__(self, folder="."):
        validpath = type(self).validpath

        self.home = validpath(folder) / HOMEPAGE
        self._options = None
        self._paths = None

    folder = property(lambda self: self.home.parent)

    # Magic methods

    def __call__(self, page):
        """ Iterator[str]: Lines of finished page. """
        return self.generate(page, **self.query(page, **self.options))

    def __fspath__(self):
        """ str: String representation of base folder. """
        return str(self.folder)

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
        return f"{type(self).__name__}({self.folder})"

    def __truediv__(self, pathlike):
        """ Path: Absolute path from base folder. """
        return self.folder / pathlike

    # Commands

    @classmethod
    def apply(cls, style, target):
        """ None: Cat stylesheets from style folder to target folder. """
        cls.write(cls.stylecat(style), cls.validpath(target) / STYLESHEET)

    def build(self, target):
        """ None: Generate each page and write to target folder. """
        items, validpath, write = self.items, self.validpath, self.write

        target = validpath(target)
        for path, text in items():
            path = target / path.relative_to(self).with_suffix(".html")
            path.parent.mkdir(exist_ok=True, parents=True)
            write(text, path)

    def clean(self, ready):
        """ None: Save cleaned page bodies to ready folder. """
        validpath, tidycopy = self.validpath, self.tidycopy

        ready = validpath(ready)
        for dirty in self:
            clean = ready / dirty.relative_to(self).with_suffix(".html")
            clean.parent.mkdir(exist_ok=True, parents=True)
            tidycopy(dirty, clean)

    @classmethod
    def delete(cls, suffix, target):
        """ None: Remove files with selected suffix and any empty folders. """
        validpath = cls.validpath

        target = validpath(target)
        pattern = "*." + suffix.lstrip(".")
        for path in target.rglob(pattern):
            print("Delete", path)
            path.unlink()

    # HTML generators

    def generate(self, page, title="", **kwargs):
        """ Iterator[str]: All lines in page. """
        page = self / page

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
        yield ""

    def icons(self, page, icons=(), nextlink="", prevlink="", **kwargs):
        """
        Iterator[str]: Links drawn with JPEGs, PNGs, ICOs or even GIFs.
        Consider SVGs so there's no scaling glitch. (I love it.)
        """
        home, paths, urlpath = self.home, self.paths, self.urlpath

        page = self / page
        i, n = paths.index(page), len(paths)

        yield '<section id="icons">'
        if prevlink:
            href = urlpath(page, (paths[(i - 1) % n]).with_suffix(".html"))
            yield f'<a href="{href}" rel="prev">{prevlink}</a>'
        for alt, src, href in icons:
            src = urlpath(page, self / src)
            alt = f'<img alt="{alt}" src="{src}" height="32" title="{alt}">'
            yield f'<a href="{href}">{alt}</a>'
        if nextlink:
            href = urlpath(page, (paths[(i + 1) % n]).with_suffix(".html"))
            yield f'<a href="{href}" rel="next">{nextlink}</a>'
        yield "</section>"

    def jump(self, page, javascripts=(), updog="", **kwargs):
        """
        Iterator[str]: And I know, reader, just how you feel.
        You got to scroll past the pop-ups to get to what's real.
        """
        yield '<section id="jump">'
        if updog:
            yield f'<a href="#" id="updog">{updog}</a>'
        for src in javascripts:
            yield f'<script src="{src}" async></script>'
        yield "</section>"

    def klf(self, page, copyright="", email="", qlink="", license=(), **kwargs):
        """
        Iterator[str]: Copyright, license, and final elements.
        They're justified, and they're ancient. I hope you understand.
        """
        yield '<section id="klf">'
        if copyright:
            yield f'<span id="copyright">{copyright}</span>'
        if license:
            yield '<a href="{}" rel="license">{}</a>'.format(*license)
        if email:
            yield f"<address>{email}</address>"
        if qlink:
            yield f'<a href="{QUARTOHOME}" rel="generator">{qlink}</a>'
        yield "</section>"

    def links(self, page, base="", favicon="", styles=(), **kwargs):
        """ Iterator[str]: <link> tags in page <head>. """
        home, urlpath = self.home, self.urlpath

        page = (self / page).with_suffix(".html")
        link = '<link rel="{}" href="{}">'.format

        if base:
            yield link("home", base)
            yield link("canonical", urljoin(base, urlpath(home, page)))
        if favicon:
            yield link("icon", urlpath(page, self / favicon))
        for sheet in styles:
            yield link("stylesheet", urlpath(page, self / sheet))

    def meta(self, page, meta=(), **kwargs):
        """ Iterator[str]: <meta> tags in page <head>. """
        mtag = '<meta name="{}" content="{}">'.format

        yield '<meta charset="utf-8">'
        yield mtag("viewport", "width=device-width, initial-scale=1.0")
        for k, v in dict(meta).items():
            yield mtag(k, v)

    def nav(self, page, homelink="home", **kwargs):
        """ Iterator[str]: <nav> element with links to other pages. """
        home, paths, urlpath = self.home, self.paths, self.urlpath

        page = (self / page).with_suffix(".html")
        opendirs = frozenset(page.parents)
        workdirs = frozenset(home.parents)
        openbox = "<details open><summary>{}</summary>".format
        shutbox = "<details><summary>{}</summary>".format

        yield "<nav>"
        for p in paths:

            p = p.with_suffix(".html")
            href = "#" if (p == page) else urlpath(page, p)
            context = workdirs
            workdirs = frozenset(p.parents)

            yield from ("</details>" for _ in (context - workdirs))
            for d in sorted(workdirs - context):
                yield openbox(d.stem) if d in opendirs else shutbox(d.stem)

            if p == home:
                yield f'<a href="{href}" id="home">{homelink}</a>'
            else:
                yield f'<a href="{href}">{p.stem.replace("_", " ")}</a>'

        yield from ("</details>" for _ in (workdirs - set(home.parents)))
        yield "</nav>"

    # Cached properties

    @property
    def options(self):
        """ dict: Home page options from index.json file. """
        home, options, query = self.home, self._options, self.query

        if options is None:
            options = query(home)
            self._options = options

        return options

    @property
    def paths(self):
        """ Tuple[Path]: Absolute path to each page in home folder. """
        home, paths, readlines = self.home, self._paths, self.readlines

        if paths is None:
            folder = home.parent
            pagepaths = folder / PAGEPATHS
            if pagepaths.is_file():
                paths = (x.strip() for x in readlines(pagepaths))
                paths = tuple(folder / x for x in paths if x)
            if not paths:
                paths = set(folder.rglob("*.html")) - {home}
                paths = (home, *sorted(paths))

            self._paths = paths

        return paths

    # File methods

    @classmethod
    def query(cls, page, **kwargs):
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

        cmds = "tidy -ashtml -bare -clean -indent -quiet -wrap 0".split()
        cmds += "--fix-style-tags no --show-body-only yes".split()
        cmds += ["-output", str(clean), str(dirty)]

        print("Tidy", clean)
        status = run(cmds).returncode
        if status and (status != 1):
            raise ChildProcessError("Tidy returned {}".format(status))

    @classmethod
    def urlpath(cls, page, url):
        """
        str: URL from page to (local file or remote URL).
        Inputs can be Path or str objects. Inputs must not be relative.
        """
        page, url = Path(page), str(url)

        if urlsplit(url).scheme:
            return url
        elif not url.startswith("/"):
            raise ValueError(f"ambiguous src: {src}")
        elif not page.is_absolute():
            raise ValueError(f"ambiguous page: {page}")
        else:
            return quote(relpath(url, page.parent))

    @classmethod
    def validpath(cls, path):
        """ Path: Absolute path. Raise error if path does not exist. """
        path = Path(path)

        return path if path.is_absolute() else path.resolve(strict=True)

    @classmethod
    def write(cls, text, path):
        """ None: Write text to selected path. """
        path = Path(path)

        with open(path, "w") as file:
            print("Write", path)
            file.write(str(text))
