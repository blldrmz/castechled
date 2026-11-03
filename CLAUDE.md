# CLAUDE.md — castechled.com (CasTech LED)

LED screen website for **CasTechLED by Virexa**. Owner: Bilal Durmaz. He talks to you in Turkish or English. The site is in English, with Czech, German and Russian versions.

## Working rules

- Follow the karpathy-guidelines skill: state assumptions, minimum code, surgical changes, verify before saying "done".
- Never change copy, logo, images or prices on your own initiative. Do only what was asked; mention other issues instead of fixing them.
- `main` is published as-is to castechled.com (GitHub Pages, no build step). Anything pushed to `main` is live. For anything bigger than a text fix, work on a branch and open a PR.
- Commit messages: short, English, imperative.

## Stack

- **Plain static HTML + one `styles.css` + one `script.js`.** No framework, no bundler, no npm. Do not introduce one.
- Every page carries its own copy of the header, nav, footer and JSON-LD. A change to shared parts must be made in **every English page** (`*.html` and `products/*.html`), then the translations rebuilt (see below).
- `CNAME` (castechled.com), `.nojekyll`, `.well-known/security.txt`, `robots.txt`: do not touch.
- Font: **Inter**, self-hosted in `assets/fonts/` (same as virexa-tech.com). No other fonts, no Google Fonts link.
- Forms (`quote.html`, `contact.html`) post to FormSubmit → `sales@virexa-tech.com`. Never change the recipient. Public contact email is `info@castechled.com`. **Never use castecheq.com addresses on this site.**

Preview locally: `python3 -m http.server` in the repo root (links are root-absolute, so open via the server, not as files).

## Translations (`/cs/`, `/de/`, `/ru/`)

English pages in the root are the source. **The `/cs/`, `/de/` and `/ru/` folders are generated. Never edit them by hand.**

After changing English text:
1. `python3 tools/i18n/extract.py` refreshes `tools/i18n/source.json`.
2. Add the new or changed strings to `cs.json`, `de.json` and `ru.json` (`"English": "translation"`).
3. `python3 tools/i18n/build.py` regenerates all languages, the hreflang tags, the language menu and `sitemap.xml`. It fails and lists any missing translation. Fix those; don't skip them.

Strings that stay the same in every language (brand, addresses, emails, IDs) go in `KEEP` in `build.py`. `privacy.html` and `terms.html` are English-only (`SKIP_PAGES` in `common.py`). Do not commit `__pycache__` changes.

## Images

- Photos are `.webp` under `assets/`, `assets/img/` and `assets/projects/`.
- After adding or replacing photos, run `python3 scripts/make_image_variants.py` **after** `build.py`. It makes the `.w480`/`.w960` copies and writes `srcset` into every page, including translations. Requires Pillow.
- `<span class="image-supplier-mask">CASTECHLED</span>` overlays on some product photos are intentional. Do not remove them.
- Outdoor LED and installation photos (including install crews) may be used uncropped. People may be cropped out of casino-floor photos.
- Logo: `assets/castech-mark.svg` / `assets/favicon.svg`: gold "C" with a single row of LED bulbs in its band, closed ends, plain gold "T" inside, on navy. Do not swap it for the CasTech EQ roulette/card-suit mark.

## Business facts the copy must respect

- Main SEO keywords: **"casino LED screen"** and **"LED video wall"**.
- The site must say: **indoor and outdoor** LED screens; a range of **pixel pitches** (fine pitch for close viewing, larger pitch for long distance); **viewing distance** decides the right pitch; screens are **fully customizable** (size, shape, brightness, mounting).
- Say "LED screen", not "LED display", in new copy.
- Jackpot screens are sold on castecheq.com. Link to `https://castecheq.com/jackpot-screens/` rather than building a jackpot section here.
- Real past projects include: a 4-sided P2.5 jackpot screen (Bet25), a 2-sided P2.5 indoor jackpot screen (Otium Casino), a P5 outdoor facade screen (billiard club) and a curved P3 outdoor building facade. Use the existing case studies on `projects.html` too. Never invent projects, clients or specs.

## Company details (footer, legal, about)

- CasTechLED is a brand of Virexa AI Technologies s.r.o., IČO 29716055, Cihlářská 782/10a, Prosek, 190 00 Praha 9. Commercial Register, Municipal Court in Prague, section C, file 451241.
- Sister company: Deniz Trade LLC, Batumi, ID 445613480, Khakhuli Str. No. 3.
- Phones: Prague +420 704 481 975, Batumi +995 555 48 19 75. Do not change them.
