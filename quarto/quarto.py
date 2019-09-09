from pathlib import Path

from .reader import querypage, readlines, stylesheet, tidybody, urlpath
from .stanza import CSSPATH, icons, jump, klf, links, meta, nav


class Quarto:
    """
    Find, read, and finish raw HTML files.
    """

    def __init__(self, folder="."):
        folder = Path(folder).resolve()
        paths = folder.glob("ready/**/*.html")
        home = folder / "ready/index.html"

        self.defaults = querypage(home)
        self.folder = folder
        self.paths = (home, *sorted(set(paths) - {home}))

    home = property(lambda self: self.paths[0])

    # Magic methods

    def __call__(self, i):
        return self.generate(i, **self.options(i))

    def __getitem__(self, i):
        return "\n".join(self(i))

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __len__(self):
        return len(self.paths)

    def __repr__(self):
        return f"Quarto({self.folder})"

    # Safety methods

    def abspath(self, *parts):
        """ Path: Ensure path is an absolute Path object in project folder. """
        folder = self.folder

        path = folder.joinpath(*parts)
        if folder not in path.parents:
            raise ValueError(f"{path} is outside {folder}")

        return path

    # Main methods

    def build(self):
        """ None: Generate and save all pages to target folder. """
        paths, vacuum, write = self.paths, self.vacuum, self.write

        homedir = paths[0].parent
        print("Build", len(paths), "pages in", homedir)

        vacuum(".html")
        for path, text in zip(paths, self):
            write(path.relative_to(homedir), text)

        print("What's done is done. Exeunt", self)

    def catstyle(self, style="doctoral"):
        """ None: Concatenate stylesheets and save to target folder. """
        folder, vacuum, write = self.folder, self.vacuum, self.write

        styledir = folder / "styles" / style
        print("Concatenate styles from", styledir)

        vacuum(".css")
        write(CSSPATH, stylesheet(styledir))

        print("The", CSSPATH, "of", self, "is", style)

    def errors(self):
        """ Tuple[str]: Check output for HTML errors. """
        raise NotImplementedError

    # Pagemakers

    def generate(self, i, title="", **kwargs):
        """ Iterator[str]: Generate lines in page. """
        paths = self.paths

        path = paths[i]
        main = map(str.rstrip, readlines(path))
        title = str(title or page.stem)

        yield "<!doctype html>"
        yield "<html>"
        yield "<head>"
        yield from ("<title>", title, "</title>")
        yield from links(paths, i, **kwargs)
        yield from meta(paths, i, **kwargs)
        yield "</head>"
        yield "<body>"
        yield from nav(paths, i, **kwargs)
        yield from ("<main>", *main, "</main>")
        yield from icons(paths, i, **kwargs)
        yield from jump(paths, i, **kwargs)
        yield from klf(paths, i, **kwargs)
        yield "</body>"
        yield "</html>"

    def options(self, i):
        """ dict: Page options with home options as defaults. """
        defaults, paths = self.defaults, self.paths

        return {**defaults, **(querypage(paths[i]) or dict())}

    # Dangerous methods

    def vacuum(self, suffix=".html"):
        """ None: Delete all files in target folder with selected suffix. """
        target = self.abspath("target")

        suffix = "." + suffix.lstrip(".")
        for path in target.rglob("*"):
            if path.suffix == suffix:
                print("Delete", path)
                path.unlink()

    def write(self, path, text):
        """ None: Save text to file in target folder. """
        path = self.abspath("target", path)

        print("Write", path)
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as file:
            print(text, file=file)
