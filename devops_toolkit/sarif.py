from __future__ import annotations

import json

from .baseline import finding_fingerprint
from .models import AuditReport, Finding


def _level(finding: Finding) -> str:
    if finding.severity == "error":
        return "error"
    if finding.severity == "warning":
        return "warning"
    return "note"


def render_sarif(report: AuditReport) -> str:
    rules = {}
    for finding in report.findings:
        rules[finding.check] = {
            "id": finding.check,
            "name": finding.check,
            "shortDescription": {"text": finding.message},
        }
    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "devops-audit-toolkit", "rules": list(rules.values())}},
                "results": [
                    {
                        "ruleId": finding.check,
                        "level": _level(finding),
                        "message": {"text": finding.message},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": finding.path.relative_to(report.root).as_posix()
                                    }
                                }
                            }
                        ],
                        "partialFingerprints": {"primaryLocationLineHash": finding_fingerprint(finding)},
                    }
                    for finding in report.findings
                ],
            }
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
