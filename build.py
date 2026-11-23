#!/usr/bin/env python3
"""Builds the site: wraps each page body in _src/ with the shared header and footer.

Each _src/<path>.html starts with a small header block, then the page body:
    title: Page title
    description: One sentence for search and link previews
    nav: home | projects | posts | cv
    ---
    <main content in HTML>
_src/index.html -> index.html; _src/posts/foo.html -> posts/foo/index.html.
Run: python3 build.py   (standard library only)
"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "_src"
SITE = "Noppawit Tharakittikirati"
NAV = [("home", "/", "Home"), ("projects", "/projects/", "Projects"),
       ("posts", "/posts/", "Posts"), ("cv", "/cv/", "CV")]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site"><div class="wrap">
<a class="name" href="/">{site}</a>
<nav>{nav}</nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<a href="https://www.linkedin.com/in/tharakittikirati/">LinkedIn</a> &middot;
<a href="https://github.com/Silicon-Melter">GitHub</a> &middot;
<a href="https://huggingface.co/earth37815">Hugging Face</a> &middot;
<a href="mailto:n.tharakittikirati@gmail.com">Email</a>
</div></footer>
</body>
</html>
"""

def build():
    for src in sorted(SRC.rglob("*.html")):
        head, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
        meta = dict(l.split(":", 1) for l in head.strip().splitlines())
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        rel = src.relative_to(SRC).with_suffix("")
        out = ROOT / ("index.html" if str(rel) == "index" else
                      (rel.parent if rel.name == "index" else rel) / "index.html")
        nav = "".join(f'<a href="{h}"{" class=on" if k == meta.get("nav") else ""}>{t}</a>'
                      for k, h, t in NAV)
        title = meta["title"] if str(rel) == "index" else f'{meta["title"]} · {SITE}'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(PAGE.format(title=html.escape(title), desc=html.escape(meta.get("description", "")),
                                   site=SITE, nav=nav, body=body.strip()), encoding="utf-8")
        print("built", out.relative_to(ROOT))

if __name__ == "__main__":
    build()
