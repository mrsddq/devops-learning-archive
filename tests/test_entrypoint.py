import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from devops_toolkit.audit import run_audit


class EntrypointTests(unittest.TestCase):
    def test_invalid_roots_cannot_report_a_clean_audit(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            file = Path(temp_dir) / "file.txt"
            file.write_text("not a directory", encoding="utf-8")
            for invalid_root in (Path(temp_dir) / "missing", file):
                with self.subTest(root=invalid_root):
                    with self.assertRaisesRegex(ValueError, "existing directory"):
                        run_audit(invalid_root)
                    result = subprocess.run(
                        [sys.executable, str(root / "scripts/devops_audit.py"), "--root", str(invalid_root), "--strict"],
                        cwd=temp_dir, capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("existing directory", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_script_runs_from_outside_repository(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as outside:
            result = subprocess.run(
                [sys.executable, str(root / "scripts/devops_audit.py"), "--root", str(root), "--json"],
                cwd=outside, capture_output=True, text=True, check=True,
            )
        payload = json.loads(result.stdout)
        self.assertIn("summary", payload)
        self.assertIn("findings", payload)


if __name__ == "__main__":
    unittest.main()
