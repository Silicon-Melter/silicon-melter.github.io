# noppawit-earth.github.io

Personal site of Noppawit Tharakittikirati: project pages and write-ups. Plain HTML and CSS, no framework, served by GitHub Pages.

## Edit or add a page
1. Write or edit a file in `_src/` (a small header block, `---`, then the page body in HTML). Examples: `_src/posts/fused-cuda-kernel.html`, `_src/projects/rl-forest-drone.html`.
2. Add a card for it to `_src/posts/index.html` or `_src/projects/index.html` (and `_src/index.html` under "Latest").
3. Run `python3 build.py` (standard library only). It writes `index.html` files next to `_src/`.
4. Preview with `python3 -m http.server` and open http://localhost:8000.
5. Commit everything, including the built pages, and push.

## Publish
Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`. The repo must be public on a free GitHub plan.
