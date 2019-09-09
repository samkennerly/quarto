"""
Run Quarto commands with `python3 -m quarto [COMMAND]`.
If no COMMAND is input, then show a help menu.
"""
import sys

from quarto import CSSPATH, Pages

HELP = f"""Quarto usage:

build [TARGET]
    Delete all HTML files in TARGET folder.
    Read main elements from ./ready folder.
    Build pages and save to TARGET folder.

catstyle STYLE [TARGET]
    Delete all CSS files in TARGET folder.
    Concatenate all CSS files in ./styles/STYLE folder.
    Save concatenated CSS file to TARGET/{CSSPATH}.
"""

script,*args = sys.argv
command,*args = args or ['help']
command = command.lower()

if command == 'build':
    Pages('.').build(*args)
elif command == 'catstyle':
    Pages('.').catstyle(*args)
elif command == 'help':
    print(HELP)
else:
    print('Unknown command:',command)
    print(HELP)
    sys.exit(2)
