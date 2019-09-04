#!/usr/bin/env python

from setuptools import find_packages, setup


def read(path):
    with open(path) as f:
        return "".join(f)


kw = {
    "author": "Sam Kennerly",
    "author_email": "samkennerly@gmail.com",
    "classifiers": [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    "description": "Simple website builder.",
    "install_requires": [ ],
    "keywords": "html css css-grid python static-website",
    "license": read("LICENSE"),
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
    "name": "quarto",
    "package_data": {"": ["ready/*.html","ready/*.json","style.css"]},
    "package_dir": {"": ""},
    "packages": find_packages(),
    "python_requires": ">=3, <4",
    "url": "https://github.com/samkennerly/quarto",
    "version": "0.0.1",
}

if __name__ == "__main__":
    setup(**kw)
