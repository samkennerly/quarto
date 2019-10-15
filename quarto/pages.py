from collections.abc import Mapping
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from posixpath import join as posixjoin
from subprocess import run
from urllib.parse import quote, urlsplit


class Pages(Mapping):
    """
    Pages(folder=".")

    Generate web pages from HTML fragments.

    Pages is an ordered, immutable { pathlib.Path: str } Mapping.
    Each key is an absolute path to the <main> element of a web page.
    Each value is a finished web page. Values are generated lazily.

    Initialize a Pages object with a base folder.
    Pages accepts absolute or relative path-like objects.

    Pages looks for newline-separated raw page paths in "pages.txt".
    If that file does not exist, then it finds .html files recursively.

    Page options (title, description, etc.) may be stored in JSON files.
    If index.json exists, then its values are defaults for all page options.
    Each JSON file must have the same path as its page, but with a .json suffix.

    Call help(Pages) for more information.
    """

    OPTIONS = "index.json"
    PATHS = "pages.txt"
    QHOME = "https://github.com/samkennerly/quarto"

    def __init__(self, folder="."):
        self.folder = self.validpath(folder)
        self._home = None
        self._options = None
        self._paths = None

    # Magic methods

    def __call__(self, page):
        """ Iterator[str]: Lines of generated page. """
        return self.generate(page, **self.query(page, **self.options))

    def __fspath__(self):
        """ str: String representation of base folder. """
        return str(self.folder)

    def __getitem__(self, page):
        """ str: Generated page as a single string. """
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
        """ Path: Absolute path. If input is relative, then append to base """
        return self.folder / pathlike

    # Commands

    @classmethod
    def apply(cls, style, sheet):
        """ None: Cat CSS files from style folder and write to one file. """
        cls.write("".join(cls.stylecat(style)), sheet)

    def build(self, target):
        """ None: Generate each page and write to target folder. """
        write = self.write
        target = self.validpath(target)
        for path, text in self.items():
            path = target / path.relative_to(self).with_suffix(".html")
            write(text, path)

    def clean(self, ready):
        """ None: Save cleaned page bodies to ready folder. """
        tidy = self.tidy
        ready = self.validpath(ready)
        for dirty in self:
            clean = ready / dirty.relative_to(self)
            tidy(dirty, clean)

    @classmethod
    def delete(cls, suffix, target):
        """ None: Remove files with selected suffix and any empty folders. """
        target = cls.validpath(target)
        pattern = "*." + suffix.lstrip(".")
        for path in target.rglob(pattern):
            print("Delete", path)
            path.unlink()

    # Page generator

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
        yield from self.nav(page, **kwargs)
        yield "<main>"
        yield from map(str.rstrip, self.readlines(page))
        yield "</main>"
        yield from self.icons(page, **kwargs)
        yield from self.jump(page, **kwargs)
        yield from self.klf(page, **kwargs)
        yield "</body>"
        yield "</html>"
        yield ""

    # Home page

    @property
    def home(self):
        """ Path: Absolute path to home page. """
        home = self._home

        if home is None:
            folder = self.folder
            found = [x for x in folder.glob("index.*") if x.suffix != ".json"]
            if not found:
                raise FileNotFoundError(folder / "index.html")
            home = found.pop()
            if found:
                raise ValueError(f"multiple homepages: {found}")

            self._home = home

        return home

    # Tag generators

    def icons(self, page, icons=(), nextlink="", prevlink="", **kwargs):
        """
        Iterator[str]: Links drawn with JPEGs, PNGs, ICOs or even GIFs.
        Consider SVGs so there's no scaling glitch. (I love it.)
        """
        folder, paths, urlpath = self.folder, self.paths, self.urlpath

        page = folder / page
        i, n = paths.index(page), len(paths)

        yield '<section id="icons">'
        if prevlink:
            href = urlpath(page, (paths[(i - 1) % n]).with_suffix(".html"))
            yield f'<a href="{href}" rel="prev">{prevlink}</a>'

        for alt, src, href in icons:
            src = urlpath(page, folder / src)
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
        QHOME = self.QHOME

        yield '<section id="klf">'
        if copyright:
            yield f'<span id="copyright">{copyright}</span>'
        if license:
            yield '<a href="{}" rel="license">{}</a>'.format(*license)
        if email:
            yield f"<address>{email}</address>"
        if qlink:
            yield f'<a href="{QHOME}" rel="generator">{qlink}</a>'
        yield "</section>"

    def links(self, page, base="", favicon="", styles=(), **kwargs):
        """ Iterator[str]: <link> tags in page <head>. """
        home, urlpath = self.home, self.urlpath

        folder = home.parent
        page = (folder / page).with_suffix(".html")
        link = '<link rel="{}" href="{}">'.format

        if base:
            yield link("canonical", posixjoin(base, urlpath(home, page)))
        if favicon:
            yield link("icon", urlpath(page, folder / favicon))
        for sheet in styles:
            yield link("stylesheet", urlpath(page, folder / sheet))

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

        page = home.parent / page
        opendirs = frozenset(page.parents)
        workdirs = frozenset(home.parents)

        yield "<nav>"
        for p in paths:

            context = workdirs
            workdirs = frozenset(p.parents)
            yield from ("</details>" for _ in (context - workdirs))
            for d in sorted(workdirs - context):
                name = d.stem.replace("_", " ")
                if d in opendirs:
                    yield f"<details open><summary>{name}</summary>"
                else:
                    yield f"<details><summary>{name}</summary>"

            name = p.stem.replace("_", " ")
            href = "#" if (p == page) else urlpath(page, p.with_suffix(".html"))
            if p == home:
                yield f'<a href="{href}" rel="home">{homelink}</a>'
            else:
                yield f'<a href="{href}">{name}</a>'

        yield from ("</details>" for _ in (workdirs - set(home.parents)))
        yield "</nav>"

    # File methods

    @property
    def options(self):
        """ dict: Default page options from JSON file. """
        options = self._options

        if options is None:
            options = self.query(self.folder / self.OPTIONS)
            self._options = options.copy()

        return options

    @property
    def paths(self):
        """ Tuple[Path]: Absolute path to each page in home folder. """
        paths = self._paths

        if paths is None:
            folder = self.folder
            paths = folder / self.PATHS
            if paths.is_file():
                readlines = self.readlines
                print("Find pages from", paths)
                paths = (x.strip() for x in readlines(paths))
                paths = tuple(folder / x for x in paths if x)
            else:
                home = self.home
                print("Find pages in", folder)
                paths = (x for x in folder.rglob("*.html") if x != home)
                paths = (home, *sorted(paths))

            self._paths = paths

        return paths

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
        """ Iterator[str]: Concatenate CSS files in style folder. """
        return cls.readlines(*sorted(cls.validpath(style).glob("*.css")))

    @classmethod
    def tidy(cls, dirty, clean):
        """ None: Clean raw HTML page and save. Requires HTML Tidy >= 5. """
        dirty, clean = Path(dirty), Path(clean)

        cmds = ["tidy", "-ashtml", "-bare", "-clean", "-quiet", "-wrap", "0"]
        cmds += ["--fix-style-tags", "n", "--vertical-space", "y"]
        cmds += ["--show-body-only", "y", "-output", str(clean), str(dirty)]

        if not dirty.exists():
            raise FileNotFoundError(dirty)

        print("Tidy", clean)
        clean.parent.mkdir(exist_ok=True, parents=True)
        status = run(cmds).returncode
        if status and (status != 1):
            raise ChildProcessError("Tidy returned {}".format(status))

    @classmethod
    def urlpath(cls, page, src):
        """
        str: URL from page to (local file or remote URL).
        Inputs must be absolute path-like objects.
        """
        page, src = Path(page), posixjoin(src)

        if urlsplit(src).scheme:
            return src
        elif not src.startswith("/"):
            raise ValueError(f"ambiguous src: {src}")
        elif not page.is_absolute():
            raise ValueError(f"ambiguous page: {page}")
        else:
            return quote(relpath(src, start=page.parent.as_posix()))

    @classmethod
    def validpath(cls, path):
        """ Path: Absolute path. Raise error if path does not exist. """
        path = Path(path)

        return path if path.is_absolute() else path.resolve(strict=True)

    @classmethod
    def write(cls, text, path):
        """ None: Write text to selected path. """
        path = Path(path)

        print("Write", path)
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as file:
            file.write(str(text))
