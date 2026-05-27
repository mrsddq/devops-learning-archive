import json
import tempfile
import unittest
from pathlib import Path

from devops_toolkit.config import load_config
from devops_toolkit.models import Finding


class ConfigTests(unittest.TestCase):
    def test_config_loads_policy_gate_and_ignored_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "policy.json"
            path.write_text(
                json.dumps({"policy": {"fail_on": ["error"], "ignored_paths": ["docs/*"]}}),
                encoding="utf-8",
            )
            config = load_config(path)

        warning = Finding("x", Path("main.tf"), "message", "warning")
        self.assertFalse(config.policy.should_fail([warning]))
        self.assertEqual(config.policy.filter_findings([Finding("x", Path("docs/a.md"), "m")]), [])


if __name__ == "__main__":
    unittest.main()
