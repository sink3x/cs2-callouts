"""Schema and consistency checks for callouts.json, maps/ and data/. Standard library only: python3 -m unittest"""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMATIC = ROOT / "schematic"
DATA = json.loads((ROOT / "callouts.json").read_text(encoding="utf-8"))
SCHEMATIC_DATA = json.loads((SCHEMATIC / "callouts.json").read_text(encoding="utf-8"))
CYRILLIC = re.compile("[Ѐ-ӿ]")
EXPECTED_MAPS = {"de_ancient", "de_anubis", "de_cache", "de_dust2", "de_inferno", "de_mirage", "de_nuke", "de_overpass", "de_train", "de_vertigo"}


class Schema(unittest.TestCase):
    def test_top_level(self):
        self.assertEqual(set(DATA), {"maps", "names"})

    def test_expected_maps(self):
        self.assertEqual(set(DATA["maps"]), EXPECTED_MAPS)

    def test_map_entries(self):
        for mid, m in DATA["maps"].items():
            with self.subTest(map=mid):
                self.assertEqual(set(m), {"name", "fit", "conf", "box", "places"})
                bx, by, bs = m["box"]
                self.assertTrue(bx >= 0 and by >= 0 and bs > 300 and bx + bs <= 1000 and by + bs <= 1000, "crop box must fit the 0..1000 frame")
                self.assertTrue(m["name"])
                self.assertIsInstance(m["fit"], (int, float))
                self.assertTrue(0 <= m["fit"] <= 1)
                self.assertIn(m["conf"], {"high", "mid", "low"})
                self.assertGreater(len(m["places"]), 10)

    def test_confidence_matches_fit(self):
        for mid, m in DATA["maps"].items():
            expected = "high" if m["fit"] >= 0.85 else ("mid" if m["fit"] >= 0.75 else "low")
            with self.subTest(map=mid):
                self.assertEqual(m["conf"], expected)

    def test_place_rows(self):
        for mid, m in DATA["maps"].items():
            seen = set()
            for row in m["places"]:
                with self.subTest(map=mid, place=row[0] if row else None):
                    self.assertEqual(len(row), 6)
                    name, x, y, side, near, level = row
                    self.assertIsInstance(name, str)
                    self.assertTrue(name.strip())
                    self.assertTrue(0 <= x <= 1000 and 0 <= y <= 1000, "position must be on the 0..1000 schema")
                    self.assertIn(side, {"t", "ct", "m"})
                    self.assertIn(near, {"a", "b", "m"})
                    self.assertIn(level, {-1, 0, 1, 2})
                    self.assertNotIn(name, seen, "duplicate place on one map")
                    seen.add(name)


class Translations(unittest.TestCase):
    def test_every_place_has_ru_de_fr(self):
        names = DATA["names"]
        for mid, m in DATA["maps"].items():
            for row in m["places"]:
                with self.subTest(map=mid, place=row[0]):
                    self.assertIn(row[0], names)
                    self.assertEqual(set(names[row[0]]), {"ru", "de", "fr"})
                    for lang, text in names[row[0]].items():
                        self.assertTrue(text.strip(), lang)

    def test_scripts(self):
        for en, tr in DATA["names"].items():
            with self.subTest(place=en):
                self.assertIsNone(CYRILLIC.search(en), "the source name is English")
                self.assertIsNotNone(CYRILLIC.search(tr["ru"]), "ru must be Cyrillic")
                self.assertIsNone(CYRILLIC.search(tr["de"]))
                self.assertIsNone(CYRILLIC.search(tr["fr"]))

    def test_no_orphan_translations(self):
        used = {row[0] for m in DATA["maps"].values() for row in m["places"]}
        self.assertEqual(set(DATA["names"]) - used, set(), "translation without a place")


class Schematic(unittest.TestCase):
    """The licence-clean alternative dataset in schematic/: our own drawings of the walkable geometry."""

    def test_same_maps_and_names_as_the_main_dataset(self):
        self.assertEqual(set(SCHEMATIC_DATA["maps"]), set(DATA["maps"]))
        self.assertEqual(SCHEMATIC_DATA["names"], DATA["names"])

    def test_rows_are_valid(self):
        for mid, m in SCHEMATIC_DATA["maps"].items():
            for row in m["places"]:
                with self.subTest(map=mid, place=row[0]):
                    self.assertEqual(len(row), 6)
                    self.assertTrue(0 <= row[1] <= 1000 and 0 <= row[2] <= 1000)
                    self.assertIn(row[3], {"t", "ct", "m"})
                    self.assertIn(row[4], {"a", "b", "m"})
                    self.assertIn(row[5], {-1, 0, 1, 2})
                    self.assertIn(row[0], SCHEMATIC_DATA["names"])

    def test_every_map_has_a_schema_image(self):
        for mid in SCHEMATIC_DATA["maps"]:
            with self.subTest(map=mid):
                f = SCHEMATIC / "maps" / f"{mid}.webp"
                self.assertTrue(f.is_file())
                head = f.read_bytes()[:12]
                self.assertEqual(head[:4], b"RIFF")
                self.assertEqual(head[8:12], b"WEBP")

    def test_data_files_cover_all_maps(self):
        meta = json.loads((SCHEMATIC / "data" / "meta.json").read_text(encoding="utf-8"))
        fit = json.loads((SCHEMATIC / "data" / "fit_report.json").read_text(encoding="utf-8"))
        with (SCHEMATIC / "data" / "nav_places.csv").open(encoding="utf-8") as fh:
            csv_maps = {r["map"] for r in csv.DictReader(fh)}
        for mid in SCHEMATIC_DATA["maps"]:
            with self.subTest(map=mid):
                self.assertIn(mid, meta)
                self.assertIn(mid, fit)
                self.assertIn(mid, csv_maps)


if __name__ == "__main__":
    unittest.main()
