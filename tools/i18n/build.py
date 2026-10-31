"""Build the translated versions of castechled.com.

English HTML in the repository root is the source of truth. For every language in LANGS this script
writes /<lang>/... copies with translated text, localised links, <html lang>, canonical and og:url.
It also (re)writes the hreflang block and the language menu in the English pages, and regenerates
sitemap.xml with every language.

Usage:  python3 tools/i18n/build.py          (fails and lists strings that have no translation)
        python3 tools/i18n/extract.py        (refresh source.json after editing English pages)

Translations live in tools/i18n/<lang>.json as {"English text": "translation"}.
"""
import html, json, re, sys
from pathlib import Path

from common import ATTRS, LANG_NAMES, LANGS, ROOT, pages

SITE = "https://castechled.com"
PAGES = pages()
PAGE_SET = set(PAGES)
# Only languages that already have a translation file are built and linked.
ACTIVE = [l for l in LANGS if (ROOT / f"tools/i18n/{l}.json").exists()]

# Strings that stay the same in every language (brand, addresses, e-mail, IDs).
KEEP = {
    "CASTECH", "LED", "CASTECHLED", "info@castechled.com", "info@castechled.com ↗", "Cihlářská 782/10a, Prosek",
    "190 00 Praha 9", "ID 445613480", "Virexa AI Technologies", "Khakhuli Street No. 3", "name@company.com",
}
PREFIXES = ("View larger photograph: ", "View full photograph: ", "Show slide ")

I18N_HEAD = re.compile(r"<!--i18n-head-->.*?<!--/i18n-head-->", re.S)
I18N_NAV = re.compile(r"<!--i18n-nav-->.*?<!--/i18n-nav-->", re.S)
TOKEN = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
ATTR_RE = re.compile(r'(\s(?:%s)=")([^"]*)(")' % "|".join(re.escape(a) for a in ATTRS))
META_RE = re.compile(r'(<meta\s+(?:name="description"|property="og:(?:title|description)")\s+content=")([^"]*)(")')


def url_path(page):
    return "/" if page == "index.html" else "/" + page


def lang_path(lang, page):
    p = url_path(page)
    return p if lang == "en" else f"/{lang}{p}"


def head_block(page):
    links = [f'<link rel="alternate" hreflang="{l}" href="{SITE}{lang_path(l, page)}">' for l in ["en", *ACTIVE]]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{url_path(page)}">')
    return "<!--i18n-head-->" + "".join(links) + "<!--/i18n-head-->"


def nav_block(lang, page):
    active = ' class="active-lang"'
    items = "".join(
        f'<a href="{lang_path(l, page)}" hreflang="{l}" lang="{l}"{active if l == lang else ""}>{LANG_NAMES[l]}</a>'
        for l in ["en", *ACTIVE]
    )
    return (
        '<!--i18n-nav--><details class="lang-menu"><summary aria-label="Language / Jazyk / Sprache / Язык">'
        f'{lang.upper()} <span class="down-chevron">⌄</span></summary><div class="dropdown lang-drop">{items}</div></details><!--/i18n-nav-->'
    )


def add_i18n_blocks(src, lang, page):
    src = I18N_HEAD.sub("", src)
    src = I18N_NAV.sub("", src)
    src = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + head_block(page), src, count=1)
    # language menu goes at the end of the main navigation
    src = re.sub(r'(<nav id="site-nav"[^>]*>.*?)(</nav>)', lambda m: m.group(1) + nav_block(lang, page) + m.group(2), src, count=1, flags=re.S)
    return src


class Translator:
    def __init__(self, lang):
        self.lang = lang
        self.table = json.loads((ROOT / f"tools/i18n/{lang}.json").read_text())
        self.missing = []

    def t(self, s):
        if s in KEEP or not any(c.isalpha() for c in s):
            return s
        if s in self.table:
            return self.table[s]
        for p in PREFIXES:
            if s.startswith(p):
                return self.t(p.strip()) + " " + self.t(s[len(p):])
        if s not in self.missing:
            self.missing.append(s)
        return s

    def text(self, raw):
        return html.escape(self.t(html.unescape(raw).strip()), quote=False)

    def attr(self, raw):
        return html.escape(self.t(html.unescape(raw).strip()), quote=True)


def translate_html(src, tr):
    out, skip, in_title = [], 0, False
    for part in TOKEN.split(src):
        if not part:
            continue
        if part.startswith("<"):
            low = part.lower()
            m = re.match(r"</?\s*([a-z0-9]+)", low)
            tag = m.group(1) if m else ""
            closing = low.startswith("</")
            if tag in ("script", "style", "svg"):
                skip += -1 if closing else (0 if part.endswith("/>") else 1)
            if tag == "title":
                in_title = not closing
            if not closing and not part.startswith("<!--"):
                part = ATTR_RE.sub(lambda a: a.group(1) + tr.attr(a.group(2)) + a.group(3), part)
                part = META_RE.sub(lambda a: a.group(1) + tr.attr(a.group(2)) + a.group(3), part)
            out.append(part)
        elif skip or not part.strip():
            out.append(part)
        else:
            lead = part[: len(part) - len(part.lstrip())]
            trail = part[len(part.rstrip()):]
            out.append(lead + (tr.attr(part) if in_title else tr.text(part)) + trail)
    return "".join(out)


def localise_links(src, lang, page):
    def fix(m):
        attr, url = m.group(1), m.group(2)
        path = url.split("#")[0].split("?")[0]
        rest = url[len(path):]
        if path == "/":
            return f'{attr}="/{lang}/{rest}"'
        if path.startswith("/") and path[1:] in PAGE_SET:
            return f'{attr}="/{lang}{path}{rest}"'
        if lang == "ru" and url.startswith("https://castecheq.com/") and "/ru/" not in url:
            return f'{attr}="https://castecheq.com/ru/{url[len("https://castecheq.com/"):]}"'
        return m.group(0)

    src = re.sub(r'(href)="([^"]*)"', fix, src)
    src = src.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    own = SITE + url_path(page)
    src = src.replace(f'<link rel="canonical" href="{own}">', f'<link rel="canonical" href="{SITE}{lang_path(lang, page)}">')
    src = src.replace(f'<meta property="og:url" content="{own}">', f'<meta property="og:url" content="{SITE}{lang_path(lang, page)}">')
    return src


def sitemap():
    rows = []
    for page in PAGES:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{lang_path(l, page)}"/>' for l in ["en", *ACTIVE])
        for l in ["en", *ACTIVE]:
            rows.append(f"<url><loc>{SITE}{lang_path(l, page)}</loc>{alts}</url>")
    for extra in ("privacy.html", "terms.html"):
        rows.append(f"<url><loc>{SITE}/{extra}</loc></url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(rows) + "</urlset>\n"
    )


def main():
    problems = {}
    for page in PAGES:
        path = ROOT / page
        en = add_i18n_blocks(path.read_text(), "en", page)
        path.write_text(en)
    for lang in ACTIVE:
        tr = Translator(lang)
        for page in PAGES:
            src = I18N_NAV.sub("", I18N_HEAD.sub("", (ROOT / page).read_text()))
            out = add_i18n_blocks(localise_links(translate_html(src, tr), lang, page), lang, page)
            dest = ROOT / lang / page
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(out)
        if tr.missing:
            problems[lang] = tr.missing
    (ROOT / "sitemap.xml").write_text(sitemap())
    if problems:
        for lang, miss in problems.items():
            print(f"[{lang}] {len(miss)} untranslated strings:")
            for s in miss[:40]:
                print("   ", s)
        sys.exit(1)
    print("built", len(PAGES), "pages x", len(ACTIVE), "languages:", ", ".join(ACTIVE))


if __name__ == "__main__":
    main()
