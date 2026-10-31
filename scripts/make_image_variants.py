"""Create smaller copies of large photos and add srcset/sizes to <img> tags.

Run from the repo root after adding or replacing photos:
    python3 scripts/make_image_variants.py
It writes name.w480.webp / name.w960.webp next to each large .webp under assets/
and updates every .html page, including /cs/, /de/ and /ru/. Run it after
tools/i18n/build.py. Safe to run repeatedly.
"""
import glob
import os
import re

from PIL import Image

WIDTHS = (480, 960)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

variants = {}
for path in glob.glob("assets/**/*.webp", recursive=True):
    if re.search(r"\.w\d+\.webp$", path):
        continue
    with Image.open(path) as im:
        width, height = im.size
        made = []
        for w in WIDTHS:
            if width <= w * 1.25:
                continue
            out = path[:-5] + f".w{w}.webp"
            if not os.path.exists(out):
                im.resize((w, round(height * w / width)), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)
            made.append(w)
    if made:
        variants["/" + path.replace(os.sep, "/")] = made + [width]

# Rendered width of each image slot, keyed by the class of the element that wraps it.
SIZES = [
    ("cat-image", "(max-width:400px) 50vw, (max-width:760px) 50vw, 300px"),
    ("project-card", "(max-width:760px) 100vw, 400px"),
    ("gallery-item", "(max-width:400px) 100vw, (max-width:760px) 50vw, 400px"),
    ("pj-", "(max-width:760px) 50vw, 400px"),
    ("casino-card", "(max-width:760px) 100vw, 600px"),
    ("about-image", "(max-width:760px) 100vw, 600px"),
]
DEFAULT_SIZES = "(max-width:760px) 100vw, 50vw"


def add_srcset(html):
    def fix(m):
        tag = m.group(0)
        if "srcset=" in tag:
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1) not in variants:
            return tag
        s = src.group(1)
        widths = variants[s]
        srcset = ", ".join([f"{s[:-5]}.w{w}.webp {w}w" for w in widths[:-1]] + [f"{s} {widths[-1]}w"])
        before = html[max(0, m.start() - 400):m.start()]
        cls = re.findall(r'class="([^"]+)"', before)
        context = " ".join(cls[-2:]) if cls else ""
        sizes = next((v for k, v in SIZES if k in context), DEFAULT_SIZES)
        return tag.replace(f'src="{s}"', f'src="{s}" srcset="{srcset}" sizes="{sizes}"', 1)

    return re.sub(r"<img\b[^>]*>", fix, html)


changed = 0
for page in glob.glob("*.html") + glob.glob("products/*.html") + glob.glob("*/*.html") + glob.glob("*/products/*.html"):
    if page.startswith(("node_modules", "tools")):
        continue
    with open(page, encoding="utf-8") as f:
        html = f.read()
    new = add_srcset(html)
    if new != html:
        with open(page, "w", encoding="utf-8") as f:
            f.write(new)
        changed += 1
print(f"{len(variants)} photos have smaller copies; {changed} pages updated")
