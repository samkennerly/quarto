from pathlib import Path

from .readers import querypage, stylesheet
from .stanzas import CSSPATH, generate


class Quarto:
    """
    Find, read, and finish raw HTML files.
    """

    def __init__(self, folder="."):
        folder = Path(folder).resolve()
        paths = folder.glob("ready/**/*.html")
        home = folder / "ready/index.html"

        self._options = querypage(home)
        self.folder = folder
        self.paths = (home, *sorted(set(paths) - {home}))

    # Magic methods

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

    # User methods

    def apply(self, style="doctoral"):
        """ None: Concatenate stylesheets and save to target folder. """
        folder, vacuum, write = self.folder, self.vacuum, self.write

        styledir = folder / "styles" / style
        print("Apply style from", styledir)

        if not styledir.is_dir():
            raise NotADirectoryError(styledir)

        vacuum(".css")
        write(CSSPATH, stylesheet(styledir))

        print("The", CSSPATH, "of", self, "is", style)

    def build(self):
        """ None: Generate and save all pages to target folder. """
        paths, vacuum, write = self.paths, self.vacuum, self.write

        homedir = paths[0].parent
        print("Build", len(paths), "pages from", homedir)

        vacuum(".html")
        for path, text in zip(paths, self):
            write(path.relative_to(homedir), text)

        print("What's done is done. Exeunt", self)

    def clean(self):
        """ None: Replace target pages with standardized HTML5. """
        raise NotImplementedError

    def decapitate(self):
        """ None: Remove <head> and non-<body> elements from raw pages. """
        raise NotImplementedError

    def errors(self):
        """ Tuple[str]: HTML5 errors detected in output pages. """
        raise NotImplementedError

    # File methods

    def options(self, i):
        """ dict: Page options with home options as defaults. """
        return {**self._options, **querypage(self.paths[i])}

    def vacuum(self, suffix=".html"):
        """ None: Delete all files in target folder with selected suffix. """
        target = self.folder / "target"

        pattern = "**/*." + suffix.lstrip(".")
        print("Vacuum {}/{}".format(target, pattern))

        for path in target.glob(pattern):
            print("Delete", path)
            path.unlink()

    def write(self, path, text):
        """ None: Save text to file in target folder. """
        target = self.folder / "target"

        path = target / path
        print("Write", path)

        if target not in path.parents:
            raise ValueError("{} is outside {}".format(path, target))

        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as file:
            print(text, file=file)
