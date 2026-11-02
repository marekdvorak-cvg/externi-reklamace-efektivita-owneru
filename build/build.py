"""Sestaví index.html z build/data.json (výsledky SOQL dotazů) a šablon.

Použití:  python3 build/build.py
data.json obsahuje pro každý dataset seznam řádků přesně jako vrací SOQL
(bez pole "attributes"). Dotazy jsou popsané v build/QUERIES.md.
"""
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OWNERS = ["Pavel Tran Son", "Marco Antonio Sinica", "Kryštof Veber"]
NEEDED = ["opened_daily", "closed_daily", "closed_stats", "closed_30", "backlog", "backlog_30",
          "done_open", "cost_source", "extension", "resolution", "cpc_types"]

data = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
missing = [k for k in NEEDED if k not in data]
assert not missing, f"Chybí datasety: {missing}"
for rows in data.values():
    for r in rows:
        r.pop("attributes", None)

# Kontrola konzistence: uzavřené po dnech i podle zdroje musí sedět s celkovým počtem.
for o in OWNERS:
    total = sum(r["cnt"] for r in data["closed_stats"] if r["owner"] == o)
    by_day = sum(r["cnt"] for r in data["closed_daily"] if r["owner"] == o)
    by_src = sum(r["cnt"] for r in data["cost_source"] if r["owner"] == o)
    by_ext = sum(r["cnt"] for r in data["extension"] if r["owner"] == o)
    assert total == by_day == by_src == by_ext, f"Nesedí počty pro {o}: {total}, {by_day}, {by_src}, {by_ext}"

now = datetime.now(ZoneInfo("Europe/Prague"))
stamp = f"{now.day}. {now.month}. {now.year}, {now:%H:%M}"
dstamp = f"{now.day}. {now.month}. {now.year}"

page = open(os.path.join(HERE, "page.html"), encoding="utf-8").read()
page = page.replace('<meta name="dash-one-writer">\n', "")
swaps = [
    ('Externí reklamace · 1. 9. 2026 – <span data-draw="today">—</span> · živá data ze Salesforce',
     f"Externí reklamace · 1. 9. 2026 – {dstamp} · data ze Salesforce, stav k {stamp}"),
    ('<button type="button" class="lx-refresh">↻ Obnovit data</button>',
     f'<span class="lx-stamp">Stav k {stamp}</span>'),
]
for a, b in swaps:
    assert page.count(a) == 1, a
    page = page.replace(a, b)

shell = open(os.path.join(HERE, "shell.html"), encoding="utf-8").read()
out = (shell.replace("__DATA__", json.dumps(data, ensure_ascii=False))
            .replace("__STAMP__", stamp)
            .replace("__PAGE__", page))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html sestaven, stav k", stamp)
