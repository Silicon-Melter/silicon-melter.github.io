#!/usr/bin/env python3
"""Builds the site: wraps each page body in _src/ with the shared layout (top bar, profile sidebar, footer).

Each _src/<path>.html starts with a small header block, then the page body:
    title: Page title
    description: One sentence for search and link previews
    nav: home | projects | posts | cv
    date: 2026-11            (year-month; sorts the lists, newest first)
    when: Nov 2026           (optional, the date as shown; defaults to the year of `date`)
    card: Short line shown under the title in project/post lists (defaults to description)
    thumb: /assets/img/x.jpg (optional; lists show a text tile with `tag` instead)
    tag: CUDA                (optional, a short word for the tile when there is no thumb)
    code: https://github.com/...   (optional, adds a "Code" link in lists)
    selected: yes            (optional, also list it under "Selected projects" on the home page; works for posts too)
    partof: /projects/x/     (posts only, optional: the project this post is a step of; adds a "Part of" line)
    redirect: /path          (optional; the page only forwards visitors to that address)
    project: yes             (only for pages outside projects/ that should appear in the project list)
    ---
    <main content in HTML>

Lists are generated, so adding a project is one file: drop _src/projects/<name>.html and rebuild.
Projects without a page of their own (datasets, tools) are blocks in _src/_links.txt, same keys plus `url:`.
Placeholders a page body can use:
    {{projects}}  {{projects:selected}}  {{posts}}  {{include:_partials/file.html}}
Files and folders starting with "_" inside _src/ are not built as pages.
_src/index.html -> index.html; _src/posts/foo.html -> posts/foo/index.html.
Run: python3 build.py   (standard library only)
"""
import pathlib, html, re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "_src"
SITE = "Noppawit Tharakittikirati"
NAV = [("home", "/", "About"), ("projects", "/projects/", "Projects"),
       ("posts", "/posts/", "Posts"), ("cv", "/cv/Noppawit_Tharakittikirati_CV.pdf", "CV")]

# Profile sidebar, shown on every page (the left column on wide screens, a compact block on phones).
ICON = {
    "mail": '<path d="M3 5h18v14H3z" fill="none"/><path d="m3 6 9 7 9-7" fill="none"/>',
    "github": '<path d="M9 19c-4 1.5-4-2-6-2.5m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21" fill="none"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="2" fill="none"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7" fill="none"/>',
    "hf": '<circle cx="12" cy="12" r="9" fill="none"/><path d="M8.5 14.5a4 4 0 0 0 7 0M9 10v.01M15 10v.01" fill="none"/>',
    "cv": '<path d="M6 3h8l4 4v14H6z" fill="none"/><path d="M14 3v4h4M9 12h6M9 16h6" fill="none"/>',
    "pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z" fill="none"/><circle cx="12" cy="10" r="2" fill="none"/>',
    "school": '<path d="m2 9 10-5 10 5-10 5z" fill="none"/><path d="M6 11v5c3 2 9 2 12 0v-5" fill="none"/>',
}
def icon(name):
    return (f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

PROFILE_LINKS = [("mail", "mailto:n.tharakittikirati@gmail.com", "Email"),
                 ("github", "https://github.com/Silicon-Melter", "GitHub"),
                 ("linkedin", "https://www.linkedin.com/in/tharakittikirati/", "LinkedIn"),
                 ("hf", "https://huggingface.co/earth37815", "Hugging Face"),
                 ("cv", "/cv/Noppawit_Tharakittikirati_CV.pdf", "CV (PDF)")]

# Drop a square photo at assets/img/profile.jpg and it replaces the initials.
PHOTO = ROOT / "assets/img/profile.jpg"
AVATAR = ('<img class="avatar" src="/assets/img/profile.jpg" alt="Photo of Noppawit Tharakittikirati" width="160" height="160">'
          if PHOTO.exists() else '<div class="avatar initials" aria-hidden="true">NT</div>')

SIDEBAR = f"""<aside class="profile">
{AVATAR}
<div class="who">
<p class="pname"><a href="/">{SITE}</a></p>
<p class="role">Robotics &amp; AI Engineering student</p>
<ul class="facts">
<li>{icon("school")}KMITL, Bangkok</li>
<li>{icon("pin")}Thailand</li>
</ul>
</div>
<ul class="plinks">
{"".join(f'<li><a href="{h}">{icon(i)}<span>{t}</span></a></li>' for i, h, t in PROFILE_LINKS)}
</ul>
</aside>"""

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
<body class="{kind}">
<header class="masthead"><div class="bar">
<a class="name" href="/">{site}</a>
<nav>{nav}</nav>
</div></header>
<div class="layout">
{sidebar}
<main>
{body}
</main>
</div>
<footer><div class="bar">
<span>&copy; 2026 {site}</span>
<span>Plain HTML and CSS, hosted on GitHub Pages</span>
</div></footer>
</body>
</html>
"""

REDIRECT = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}">
</head><body><p><a href="{to}">Continue to {title}</a></p></body></html>
"""

def parse_meta(text):
    meta = {}
    for line in text.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta

def url_for(rel):
    """Turns a path relative to _src (without suffix) into the page's URL."""
    if str(rel) == "index":
        return "/"
    return "/" + str(rel.parent if rel.name == "index" else rel).replace("\\", "/") + "/"

def load_pages():
    pages = []
    for src in sorted(SRC.rglob("*.html")):
        rel = src.relative_to(SRC)
        if any(part.startswith("_") for part in rel.parts):
            continue
        head, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
        meta = parse_meta(head)
        rel = rel.with_suffix("")
        meta.update(_rel=rel, _body=body.strip(), url=meta.get("url") or url_for(rel))
        pages.append(meta)
    return pages

def load_links():
    path = SRC / "_links.txt"
    if not path.exists():
        return []
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))
    return [parse_meta(b) for b in blocks if b.strip() and not b.strip().startswith("#")]

def entry_html(e):
    e_ = lambda k: html.escape(e.get(k, ""), quote=True)
    when = e.get("when") or e.get("date", "")[:4]
    if e.get("thumb"):
        media = f'<img src="{e_("thumb")}" alt="" loading="lazy">'
    else:
        media = f'<span class="tile">{e_("tag") or html.escape(e["title"][:1])}</span>'
    external = not e["url"].startswith("/")
    links = [f'<a href="{e_("url")}">{"Visit" if external else "Read"}</a>']
    if e.get("code"):
        links.append(f'<a href="{e_("code")}">Code</a>')
    return (f'<li class="entry"><a class="thumb" href="{e_("url")}" tabindex="-1" aria-hidden="true">{media}</a>'
            f'<div class="body"><p class="et"><a href="{e_("url")}">{html.escape(e["title"])}</a></p>'
            f'<p class="ed">{html.escape(e.get("card") or e.get("description", ""))}</p>'
            f'<p class="em"><span class="when">{html.escape(when)}</span>{" ".join(links)}</p></div></li>')

def entry_list(items):
    items = sorted(items, key=lambda e: e.get("date", ""), reverse=True)
    return '<ul class="entries">\n' + "\n".join(entry_html(e) for e in items) + "\n</ul>"

def build():
    pages = load_pages()
    links = load_links()
    is_project = lambda p: str(p["_rel"]).startswith("projects/") and p["_rel"].name != "index" or p.get("project") == "yes"
    projects = [p for p in pages if is_project(p)] + links
    posts = [p for p in pages if str(p["_rel"]).startswith("posts/") and p["_rel"].name != "index"]
    lists = {"{{projects}}": entry_list(projects),
             "{{projects:selected}}": entry_list([p for p in projects + posts if p.get("selected") == "yes"]),
             "{{posts}}": entry_list(posts)}

    by_url = {p["url"]: p for p in pages}
    for p in pages:
        body = p["_body"]
        parent = by_url.get(p.get("partof", ""))
        if parent:
            line = f'<p class="partof">Part of <a href="{parent["url"]}">{html.escape(parent["title"])}</a></p>'
            body = body.replace("</h1>", "</h1>\n" + line, 1)
        body = re.sub(r"\{\{include:([^}]+)\}\}",
                      lambda m: (SRC / m.group(1).strip()).read_text(encoding="utf-8").strip(), body)
        for k, v in lists.items():
            body = body.replace(k, v)
        rel = p["_rel"]
        out = ROOT / ("index.html" if str(rel) == "index" else
                      (rel.parent if rel.name == "index" else rel) / "index.html")
        nav = "".join(f'<a href="{h}"{" class=on" if k == p.get("nav") else ""}>{t}</a>' for k, h, t in NAV)
        title = p["title"] if str(rel) == "index" else f'{p["title"]} · {SITE}'
        kind = "article" if rel.name != "index" else "listing"
        out.parent.mkdir(parents=True, exist_ok=True)
        if p.get("redirect"):
            to = html.escape(p["redirect"], quote=True)
            out.write_text(REDIRECT.format(to=to, title=html.escape(title)), encoding="utf-8")
            print("built", out.relative_to(ROOT), "->", p["redirect"])
            continue
        out.write_text(PAGE.format(title=html.escape(title), desc=html.escape(p.get("description", "")),
                                   site=SITE, nav=nav, sidebar=SIDEBAR, kind=kind, body=body),
                       encoding="utf-8")
        print("built", out.relative_to(ROOT))

if __name__ == "__main__":
    build()
