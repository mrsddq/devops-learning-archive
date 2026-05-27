import json
import tempfile
import unittest
from pathlib import Path

from devops_toolkit.baseline import filter_new_findings, finding_fingerprint, write_baseline
from devops_toolkit.models import Finding


class BaselineTests(unittest.TestCase):
    def test_fingerprint_is_stable(self):
        finding = Finding("docker-runtime", Path("Dockerfile"), "missing CMD")
        self.assertEqual(finding_fingerprint(finding), finding_fingerprint(finding))

    def test_baseline_filters_existing_findings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline = Path(temp_dir) / "baseline.json"
            existing = Finding("docker-runtime", Path("Dockerfile"), "missing CMD")
            new = Finding("terraform-tags", Path("main.tf"), "missing tags", "info")
            write_baseline(baseline, [existing])
            remaining = filter_new_findings([existing, new], baseline)

        self.assertEqual([finding.check for finding in remaining], ["terraform-tags"])

    def test_baseline_schema_is_versioned(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline = Path(temp_dir) / "baseline.json"
            write_baseline(baseline, [Finding("x", Path("a"), "m")])
            payload = json.loads(baseline.read_text(encoding="utf-8"))

        self.assertEqual(payload["version"], 1)


if __name__ == "__main__":
    unittest.main()
