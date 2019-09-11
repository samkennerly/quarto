import sys

from quartocat import CSSPATH, Quarto

HELP = f"""
Build static websites quickly with Python 3.

Commands:

    apply STYLE [PROJECT]
        0. Default PROJECT is current working directory.
        1. Concatenate CSS files in PROJECT/styles/STYLE
        2. Delete all CSS files in PROJECT/target
        3. Rebuild new PROJECT/target/{CSSPATH}

    build [PROJECT]
        0. Default PROJECT is current working directory.
        1. Find raw HTML files in PROJECT/ready folder.
        2. Delete all HTML files in PROJECT/target folder.
        3. Rebuild new HTML files in PROJECT/target folder.

    help
        0. Show this menu

More information:

    https://github.com/samkennerly/quartocat
"""


def fail(*args):
    print("***", *args, file=sys.stderr)
    print("Run 'quartocat help' to see all commands.")
    sys.exit(2)


args = iter(sys.argv)
script = next(args)
command = next(args, "help").lower()

if command == "apply":
    style = next(args, "") or fail("style name is required")
    Quarto(*args).apply(style)
elif command == "build":
    Quarto(*args).build()
elif command == "help":
    print(HELP)
else:
    fail("Unknown command:", script, command, *args)
