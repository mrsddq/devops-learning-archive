import json
import tempfile
import unittest
from pathlib import Path

from devops_toolkit.models import AuditReport, FileInventory, Finding
from devops_toolkit.sarif import render_sarif


class SarifTests(unittest.TestCase):
    def test_sarif_contains_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            finding = Finding("docker-runtime", root / "Dockerfile", "missing CMD")
            report = AuditReport(root=root, inventory=FileInventory(), findings=[finding])
            payload = json.loads(render_sarif(report))

        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(payload["runs"][0]["results"][0]["ruleId"], "docker-runtime")


if __name__ == "__main__":
    unittest.main()
