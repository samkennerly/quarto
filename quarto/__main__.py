import sys

from quarto import CSSPATH, Quarto

HELP = """
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
        3. Rebuild new ./target/{}
        Input PROJECT path to use a different base folder.

Examples:

    quarto build
    quarto catstyle doctoral

    quarto build ~/sites/kittens
    quarto catstyle cinematic ~/sites/kittens
""".format(CSSPATH)

def build(folder='.'):
    Quarto(folder).build()

def catstyle(style,folder='.'):
    Quarto(folder).catstyle(style)

def fail(*args):
    print('Then fail, Quarto!')
    sys.exit(2)

args = iter(sys.argv)
script = next(args)
command = next(args,'help').lower()

if command == 'build':
    build(*args)
elif command == 'catstyle':
    catstyle(*args)
elif command == 'help':
    print(HELP)
else:
    print('*** Unknown command:',command,*args)
    print("Run 'quarto help' to see all commands.")
    fail()
