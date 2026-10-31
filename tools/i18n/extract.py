"""Write every translatable English string, in page order, to tools/i18n/source.json."""
import html, json
from build import I18N_HEAD, I18N_NAV, KEEP, PAGES, PREFIXES, ROOT, translate_html

seen = []

class Collector:
    def t(self, s):
        for p in PREFIXES:
            if s.startswith(p):
                self.t(p.strip())
                return self.t(s[len(p):])
        if s and s not in KEEP and s not in seen and any(c.isalpha() for c in s):
            seen.append(s)
        return s
    def text(self, raw):
        self.t(html.unescape(raw).strip()); return raw
    attr = text

for p in PAGES:
    src = I18N_NAV.sub("", I18N_HEAD.sub("", (ROOT / p).read_text()))
    translate_html(src, Collector())
(ROOT / "tools/i18n/source.json").write_text(json.dumps(seen, ensure_ascii=False, indent=0))
print(len(seen), "strings")
