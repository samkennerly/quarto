# Much Ado About Quartos

Quartos are designed to:

- build
  [lean](https://gomakethings.com/the-lean-web/)
  websites
- help beginners [learn HTML and CSS](https://neocities.org/tutorials)
- be modified and or copypasted into other projects
- avoid installing
  [500 packages](https://chriswarrick.com/blog/2019/02/15/modern-web-development-where-you-need-500-packages-to-build-bootstrap/)
  and
  [500 MB frameworks](https://medium.com/@mattholt/its-2019-and-i-still-make-websites-with-my-bare-hands-73d4eec6b7)
  to build a
  [5kB page](https://motherfuckingwebsite.com/).

See the [home page](index.html) for a quick tutorial.

## As You Like It

Quartos are templates to be copied and modified,
not frameworks to be installed and configured.
(Whether that's good or bad is a matter of
[taste](https://dhh.dk/2012/rails-is-omakase.html)).
All core code's
[one page](https://github.com/samkennerly/quarto/tree/master/quire/quire.py),
and all the styles and content merely folders.
If you don't like it, change it.

<dl>
<dt>Change the options</dt>
<dt>Change the pages</dt>
<dt>Change the styles</dt>
<dt>Change the code</dt>
</dl>

## Self-promotion is not so vile a sin.

### Quartos are small

- &nbsp; 1 Python module
- \+ 4 Python scripts
- \+ 0 [ten-ton widgets](https://css-tricks.com/ten-ton-widgets/)
- ≈ 500 lines of code

### Quartos are clean

- No installation.
- No environment variables.
- No files written outside its folder (unless you insist).
- No plugins, templates, frameworks, loggers, shims, wrappers, ...

### Quartos are lazy

- [Cat](https://en.wikipedia.org/wiki/Concatenation) strings without [schlemieling](https://en.wikichip.org/wiki/schlemiel_the_painter%27s_algorithm).
- Generate HTML
[lazily](https://en.wikipedia.org/wiki/Lazy_evaluation),
one line at a time.
- Build pages without copying images, audio, video, or any other files.
- Do not start any web servers, file watchers, event listeners, or any other
[busy loops](https://en.wikipedia.org/wiki/Busy_waiting).

### Quartos are independent

- No [requirements](https://github.com/samkennerly/quarto/blob/master/requirements.txt).
- Want to write pages in Markdown? In that case,
[one requirement](https://github.com/lepture/mistune).
- Build multiple quartos on the same machine without conflicts.
- No `setup.py`, `virtualenv`, `pipenv`, `__init__.py`, `__main__.py`, `sys.path` hacks,
dependency resolution trees, version conflicts, or upgrades.

To upgrade a quarto, copy the `quire` folder from a newer quarto.
There is no code outside the `quire` folder.


## We will draw the curtain and show you the HTML.

See the [source code]() for any web page:

<dl>
  <dt>Chrome</dt>
  <dd>View &gt; Developer &gt; View Source (<kbd>Ctrl+U, ⌥⌘U</kbd>)</dd>
  <dd>View &gt; Developer &gt; Developer Tools (<kbd>Ctrl+Shift+I, ⌥⌘I</kbd>)</dd>
  <dt>Firefox</dt>
  <dd>Tools &gt; Web Developer &gt; Page Source (<kbd>Ctrl+U, ⌘U</kbd>)</dd>
  <dd>Tools &gt; Web Developer &gt; Toggle Tools (<kbd>Ctrl+Shift+I, ⌥⌘I</kbd>)</dd>
</dl>

It should look something like this:
```
<!DOCTYPE html>
<html>
<head>
<title>
Quarto builds websites.
</title>
<link rel="canonical" href="https://quarto.neocities.org/index.html">
...
```

### The browser doth request too much, methinks.
### I cannot tell what the dickens this page is.
### I click to bury pop-ups, not to raise them.
### Load all, host a few, do wrong to none.




## Give the devs their due.

### `proof` images

- [galaxy.jpg](media/galaxy.jpg) by [NASA and ESA](https://commons.wikimedia.org/wiki/File:Hubble_view_of_barred_spiral_galaxy_Messier_83.jpg)
- [quarto.svg](media/quarto.svg) by [Molly Blair](https://mollyeblair.com/)

### `quire` code

- [Sam Kennerly](https://samkennerly.github.io/)

### `ready` pages

- [Sam Kennerly](https://samkennerly.github.io/)

### `style` sheets

- `adrift`, `burning`, `doctoral` by [Sam Kennerly](https://samkennerly.github.io/)
- `celestial` by [Jennifer Blair](https://jennifer-blair.com/)
and [Sam Kennerly](https://samkennerly.github.io/)
