"""Рисует схемы карт CS2 из nav-mesh (awpy-data): проходимые области сверху, цвет — высота.
Запуск: python render.py <каталог вывода>. Нужны awpy и pillow."""
import json
import sys
from pathlib import Path

from awpy import NavMesh, data
from PIL import Image, ImageDraw

MAPS = ['de_mirage', 'de_dust2', 'de_inferno', 'de_nuke', 'de_ancient', 'de_anubis', 'de_overpass', 'de_train', 'de_vertigo', 'de_cache']
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
(OUT / 'maps').mkdir(parents=True, exist_ok=True)
(OUT / 'prev').mkdir(parents=True, exist_ok=True)
S = 2  # суперсэмплинг


def color(z, lo, hi):
    t = 0 if hi == lo else min(max((z - lo) / (hi - lo), 0), 1)
    a = (38, 56, 84)
    b = (190, 204, 224)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


md = data.map_data()
meta = {}
for m in MAPS:
    info = md.get(m)
    try:
        nav = NavMesh(m)
    except Exception as e:  # noqa: BLE001
        print(m, 'нет nav:', e)
        continue
    if not info:
        print(m, 'нет map_data')
        continue
    px, py, sc = info['pos_x'], info['pos_y'], info['scale']
    polys, zs = [], []
    for i in nav.areas['area_id'].to_list():
        a = nav.area(i)
        if not a:
            continue
        pts = [((x - px) / sc, (py - y) / sc) for x, y, _z in a['corners']]
        zc = a['centroid'][2]
        polys.append((pts, zc))
        zs.append(zc)
    zs.sort()
    lo, hi = zs[int(len(zs) * .02)], zs[int(len(zs) * .98)]
    im = Image.new('RGB', (1024 * S, 1024 * S), (14, 18, 26))
    d = ImageDraw.Draw(im)
    for pts, zc in sorted(polys, key=lambda p: p[1]):
        d.polygon([(x * S, y * S) for x, y in pts], fill=color(zc, lo, hi), outline=(10, 14, 20))
    im = im.resize((1024, 1024), Image.LANCZOS)
    im.save(OUT / 'maps' / f'{m}.webp', quality=82, method=6)
    pv = im.copy()
    dd = ImageDraw.Draw(pv)
    for k in range(0, 1025, 128):
        dd.line([(k, 0), (k, 1024)], fill=(255, 80, 80), width=1)
        dd.line([(0, k), (1024, k)], fill=(255, 80, 80), width=1)
        dd.text((k + 3, 3), str(k), fill=(255, 220, 120))
        dd.text((3, k + 3), str(k), fill=(255, 220, 120))
    pv.save(OUT / 'prev' / f'{m}.png')
    meta[m] = {'pos_x': px, 'pos_y': py, 'scale': sc, 'areas': len(polys), 'zlo': round(lo), 'zhi': round(hi)}
    print(m, len(polys), 'областей, высоты', round(lo), round(hi))
json.dump(meta, open(OUT / 'meta.json', 'w'), indent=1)
