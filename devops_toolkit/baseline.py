from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import Finding


BASELINE_VERSION = 1


def finding_fingerprint(finding: Finding) -> str:
    payload = "|".join([finding.check, finding.path.as_posix(), finding.message, finding.severity])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_baseline(path: str | Path, findings: Iterable[Finding]) -> None:
    baseline_path = Path(path)
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": BASELINE_VERSION,
        "findings": [
            {
                "fingerprint": finding_fingerprint(finding),
                "check": finding.check,
                "path": finding.path.as_posix(),
                "message": finding.message,
                "severity": finding.severity,
            }
            for finding in sorted(findings, key=lambda item: (item.path.as_posix(), item.check))
        ],
    }
    baseline_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_baseline(path: str | Path) -> set[str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if int(payload.get("version", 0)) != BASELINE_VERSION:
        raise ValueError(f"Unsupported baseline version: {path}")
    return {str(item["fingerprint"]) for item in payload.get("findings", [])}


def filter_new_findings(findings: Iterable[Finding], baseline_path: str | Path | None) -> list[Finding]:
    items = list(findings)
    if baseline_path is None:
        return items
    known = load_baseline(baseline_path)
    return [finding for finding in items if finding_fingerprint(finding) not in known]
