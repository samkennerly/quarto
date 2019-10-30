# Paths

Quartos try to wrangle file
[paths](https://en.wikipedia.org/wiki/Path_%28computing%29)
into valid
[URLs](https://en.wikipedia.org/wiki/URL),
but sometimes they need help.

---

## pages.txt

Quarto scripts find pages
[recursively](https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob),
then
[lexsort](https://en.wikipedia.org/wiki/Lexicographical_order)
them and move `index.html` to the front of the queue.
If you don't like the result, you can find and sort pages yourself:

- Create a `pages.txt` file in the `ready` folder.
- On each line, type the
[relative path](https://en.wikipedia.org/wiki/Path_%28computing%29#Absolute_and_relative_paths)
from the `ready` folder to a page.
- Sort pages in any order you want. Quarto scripts will respect it.
- Any blank lines and leading/trailing whitespace will be ignored.

In this example, `about.html` will be the *last* link in each &lt;nav&gt; menu:
```
index.html
boxes/can/be/nested.html
cat_pics/octocats.html
about.html
```
Sites will build slightly faster if `pages.txt` exists.

---

## Quoted URLs

Quarto scripts automatically
[quote](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)
file paths when:

- building a &lt;nav&gt; menu
- generating &lt;script&gt; tags
- generating &lt;img&gt; tags in an `#icons` section
- generating &lt;link&gt; tags in a &lt;head&gt; element

If your `ready` pages include
[prohibited characters](https://www.w3.org/Addressing/URL/4_Recommentations.html),
then you may need to quote them manually.

---

## Relative paths

Quartos use
[relative paths](https://www.w3.org/TR/WD-html40-970917/htmlweb.html#h-5.1.2)
to avoid
[problems](https://github.com/jekyll/jekyll/issues/5482)
[when](https://github.com/jekyll/jekyll/issues/5488)
[previewing](https://github.com/jekyll/jekyll/issues/5743)
[pages](https://github.com/jekyll/jekyll/issues/5895)
[from](https://github.com/jekyll/jekyll/issues/6034)
[local](https://github.com/jekyll/jekyll/issues/6360)
[files](https://github.com/jekyll/jekyll/issues/7621).
Links which work
[locally](https://www.lifewire.com/how-to-preview-web-pages-3469885)
should still work when you upload your site - but test them to be sure!

For example, this page's &lt;nav&gt; menu links to:

```
../index.html
../about.html
../boxes/can/be/nested.html
../cat_pics/octocats.html
```
Each &lt;nav&gt; also has one link to itself which is a
[blank anchor](https://stackoverflow.com/questions/4855168/what-is-href-and-why-is-it-used).

---

## Spaces and Cases

Links in the &lt;nav&gt; menu use page filenames as labels.
To avoid problems with
[whitespace](https://stackoverflow.com/questions/497908/is-a-url-allowed-to-contain-a-space)
and/or
[capitalization](https://en.wikipedia.org/wiki/Case_sensitivity)
in file names, consider these alternatives:

- spaces
  - Use underscores instead of spaces in file and folder names.
  - Quarto scripts automatically replace each `_` with a space in &lt;nav&gt; labels.

- cases
  - Use lowercase file and folder names.
  - Use
[CSS text-transform](https://css-tricks.com/almanac/properties/t/text-transform/)
in stylesheets to capitalize &lt;nav&gt; labels.

Quarto scripts do <mark>not</mark> enforce these rules.
Break them if you want to.
