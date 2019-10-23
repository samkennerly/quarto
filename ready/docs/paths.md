# Paths

Links that work when you preview pages
[locally](https://www.lifewire.com/how-to-preview-web-pages-3469885)
should still work when you upload your site.

To avoid
[problems](https://github.com/jekyll/jekyll/issues/5482)
[with](https://github.com/jekyll/jekyll/issues/5488)
[viewing](https://github.com/jekyll/jekyll/issues/5743)
[local](https://github.com/jekyll/jekyll/issues/5895)
[files](https://github.com/jekyll/jekyll/issues/6034)
[in](https://github.com/jekyll/jekyll/issues/6360)
[browsers](https://github.com/jekyll/jekyll/issues/7621),
quartos build &lt;nav&gt; menus with
[relative paths](https://www.w3.org/TR/WD-html40-970917/htmlweb.html#h-5.1.2).
For example, this page's &lt;nav&gt; menu includes links like this:

```
../index.html
../about.html
../boxes/can/be/nested.html
../cat_pics/octocats.html
```
Each page also has one link to itself which is a
[blank anchor](https://stackoverflow.com/questions/4855168/what-is-href-and-why-is-it-used).

---

## pages.txt

By default, the `quire/build` script finds all HTML and MD files in the `ready` folder
[recursively](https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob),
sorts them
[lexicographically](),
and moves `index.html` to the front of the queue.

To find and sort pages manually, create a `ready/pages.txt` file.
Each line should be a relative path from the `ready` folder to a page.
Blank lines and leading/trailing whitespace are ignored.

In this example, `about.html` will be the *last* link in each &lt;nav&gt; menu:
```
index.html
boxes/can/be/nested.html
cat_pics/octocats.html
about.html
```

---

## UNDER CONSTRUCTION

## Quoted URLs
## Relative URLs
## Spaces and Caps
