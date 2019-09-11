from pathlib import Path

from .reader import querypage, stylesheet
from .stanza import CSSPATH, generate


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

    def __call__(self, i):
        return generate(self.paths, i, **self.options(i))

    def __getitem__(self, i):
        return "\n".join(self(i))

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __len__(self):
        return len(self.paths)

    def __repr__(self):
        return f"Quarto({self.folder})"

    def abspath(self, *parts):
        """ Path: Ensure path is an absolute Path object in project folder. """
        folder = self.folder

        path = folder.joinpath(*parts)
        if folder not in path.parents:
            raise ValueError(f"{path} is outside {folder}")

        return path

    def build(self):
        """ None: Generate and save all pages to target folder. """
        paths, vacuum, write = self.paths, self.vacuum, self.write

        homedir = paths[0].parent
        print("Build", len(paths), "pages from", homedir)

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

    def options(self, i):
        """ dict: Page options with home options as defaults. """
        defaults, paths = self.defaults, self.paths

        return {**defaults, **(querypage(paths[i]) or dict())}

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
