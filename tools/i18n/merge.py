"""Merge work/<lang>_*.txt ("N:: text" lines, N = index in source.json) into <lang>.json keyed by English."""
import glob, json, re, sys
from pathlib import Path

lang = sys.argv[1]
here = Path(__file__).parent
src = json.loads((here / "source.json").read_text())
table = json.loads((here / f"{lang}.json").read_text()) if (here / f"{lang}.json").exists() else {}
seen = set()
for f in sorted(glob.glob(str(here / f"work/{lang}_*.txt"))):
    for line in Path(f).read_text().splitlines():
        if not line.strip():
            continue
        m = re.match(r"(\d+):: ?(.*)$", line)
        if not m:
            sys.exit(f"bad line in {f}: {line}")
        i, text = int(m.group(1)), m.group(2).strip()
        if i in seen:
            sys.exit(f"duplicate index {i}")
        seen.add(i)
        table[src[i]] = text
missing = [i for i in range(len(src)) if i not in seen and src[i] not in table]
print(f"{lang}: {len(seen)} lines merged, {len(missing)} missing", missing[:20])
(here / f"{lang}.json").write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n")
