# Options files

Quartos use <dfn>options files</dfn> to answer questions like:

- Who wrote this page?
- Where is the [favicon]()?
- Which icons should be in the `#icons` section?
- Do you want to reveal your email to the entire internet?

Options files must be valid [JSON]() files.

---

## What's in a name?

If the path to a page is:
```
ready/examples/doctoral.html
```
then that page's options file must be:
```
ready/examples/doctoral.json
```
if the file exists. Options files are optional.

---

## Sites are merriest when they have a home.

- Every site <mark>must</mark> have a home page.
- The home page path must be `ready/index.html` or...
- `ready/index.md` or any other suffix except `.json`.
- Home options (if any) must be in `ready/index.json`.

---

## Each defaults toward its home.

- Each page in the `ready` folder *may* have an options file.
- Omitting the home options file is allowed but not recommended.
- Home options are used as default values for any missing page options.
- If a page has no options file, then all its values will be default values.

---

## Complete Options of Quarto

<dl>
<dt>base</dt>
<dd>The
<a href="">canonical URL</a>
for your site with the
<a href="">path component</a> removed.
<dd><code>"https://quarto.neocities.org/"</code>


<dt>copyright</dt>
<dd>Copyright statement, if any.
<dd><code>"© Sam Kennerly 2019."</code>

<dt>email</dt>
<dd>Email address to display, if any.
<dd><code>"samkennerly@gmail.com"</code>

<dt>favicon</dt>
<dd>Icon file. Can be absolute URL or path from home page.
<dd><code>"favicon.ico"</code>

<dt>homelink</dt>
<dd>Label for link to home page in &lt;nav&gt; menu.
<dd><code>"Quarto"</code>

<dt>icons</dt>
<dd>List of [alt text, image source, link URL] for <code>#icons</code> section.
<dd>Image source can be absolute URL or path from home page.
<dd><pre><code>[
  [ "GitHub", "media/icons/github.svg", "https://github.com/samkennerly" ],
  [ "Twitter", "media/icons/twitter.png", "https://twitter.com/data_lore/" ]
]
</code></pre>

<dt>javascripts</dt>
<dd>List of script sources, if any.
<dd>Sources can be absolute URLs and/or paths from home page.
<dd><pre><code>[
  "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
  "src/javascript/annoyEveryoneWith-IntrusiveDialogBoxes.js"
]
</code></pre>

<dt>license</dt>
<dd>Source and text of license, if any.
<dd>Source can be absolute URL or path from home page.
<dd><pre><code>[
  "https://creativecommons.org/licenses/by/4.0",
  "Licensed under a CC BY 4.0 license."
]
</code></pre>

<dt>meta</dt>
<dd>{ name: content } mapping for &lt;meta&gt; tags, if any.
<dd><pre><code>{
  "author": "Wm. Shakespeare",
  "description": "In Scotland, no one can hear you scream."
}
</code></pre>

<dt>nextlink</dt>
<dd>Label for link to next page, if any.
<dd><code>"fwd ⇢"</code>

<dt>prevlink</dt>
<dd>Label for link to previous page, if any.
<dd><code>"⇠ rev"</code>

<dt>qlink</dt>
<dd>Label for link to quarto repository, if any.
<dd><code>"Built by a Quarto."</code>

<dt>styles</dt>
<dd>Sources of stylesheet(s) for this page.
<dd>Sources can be absolute URLs and/or paths from home page.
<dd><pre><code>[
  "https://www.w3schools.com/html/styles.css",
  "style.css"
]
</code></pre>

<dt>title</dt>
<dd>Page &lt;title&gt; element.
<dd><code>"Macbeth II: Toil and Trouble"</code>

</dl>
