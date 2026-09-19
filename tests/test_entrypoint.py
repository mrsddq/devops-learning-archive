import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class EntrypointTests(unittest.TestCase):
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
