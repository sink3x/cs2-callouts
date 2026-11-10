"""schematic/callouts.json must be exactly what schematic/scripts/build.py produces from schematic/data/ (so data and artifact never drift)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "schematic"


class Reproducible(unittest.TestCase):
    def test_build_reproduces_callouts_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "scripts").mkdir()
            shutil.copytree(ROOT / "data", work / "data")
            for f in (ROOT / "scripts").glob("*.py"):
                shutil.copy(f, work / "scripts" / f.name)
            subprocess.run([sys.executable, str(work / "scripts" / "build.py")], check=True, capture_output=True)
            built = json.loads((work / "callouts.json").read_text(encoding="utf-8"))
        committed = json.loads((ROOT / "callouts.json").read_text(encoding="utf-8"))
        self.assertEqual(built, committed)


if __name__ == "__main__":
    unittest.main()
