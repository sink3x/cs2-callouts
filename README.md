# cs2-server-admin-callouts

[![CI](https://github.com/sink3x/cs2-server-admin-callouts/actions/workflows/ci.yml/badge.svg)](https://github.com/sink3x/cs2-server-admin-callouts/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sink3x/cs2-server-admin-callouts)](https://github.com/sink3x/cs2-server-admin-callouts/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

English · [Русский](README.ru.md)

**Callout positions for 10 Counter-Strike 2 maps**, with place names in **English, Russian, German and French**. It is the data behind the Callouts page of
**[cs2-server-admin-panel](https://github.com/sink3x/cs2-server-admin-panel)**, published on its own so anybody can reuse it.

| Maps | Dust II, Mirage, Inferno, Nuke, Overpass, Ancient, Anubis, Train, Vertigo, Cache |
|---|---|
| Languages | `en` (the official name), `ru`, `de`, `fr` |
| Main file | `callouts.json` (about 18 KB) |
| Licence | MIT for the data, code and translations (see [Images](#images) for the radars) |

## Two datasets

| | Where | Positions are in the frame of | Images |
|---|---|---|---|
| **Main** (used by the panel) | `callouts.json` | the CS2 **radar** images of the [Boltobserv](https://github.com/boltgolt/boltobserv) project | **not in this repository** (see below) |
| **Schematic** (licence-clean alternative) | `schematic/` | our **own schematic** of the walkable geometry (top-down render of the navigation mesh, colour is height) | `schematic/maps/*.webp`, MIT |

The schematic dataset is fully reproducible from the files in `schematic/data` (a test checks it) and contains no Valve artwork. Use it if you need images you may freely redistribute.

## `callouts.json`

```json
{
  "maps": {
    "de_anubis": {
      "name": "Anubis",
      "fit": 0.795,
      "conf": "mid",
      "box": [14, 5, 981],
      "places": [["Canal", 657, 561, "m", "m", -1]]
    }
  },
  "names": { "Canal": {"ru": "Канал", "de": "Kanal", "fr": "Canal"} }
}
```

A place row is `[name_en, x, y, side, near, level]`:

| Field | Meaning |
|---|---|
| `name_en` | The official English place name from the map's navigation data. Key into `names` for `ru` / `de` / `fr` |
| `x`, `y` | Position in the map image frame scaled to `0..1000` |
| `side` | `t`, `ct` or `m` (middle): which team's half it is closer to |
| `near` | `a`, `b` or `m`: which bombsite it is closer to |
| `level` | Floor: `-1` single level, otherwise `0` low, `1` middle, `2` high (maps with a large height range) |

Per map: `box` is `[x, y, size]`, the square of the `0..1000` frame that holds the playable area (the panel crops the radar to it); `fit` (0..1) says how well the old CS:GO place areas match the CS2 geometry after an automatic shift and scale;
`conf` is `high` (>= 0.85), `mid` (>= 0.75) or `low`.

> **Accuracy.** Place names and areas come from CS:GO navigation data and are fitted to CS2 automatically. On maps that were reworked a lot (Train, Inferno, Cache) the positions are **approximate**, which is what `conf: "low"` / `"mid"` says. Use it as a guide, not a ruler.

## Images

The main dataset is meant to be drawn on top of the radars of **Boltobserv** (`src/maps/<map>/radar.png`, 1536x1536). Those images are Valve's radar overviews as redistributed by Boltobserv under **GPL-3.0** (Ancient and Anubis: MIT, from Lexogrine),
and we do **not** copy them into this repository. [cs2-server-admin-panel](https://github.com/sink3x/cs2-server-admin-panel) bundles resized copies and documents their origin in `app/admin/public/callouts/NOTICE.md`. The underlying artwork belongs to Valve Corporation.

## Use it

```js
const data = await (await fetch('https://raw.githubusercontent.com/sink3x/cs2-server-admin-callouts/main/callouts.json')).json();
const label = (en, lang) => (lang === 'en' ? en : data.names[en][lang]);
```

Or download `cs2-server-admin-callouts-<version>.zip` (both datasets and `SHA256SUMS`) from the [releases](https://github.com/sink3x/cs2-server-admin-callouts/releases).

## Rebuild and test

```bash
python3 -m unittest discover -s tests -v      # standard library only
python3 schematic/scripts/build.py            # schematic/data + names.py -> schematic/callouts.json
```

`render.py` and `places.py` (in `schematic/scripts`) need `awpy`, `numpy` and `Pillow` plus awpy's map data; their docstrings say how to run them. Translations live in `schematic/scripts/names.py`; the main `callouts.json` shares the same `names`.

## Contributing

Corrections of translations and positions are very welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits and licence

[MIT](LICENSE) for code, data and translations. Place names and the original navigation data come from [awpy](https://github.com/pnxenopoulos/awpy) (MIT), which extracts them from Valve's games; radar frames and map metadata from [Boltobserv](https://github.com/boltgolt/boltobserv).
Counter-Strike and its map and place names belong to Valve Corporation; this project is not affiliated with Valve. If you are a rights holder and want something changed, open an issue.
