# Contributing

Fixes are welcome: a wrong or awkward translation, a misplaced callout, a new language, a new map.

- **Translations**: edit `schematic/scripts/names.py` (English name -> ru, de, fr) **and** the `names` object of `callouts.json`, run `python3 schematic/scripts/build.py`, then `python3 -m unittest discover -s tests`. A test checks that both datasets share the same names and that `schematic/callouts.json` matches its build.
- **Positions**: the main dataset's positions are in `callouts.json`; the schematic ones come from `schematic/data/places_raw.json` (fitted by `schematic/scripts/places.py`). Open an issue with the map, the place and where it should be (a screenshot of the schematic helps).
- **New map**: needs the awpy navigation data; see the docstrings of `schematic/scripts/render.py` and `places.py`.
- Do not add Valve radar images or other game artwork to this repository; the `schematic/` images are drawn from walkable-area geometry only.

By contributing you agree that your contribution is released under the [MIT license](LICENSE).
