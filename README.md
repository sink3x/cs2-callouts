# cs2-callouts

Схематичные карты (10 карт CS2) и места-callouts для панели [cs2-yc-sandbox](https://github.com/sink3x/cs2-yc-sandbox).

- `maps/*.webp` — **собственная схема** проходимой геометрии (nav-mesh из awpy 3.x, цвет — высота). Это не радар Valve и не его картинка.
- `callouts.json` — места: официальные названия из навигации карты (en) → ru/de/fr, позиция на схеме (0–1000), сторона, ближайшая точка, этаж.
- `data/nav_places.csv` — названия мест и координаты областей из [awpy](https://github.com/pnxenopoulos/awpy) 1.3.1 (MIT, имена мест Valve из навигационных сеток CS:GO). Координаты CS:GO подгоняются к геометрии CS2 (сдвиг/масштаб, `data/fit_report.json`), поэтому у переработанных карт (Train, Inferno, …) положение меток **примерное** — это отражено в `conf` каждой карты.

Пересборка: `scripts/render.py` (схемы), `scripts/places.py` (позиции + подгонка), `scripts/build.py` (итоговый JSON).
