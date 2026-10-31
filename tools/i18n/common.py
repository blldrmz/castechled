"""Shared helpers for the castechled.com translation build."""
import glob, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGS = ["cs", "de", "ru"]
LANG_NAMES = {"en": "English", "cs": "Čeština", "de": "Deutsch", "ru": "Русский"}
SKIP_PAGES = {"privacy.html", "terms.html"}
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-caption")

def pages():
    files = sorted(glob.glob(str(ROOT / "*.html")) + glob.glob(str(ROOT / "products" / "*.html")))
    rel = [str(Path(f).relative_to(ROOT)) for f in files]
    rel = [r for r in rel if r not in SKIP_PAGES]
    # index first so the shared header/footer strings come first
    rel.sort(key=lambda r: (r != "index.html", r))
    return rel

TOKEN = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
ATTR_RE = re.compile(r'(\s(%s)=")([^"]*)(")' % "|".join(re.escape(a) for a in ATTRS))
META_RE = re.compile(r'(<meta\s+(?:name="description"|property="og:(?:title|description)")\s+content=")([^"]*)(")')
TITLE_RE = re.compile(r"(<title>)([^<]*)(</title>)")

def walk(src, on_text, on_attr):
    """Tokenise HTML; call on_text(raw_text) for visible text and on_attr(raw_value) for translatable
    attributes. Each callback returns replacement raw text. Returns rebuilt HTML."""
    out, skip = [], 0
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
            if not closing and not part.startswith("<!--"):
                part = ATTR_RE.sub(lambda a: a.group(1) + on_attr(a.group(3)) + a.group(4), part)
                part = META_RE.sub(lambda a: a.group(1) + on_attr(a.group(2)) + a.group(3), part)
            out.append(part)
        else:
            if skip or not part.strip() or out and out[-1].lower().startswith("<title"):
                out.append(part if not (out and out[-1].lower().startswith("<title")) else on_attr(part))
                continue
            lead = part[: len(part) - len(part.lstrip())]
            trail = part[len(part.rstrip()):]
            out.append(lead + on_text(part.strip()) + trail)
    return "".join(out)

def unesc(s):
    return html.unescape(s)
