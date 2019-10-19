# Much Ado About Quartos

## Self-promotion is not so vile a sin.

### Quartos are small
- fewer than 500 lines of code
- no busy loops
- no Ten-Ton Widgets https://css-tricks.com/ten-ton-widgets/
- No server. Static websites do not need servers.

### Quartos are clean

`Quire` class

- A quarto never reads or writes outside its folder unless you insist.
- no side effects
- no caches
- minimal state

### Quartos are lazy
- Apply style only when you call `quire/apply`, not every time you fix a typo.
- Clean pages only when you call `quire/clean`, not every time you fix a typo.
- Delete pages only when you call `quire/delete`, not every time you fix a typo.
- Don't copy images, audio, video, or other large files. Don't even look at them.

### Quartos are independent

[dependency hell](https://en.wikipedia.org/wiki/Dependency_hell)

- Packages in Quarto's
[requirements.txt](https://github.com/samkennerly/quarto/blob/master/requirements.txt)
file are **not required**. The file is used to build Quarto's [dev sandbox](https://en.wikipedia.org/wiki/Deployment_environment#Development).
- Multiple quartos can exist on the same computer without conflicts.
- The stock quarto does not require any packages, plugins, templates, frameworks, templates, configuration files, custom exceptions, custom loggers, custom file formats, shims, stylesheets, `.bash_profile` edits, ENV variables, `__init__.py`, `__main__.py`, `setup.py`, `sys.path` hacks, virtualenvs, wrappers, bundlers, `pip` installs, `npm` installs, `gem` installs, or any other dependencies except Python 3.


## We will draw the curtain and show you the HTML.

See the real HTML for any web page:

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
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;
Quarto builds websites.
&lt;/title&gt;
&lt;link rel="canonical" href="https://quarto.neocities.org/index.html"&gt;
...
```

## Is this a PR I see before me?

[pull request](https://github.com/samkennerly/quarto/pulls)

### True it is that we have seen better styles.
-  Most of the stock styles were made by a design
[rookie](https://samkennerly.github.io/).
Surely you can do better!
-  Create a new folder in the `style` folder and an
[example](examples/adrift.html)
to show off your style.
-  Styles can include non-CSS files, but `quire/apply` will ignore them.
-  CSS files need not be named `align.css`, `border.css`, etc.

### Neither a rebaser nor a merger be.

- [merge](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [rebase](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [entropy](https://en.wikipedia.org/wiki/Software_entropy)
- [feature creep](https://en.wikipedia.org/wiki/Feature_creep)
- [fork](https://help.github.com/en/articles/fork-a-repo)

### Files of few bytes are the best files.
- Large files in GitHub repos can cause
[problems](https://help.github.com/en/articles/working-with-large-files).
- Try to avoid uploading any file larger than a
[galaxy](media/galaxy.jpg).
- Text files (HTML, CSS, MD, etc.) are rarely too big, but...
- Code that resembles
[pasta](https://en.wikipedia.org/wiki/Spaghetti_code)
should probably be
[refactored](https://en.wikipedia.org/wiki/Code_refactoring).

### No legacy is so rich as honesty.
- If you use someone else's work, then
[make it obvious]( https://en.wikipedia.org/wiki/Attribution_%28copyright%29).
- Copypasting from Quarto is OK **if you respect the licenses**.
- The license for Quarto code is in the
[LICENSE](https://github.com/samkennerly/quarto/blob/master/LICENSE)
file.
- The license for this website is [on this page](#klf).


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
