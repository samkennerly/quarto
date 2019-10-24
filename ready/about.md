# Much Ado About Quartos

Quartos are designed to:

- build
  [lean](https://gomakethings.com/the-lean-web/)
  websites
- help beginners [learn HTML and CSS](https://neocities.org/tutorials)
- be modified by [Python](https://www.python.org/) programmers
- be copied, pasted, and shared with anyone

See the [home page](index.html) for a quick tutorial.

## Self-promotion is not so vile a sin.

Quartos build
[5k pages](https://motherfuckingwebsite.com/)
with
[500 lines of code](https://github.com/samkennerly/quarto/tree/master/quire),
not
[500M frameworks](https://medium.com/@mattholt/its-2019-and-i-still-make-websites-with-my-bare-hands-73d4eec6b7)
with
[500 packages](https://chriswarrick.com/blog/2019/02/15/modern-web-development-where-you-need-500-packages-to-build-bootstrap/).

### Brevity is the soul of `git`.

- &nbsp; 1 module
- \+ 4 scripts
- \+ 0 [ten-ton widgets](https://css-tricks.com/ten-ton-widgets/)
- = 1 `quire` folder

### Run cleanly, as a simple script should do.

- No
[hidden variables](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file).
- No files written outside its folder (unless you insist).
- No plugins, templates, frameworks, loggers, shims, wrappers, or
[dinguses](https://en.wiktionary.org/wiki/dingus).
- Scripts are in the `quire` folder, not the `/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/quarto/quire/bin/scripts` folder.

### Write out thy lines with stateless lazy-lists.

- [Cat](https://en.wikipedia.org/wiki/Concatenation) strings without [schlemieling](https://en.wikichip.org/wiki/schlemiel_the_painter%27s_algorithm).
- Generate HTML
[lazily](https://en.wikipedia.org/wiki/Lazy_evaluation),
one line at a time.
- Build pages without copying images, audio, video, or any other files.
- Do not start any web servers, file watchers, event listeners, or
[busy loops](https://en.wikipedia.org/wiki/Busy_waiting).

### What can be happier than to despise all package installs?

- No installation.
- [Extras](https://www.python.org/dev/peps/pep-0508/#extras),
not [requirements](https://github.com/samkennerly/quarto/blob/master/requirements.txt).
- No
[combinatorial explosions](https://en.wikipedia.org/wiki/Combinatorial_explosion)
of
[implicit dependencies](https://www.davidhaney.io/npm-left-pad-have-we-forgotten-how-to-program/).
- Build multiple quartos on the same machine without conflicts.

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





## Use as much of this code as please you.

Quartos are templates to be copied and modified,
not frameworks to be installed and configured.
(Whether that's good or bad is a matter of
[taste](https://dhh.dk/2012/rails-is-omakase.html)).
All core code's
[one page](https://github.com/samkennerly/quarto/tree/master/quire/quire.py),
and all the styles and content merely folders.


To <q>install</q> a quarto,
[copy it](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template).
To <q>upgrade</q> a quarto, copy the `quire` folder from a newer quarto.
To <q>uninstall</q> a quarto, delete it.

If you don't like it, change it.

<dl>
<dt>Change the options</dt>
<dt>Change the pages</dt>
<dt>Change the styles</dt>
<dt>Change the code</dt>
</dl>


## Give the devs their due.

### code

- [Sam Kennerly](https://samkennerly.github.io/)

### media

- [galaxy.jpg](media/galaxy.jpg) by [NASA and ESA](https://commons.wikimedia.org/wiki/File:Hubble_view_of_barred_spiral_galaxy_Messier_83.jpg)
- [quarto.svg](media/quarto.svg) by [Molly Blair](https://mollyeblair.com/)

### pages

- [Sam Kennerly](https://samkennerly.github.io/)

### styles

- `adrift`, `burning`, `doctoral` by [Sam Kennerly](https://samkennerly.github.io/)
- `celestial` by [Jennifer Blair](https://jennifer-blair.com/)
and [Sam Kennerly](https://samkennerly.github.io/)
