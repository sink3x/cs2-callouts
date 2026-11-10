import csv, json, math
from collections import defaultdict
from pathlib import Path
from names import NAMES, MAP_NAMES
ROOT = Path(__file__).resolve().parent.parent  # the repository root; run from anywhere
DATA = ROOT / 'data'
raw = json.load(open(DATA / 'places_raw.json')); fit = json.load(open(DATA / 'fit_report.json'))
meta = {}
# z по местам (площадь-взвешенно) из исходной nav-информации
zs = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open(DATA / 'nav_places.csv')):
    if not r['name']: continue
    z = (float(r['z1']) + float(r['z2'])) / 2; a = abs(float(r['x2']) - float(r['x1'])) * abs(float(r['y2']) - float(r['y1']))
    zs[r['map']][r['name']].append((z, a))
def fix(en): return {'Tunnel1': 'Tunnel 1', 'Tunnel2': 'Tunnel 2'}.get(en.replace(' ', '') if en.startswith('Tunnel') and en[-1] in '12' else en, en)
out = {'maps': {}, 'names': {}}
missing = set()
for m, pl in raw.items():
    for p in pl:
        if p['en'] in ('Tunnel1', 'Tunnel2'): p['en'] = p['en'][:-1] + ' ' + p['en'][-1]
    by = {p['en']: p for p in pl}
    t = by.get('T Spawn'); ct = by.get('CT Spawn'); a = by.get('A Site'); b = by.get('B Site')
    if not ct and a and b: ct = {'x': (a['x'] + b['x']) / 2, 'y': (a['y'] + b['y']) / 2}
    d = lambda p, q: math.hypot(p['x'] - q['x'], p['y'] - q['y'])
    zlist = {}
    for p in pl:
        arr = zs[m].get(p['id'], []); tot = sum(w for _, w in arr) or 1
        zlist[p['en']] = sum(z * w for z, w in arr) / tot
    allz = sorted(zlist.values()); lo, hi = allz[0], allz[-1]
    multi = (hi - lo) >= 300
    rows = []
    for p in pl:
        if p['en'] not in NAMES: missing.add(p['en'])
        side = 'm'
        if t and ct:
            f = d(p, t) / max(1, d(p, t) + d(p, ct))
            side = 't' if f < 0.36 else ('ct' if f > 0.64 else 'm')
        near = 'm'
        if a and b:
            da, db = d(p, a), d(p, b)
            near = 'a' if da < db * 0.75 else ('b' if db < da * 0.75 else 'm')
        lvl = 1
        if multi:
            f = (zlist[p['en']] - lo) / (hi - lo); lvl = 0 if f < 0.33 else (2 if f > 0.66 else 1)
        rows.append([p['en'], p['x'], p['y'], side, near, lvl if multi else -1])
    q = fit[m]['after']
    out['maps'][m] = {'name': MAP_NAMES[m], 'fit': q, 'conf': 'high' if q >= .85 else ('mid' if q >= .75 else 'low'), 'places': rows}
for en, (ru, de, fr) in NAMES.items(): out['names'][en] = {'ru': ru, 'de': de, 'fr': fr}
print('без перевода:', sorted(missing)); print({m: (v['conf'], len(v['places'])) for m, v in out['maps'].items()})
json.dump(out, open(ROOT / 'callouts.json', 'w'), ensure_ascii=False, separators=(',', ':'))
import os; print(os.path.getsize(ROOT / 'callouts.json'), 'bytes')
