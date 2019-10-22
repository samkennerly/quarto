# Build websites with Python.

Quartos build websites. (This site is one.)
Scroll through these stanzas to see how it's done.

---

## Copy this quarto.

A <dfn>quarto</dfn> is four [folders]() in a fifth folder:

- **`proof`**
  is a [proof copy]() of a [static website]().
- **`quire`**
  is a [Python package]() which builds the `proof`.
- **`ready`**
  stores HTML or [Markdown]() pages and page
  [options](docs/options.html).
- **`style`**
  stores [stylesheets](). Use
  [the](examples/adrift.html)
  [four](examples/burning.html)
  [quarto](examples/celestial.html)
  [styles](examples/doctoral.html)
  or create your own.

Download a ZIP or [generate a repo]() from the original <q>stock</q> quarto:

[github.com/samkennerly/quarto]("https://github.com/samkennerly/quarto")

Name your first quarto anything you like.
Mine is called [badquarto](https://github.com/samkennerly/badquarto/).

---

## Install extras?

**Python 3.6+** is required to run `quire` scripts.
Some features require [extras]():

- **[Tidy 5+]()** to clean HTML files with `quire/clean`
- **[Mistune]()** to build pages from [Markdown]() files
- <del>Bottle to run a web server</del>
  <mark>under construction</mark>
- <del>ImageMagick to build galleries</del>
  <mark>under construction</mark>

Quartos do not need to be installed. To remove a quarto, delete it.

---

## Rewrite the pages.

Any
[plain text]()
editor can read and write quarto pages, options, styles, and code.

**Remove the stock pages.**

Delete everything in the `ready` folder except these files:
```
ready/index.html
ready/index.json
```
Any change you might regret can be undone with
[git reset]("https://git-scm.com/docs/git-reset).

**Write a new page.**

Create `ready/bad.html` with this text:
```
<h1>404 Foul Papers</h1>

<p>To be, or not to be?<br>Aye, there's the point.</p>

<figure>
  <img alt="Quarto logo" src="media/quarto.svg" width="256">
  <figcaption>
    This page was not built by a
    <a href="https://github.com/samkennerly/quarto">quarto<a>.
  </figcaption>
</figure>
```
The image `src` is a
[relative path](https://www.w3schools.com/html/html_filepaths.asp)
to a file in the `proof` folder.

**Edit the home options.**

Replace `ready/index.json` with this text:
```
{
  "base": "https://quarto.test/",
  "email": "",
  "homelink": "Bad Quarto",
  "meta": {
    "author": "Wm. Shakespeare?",
    "description": "What links in yonder website break?",
  },
  "nextlink": "fore",
  "prevlink": "aft",
  "qlink": "Fouled by a quarto."
  "styles": ["style.css"],
  "title": "Quarto test website."
}
```
Options are optional. Delete anything you don't want.

**Add some page options.**

Create `ready/bad.json` with this text:
```
{
  "meta": {
    "description": "No is the status of our GET request."
  },
  "title": "The Tragedy of Errors",
}
```
Home options are used to fill missing values in page options.

---

## Build your new quarto.

Open a
[terminal]()
and `cd` to your quarto.

**Delete** leftover pages and stylesheets from the `proof` folder:
```
quire/delete html
quire/delete css
```
For safety reasons, this will only delete HTML and CSS files.
It will not remove all the cat pics in the `media` folder.

**Clean** HTML files in the `ready` folder
```
quire/clean
```
`quire/clean` <mark>overwrites</mark> the original HTML files.
Keep your
[foul papers](https://en.wikipedia.org/wiki/Foul_papers)
in another folder if you want to preserve them.

**Build** new pages with `ready` pages as [main elements]():
```
quire/build
```
`quire/build` does not copy large files, start a web server, or defrost your refrigerator. It only generates and writes HTML files.

**Apply** a style from the `style` folder:
```
quire/apply style/celestial
```
`quire/apply` recursively finds all CSS files in a folder and
[cats]()
them into one file.
It does not parse or compile CSS.

Open `proof/index.html` in any browser to behold your brave new quarto.

To publish your website, upload the `proof` folder to a
[host]().
This site uses
[Neocities](neocities.org).
