import sys

from quarto import CSSPATH, Quarto

HELP = f"""
Quarto builds static websites.

Commands:

    build [PROJECT]
        1. Find raw HTML files in ./ready folder.
        2. Delete all HTML files in ./target folder.
        3. Rebuild new HTML files in ./target folder.
        Input PROJECT path to use a different base folder.

    catstyle STYLE [PROJECT]
        1. Concatenate CSS files in ./styles/STYLE
        2. Delete all CSS files in ./target
        3. Rebuild new ./target/{CSSPATH}
        Input PROJECT path to use a different base folder.

Examples:

    quarto build
    quarto catstyle doctoral

    quarto build ~/sites/kittens
    quarto catstyle cinematic ~/sites/kittens
"""


def fail(*args):
    print("Then fail, Quarto:", *args, file=sys.stderr)
    print("Run 'quarto help' to see all commands.")
    sys.exit(2)


args = iter(sys.argv)
script = next(args)
command = next(args, "help").lower()

if command == "build":
    Quarto(*args).build()

elif command == "catstyle":
    style = next(args, "") or fail("no style selected.")
    Quarto(*args).catstyle(style)

elif command == "help":
    print(HELP)

else:
    fail("unknown command:", command, *args)
