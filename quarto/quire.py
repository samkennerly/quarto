from collections.abc import Mapping
from json import load as jsonload
from os.path import relpath
from pathlib import Path
from posixpath import join as posixjoin
from subprocess import run
from urllib.parse import quote, urlsplit

try:
    from mistune import Markdown

    mdparse = Markdown().parse
except ImportError as err:

    def mdparse(text, err=err):
        """ None: Show error caused by trying to import Markdown parser. """
        raise ImportError(f"Cannot parse Markdown: {err}")


class Quire(Mapping):
    """
    Generate web pages from HTML fragments and/or Markdown files.

    Quire is an ordered, immutable { pathlib.Path: str } Mapping.
    .keys() are absolute pathlib.Path objects for unfinished pages.
    .values() are HTML pages as strings. Values are generated lazily.

    Initialize a Quire with the path to a folder containing raw pages.
    Quire accepts absolute or relative Path objects or strings as input.
    Quire looks for a "pages.txt" file with newline-separated page paths.
    If "pages.txt" does not exist, then it finds .html files recursively.

    Page options (title, description, etc.) may be stored in JSON files.
    If index.json exists, then its values are defaults for all page options.
    Each JSON file must have the same path as its page, but with a .json suffix.

    Call help(Quire) for more information.
    """

    def __init__(self, folder="."):
        self.folder = Path(folder).resolve()
        self._home = None
        self._options = None
        self._pages = None

    # Magic methods

    def __call__(self, page):
        """ Iterator[str]: Lines of generated page. """
        return self.generate(page, **self.query(page, **self.options))

    def __getitem__(self, page):
        """ str: Generated page as a single string. """
        return "\n".join(self(page))

    def __iter__(self):
        """ Iterable[Path]: Absolute Path to each main element. """
        return iter(self.pages)

    def __len__(self):
        """ int: Number of main elements found. """
        return len(self.pages)

    def __repr__(self):
        """ str: Printable representation of self. """
        return f"{type(self).__name__}({self.folder})"

    # Commands

    @classmethod
    def apply(cls, style, sheet):
        """ None: Cat CSS files from style folder and write to one file. """
        stylecat, write = cls.stylecat, cls.write

        style = "".join(map(str.strip, stylecat(style)))
        print("Write", sheet)
        write(style, sheet)

    def build(self, target):
        """ None: Generate each page and write to target folder. """
        folder, items, write = self.folder, self.items, self.write

        target = Path(target).resolve()
        for path, text in items():
            path = target / path.relative_to(folder).with_suffix(".html")
            print("Write", path)
            write(text, path)

    @classmethod
    def clean(cls, source, target):
        """ None: Save clean page <body> contents to target folder. """
        tidybody = cls.tidybody

        source = Path(source).resolve()
        target = Path(target).resolve()
        for dirty in source.rglob("*.html"):
            clean = target / dirty.relative_to(source)
            print("Tidy", clean)
            tidybody(dirty, clean)

    @classmethod
    def delete(cls, suffix, target):
        """ None: Remove files with selected suffix. """

        suffix = str(suffix).lstrip(".")
        target = Path(target).resolve()
        for path in target.rglob("*." + suffix):
            print("Delete", path)
            path.unlink()

    # Page generator

    def generate(self, page, language="", **kwargs):
        """ Iterator[str]: All lines in page. """
        language = kwargs.setdefault("language", "en")
        title = kwargs.setdefault("title", page.stem.replace("_", ""))

        yield "<!DOCTYPE html>"
        yield f'<html lang="{language}">'
        yield "<head>"
        yield f"<title>{title}</title>"
        yield from self.links(page, **kwargs)
        yield from self.meta(page, **kwargs)
        yield "</head>"
        yield "<body>"
        yield from self.nav(page, **kwargs)
        yield "<main>"
        if page.suffix == ".md":
            yield mdparse("".join(self.readlines(page)))
        else:
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
            found = (x for x in folder.glob("index.*") if x.suffix != ".json")
            home = next(found, None)
            if not home:
                raise FileNotFoundError(folder / "index.html")
            if any(found):
                raise ValueError("Multiple homepages")

            self._home = home

        return home

    # Tag generators

    def icons(self, page, icons=(), **kwargs):
        """
        Iterator[str]: #icons section for links to social media, etc.
        Links can be JPEGs, PNGs, ICOs or even GIFs.
        Consider SVG so there's no scaling glitch. (I love it.)
        """
        urlpath = self.urlpath

        yield '<section id="icons">'
        for alt, src, href in icons:
            src = urlpath(page, src)
            alt = f'<img alt="{alt}" src="{src}" height="32" title="{alt}">'
            yield f'<a href="{href}">{alt}</a>'
        yield "</section>"

    def jump(self, page, jscripts=(), nextlink="", prevlink="", updog="", **kwargs):
        """
        Iterator[str]: #jump section for scripts and previous/up/next links.
        And I know, reader, just how you feel.
        You got to scroll past the pop-ups to get to what's real.
        """
        pages, urlpath = self.pages, self.urlpath

        i, n = pages.index(page), len(pages)
        urlprev = urlpath(page, pages[(i - 1) % n].with_suffix(".html"))
        urlnext = urlpath(page, pages[(i + 1) % n].with_suffix(".html"))

        yield '<section id="jump">'
        if prevlink:
            yield f'<a href="{urlprev}" rel="prev">{prevlink}</a>'
        if updog:
            yield f'<a href="#" id="updog">{updog}</a>'
        if nextlink:
            yield f'<a href="{urlnext}" rel="next">{nextlink}</a>'
        for src in jscripts:
            yield f'<script src="{urlpath(src)}" async></script>'
        yield "</section>"

    def klf(
        self, page, copyright="", email="", klftext="", license=(), qlink="", **kwargs
    ):
        """
        Iterator[str]: #klf section for copyright, license, and fine print.
        They're justified, and they're ancient. I hope you understand.
        """
        urlpath = self.urlpath

        yield '<section id="klf">'
        if copyright:
            yield f'<span id="copyright">{copyright}</span>'
        if license:
            href, text = license
            yield f'<a href="{urlpath(page, href)}" rel="license">{text}</a>'
        if qlink:
            yield f'<a href="https://quarto.neocities.org/">{qlink}</a>'
        if klftext:
            yield f'<span id="klftext">{klftext}</span>'
        if email:
            yield f"<address>{email}</address>"
        yield "</section>"

    def links(self, page, base="", favicon="", styles=(), **kwargs):
        """ Iterator[str]: <link> tags in page <head>. """
        home, urlpath = self.home, self.urlpath

        page = page.with_suffix(".html")
        link = '<link rel="{}" href="{}">'.format
        if base:
            yield link("canonical", posixjoin(base, urlpath(home, page)))
        if favicon:
            yield link("icon", urlpath(page, favicon))
        for sheet in styles:
            yield link("stylesheet", urlpath(page, sheet))

    def meta(self, page, author="", description="", meta=(), ogimage="", **kwargs):
        """ Iterator[str]: <meta> tags in page <head>. """
        home, urlpath = self.home, self.urlpath

        mtag = '<meta name="{}" content="{}">'.format
        ogtag = '<meta property="og:{}" content="{}">'.format

        yield '<meta charset="utf-8">'
        yield '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        if author:
            yield mtag("author", author)
        if description:
            yield mtag("description", description)
        if ogimage:
            yield ogtag("image", urlpath(page, ogimage))
        for k, v in dict(meta).items():
            yield mtag(k, v)
        yield mtag("generator", "https://quarto.neocities.org/")

    def nav(self, page, homelink="home", **kwargs):
        """ Iterator[str]: <nav> element with links to other pages in site. """
        home, pages, urlpath = self.home, self.pages, self.urlpath

        opendirs = frozenset(page.parents)
        workdirs = frozenset(home.parents)

        yield "<nav>"
        for p in pages:

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
        """ dict: Home page options from JSON file. """
        options = self._options

        if options is None:
            options = self.query(self.folder / "index.json")
            self._options = options

        return options

    @property
    def pages(self):
        """ Tuple[Path]: Absolute path to each page in home folder. """
        pages = self._pages

        if pages is None:
            folder = self.folder
            pages = folder / "pages.txt"
            if pages.is_file():
                pages = map(str.strip, self.readlines(pages))
                pages = tuple(folder / x for x in pages if x)
            else:
                home = self.home
                pages = folder.rglob("*.*")
                pages = (x for x in pages if x.suffix in (".html", ".md"))
                pages = (home, *sorted(x for x in pages if x != home))

            self._pages = pages

        return pages

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
        return cls.readlines(*sorted(Path(style).rglob("*.css")))

    @classmethod
    def tidybody(cls, dirty, clean):
        """ None: Clean raw HTML page and save. Requires HTML Tidy >= 5. """
        dirty, clean = Path(dirty), Path(clean)

        cmds = ["tidy", "-ashtml", "-bare", "-clean", "-indent", "-quiet"]
        cmds += ["--fix-style-tags", "n", "--vertical-space", "n", "-wrap", "0"]
        cmds += ["--show-body-only", "y", "-output", str(clean), str(dirty)]

        if not dirty.exists():
            raise FileNotFoundError(dirty)

        clean.parent.mkdir(exist_ok=True, parents=True)
        status = run(cmds).returncode
        if status and (status != 1):
            raise ChildProcessError("Tidy error status {}".format(status))

    def urlpath(self, page, target):
        """
        str: URL from page to target.
        Target can be an absolute URL, absolute path, or path from base folder.
        """
        folder = self.folder

        page = folder / page
        target = str(target)
        if not urlsplit(target).scheme:
            target = folder / target
            target = quote(relpath(target, start=page.parent.as_posix()))

        return target

    @classmethod
    def write(cls, text, path):
        """ None: Write text to selected path. """
        path, text = Path(path), str(text)

        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as file:
            file.write(text)


# Copyright © 2020 Sam Kennerly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
