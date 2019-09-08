#!/usr/bin/env python3

from sys import argv as ARGV

from quarto import CSSPATH, Pages

HELP = f"""
Quarto usage:

build [TARGET]
    Delete all HTML files in TARGET folder.
    Read main elements from ./ready folder.
    Build pages and save to TARGET folder.

catstyle STYLE [TARGET]
    Delete all CSS files in TARGET folder.
    Concatenate all CSS files in ./styles/STYLE folder.
    Save concatenated CSS file to TARGET/{CSSPATH}.
"""

script,*args = ARGV
action,*args = args or ('help')

if action == 'build':
    Pages('.').build(*args)
elif action == 'catstyle':
    Pages('.').catstyle(*args)
else:
    print(HELP)
