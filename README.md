# noppawit-earth.github.io

Personal site of Noppawit Tharakittikirati: project pages and write-ups. Plain HTML and CSS, no framework, served by GitHub Pages.

## Edit or add a page
Every page shares one layout (top bar, profile sidebar, footer), written in `build.py`. Styles are in `assets/style.css`.

**Posts or projects?** A post is one step of the work (a problem, what you tried, what came out); a project page is the finished picture and links to its posts. A post can name its project with `partof: /projects/<name>/`.

**Add a project:** drop one file, `_src/projects/<name>.html`, then run `python3 build.py`. The file is a small header block, `---`, then the page body in HTML:

```
title: My project
description: One sentence for search and link previews
nav: projects
date: 2026-11            # sorts the lists, newest first
when: 2026               # optional, the date as shown
card: One line shown in the project list
thumb: /assets/img/my-project.jpg   # optional; otherwise a text tile shows `tag`
tag: ROS                 # optional
code: https://github.com/...        # optional
selected: yes            # optional, also show it on the home page
---
<h1>My project</h1>
<p class="meta">2026 &middot; tools used</p>
<p class="lead">What it is, in two sentences.</p>
...
```

The project list, the home page's "Selected projects" and the posts list are generated from these headers, so no card needs to be written by hand. A project without a page of its own (a dataset, a tool) is a block in `_src/_links.txt` with a `url:`. Experience and awards live once in `_src/_partials/` and appear on both the home page and the CV page. To show a photo in the sidebar instead of the initials, add a square `assets/img/profile.jpg` and rebuild.

Preview with `python3 -m http.server` and open http://localhost:8000. Commit everything, including the built pages, and push.

## Publish
Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`. The repo must be public on a free GitHub plan.
