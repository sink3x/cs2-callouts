"""Места (callouts) из awpy 1.3.1 nav_info.csv -> позиции на схеме карты CS2 (0..1000) с автоподгонкой.
Запуск: python places.py <nav_places.csv> <meta.json> <каталог>  (maps/ лежит в каталоге; нужны pillow, numpy)."""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

CSV, META, ROOT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
meta = json.load(open(META))

SPECIAL = {
    'BombsiteA': 'A Site', 'BombsiteB': 'B Site', 'CTSpawn': 'CT Spawn', 'TSpawn': 'T Spawn',
    'BackofA': 'Back of A', 'BackofB': 'Back of B', 'TopofMid': 'Top of Mid', 'TunnelsA': 'Tunnels',
    'ARamp': 'A Ramp', 'BDoors': 'B Doors', 'ExtendedA': 'Extended A', 'APlatform': 'A Platform',
    'BPlatform': 'B Platform', 'CTSideUpper': 'CT Side Upper', 'TRamp': 'T Ramp',
}


def human(n):
    if n in SPECIAL:
        return SPECIAL[n]
    s = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', n)
    return re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', s)


by = defaultdict(list)
for r in csv.DictReader(open(CSV)):
    x1, y1, x2, y2 = (float(r[k]) for k in ('x1', 'y1', 'x2', 'y2'))
    by[r['map']].append((r['name'], (x1 + x2) / 2, (y1 + y2) / 2, abs(x2 - x1) * abs(y2 - y1)))


def walk_mask(m):
    a = np.asarray(Image.open(ROOT / 'maps' / f'{m}.webp').convert('RGB')).astype(int)
    return a.sum(axis=2) > 120  # фон (14,18,26) и контуры темнее порога


def fit(pts, mask):
    """Ищем (dx, dy, s) — максимум попаданий центров областей в проходимую геометрию."""
    def score(dx, dy, s):
        x = np.clip(((pts[:, 0] - 512) * s + 512 + dx).round().astype(int), 0, 1023)
        y = np.clip(((pts[:, 1] - 512) * s + 512 + dy).round().astype(int), 0, 1023)
        return mask[y, x].mean()
    base = score(0, 0, 1.0)
    best = (base, 0, 0, 1.0)
    for s in np.arange(0.70, 1.201, 0.02):
        for dx in range(-90, 91, 3):
            for dy in range(-90, 91, 3):
                v = score(dx, dy, s)
                if v > best[0]:
                    best = (v, dx, dy, round(float(s), 2))
    # уточнение
    v0, dx0, dy0, s0 = best
    for dx in range(dx0 - 3, dx0 + 4):
        for dy in range(dy0 - 3, dy0 + 4):
            for s in (s0 - .01, s0, s0 + .01):
                v = score(dx, dy, s)
                if v > best[0]:
                    best = (v, dx, dy, round(float(s), 3))
    return base, best


out, report = {}, {}
for m, rows in by.items():
    mt = meta.get(m)
    if not mt:
        continue
    pts = np.array([[(x - mt['pos_x']) / mt['scale'], (mt['pos_y'] - y) / mt['scale']] for _n, x, y, _a in rows])
    mask = walk_mask(m)
    base, (sc, dx, dy, s) = fit(pts, mask)
    report[m] = {'before': round(float(base), 3), 'after': round(float(sc), 3), 'dx': dx, 'dy': dy, 's': s}

    def tr(px, py):
        return (px - 512) * s + 512 + dx, (py - 512) * s + 512 + dy

    groups = defaultdict(list)
    for (n, x, y, a), (px, py) in zip(rows, pts):
        if n:
            groups[n].append((tr(px, py), a))
    res = []
    for n, ar in groups.items():
        tot = sum(a for _p, a in ar) or 1
        cx = sum(p[0] * a for p, a in ar) / tot
        cy = sum(p[1] * a for p, a in ar) / tot
        # привязка к ближайшей реальной области: метка не попадает в «пустоту» вогнутых мест
        bp = min(ar, key=lambda t: (t[0][0] - cx) ** 2 + (t[0][1] - cy) ** 2)[0]
        if not (8 <= bp[0] <= 1016 and 8 <= bp[1] <= 1016):
            continue
        res.append({'id': n, 'en': human(n), 'x': round(bp[0] / 1.024), 'y': round(bp[1] / 1.024), 'n': len(ar)})
    res.sort(key=lambda p: -p['n'])
    out[m] = res

json.dump(out, open(ROOT / 'places_raw.json', 'w'), ensure_ascii=False, indent=0)
json.dump(report, open(ROOT / 'fit_report.json', 'w'), indent=1)
(ROOT / 'ovl').mkdir(exist_ok=True)
for m, res in out.items():
    pv = Image.open(ROOT / 'maps' / f'{m}.webp').convert('RGB')
    d = ImageDraw.Draw(pv)
    for p in res:
        x, y = p['x'] * 1.024, p['y'] * 1.024
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 90, 60))
        d.text((x + 6, y - 5), p['en'], fill=(255, 235, 150))
    pv.save(ROOT / 'ovl' / f'{m}.png')
    print(m, len(res), 'мест', report[m])
