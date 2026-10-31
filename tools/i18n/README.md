# Translations for castechled.com

English pages in the repository root are the source. Translated copies in `/cs/`, `/de/` and `/ru/` are generated — do not edit them by hand.

After changing English text:

1. `python3 tools/i18n/extract.py` — refreshes `source.json` with every English string.
2. Add the new or changed strings to `cs.json`, `de.json`, `ru.json` (`"English": "translation"`).
3. `python3 tools/i18n/build.py` — regenerates every language, the hreflang links, the language menu and `sitemap.xml`. It stops and lists any string that still has no translation.

Strings that are the same in every language (brand, addresses, e-mail) are listed in `KEEP` in `build.py`.
