from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from typing import Iterable

from .models import Finding


@dataclass(frozen=True)
class AuditPolicy:
    fail_on: tuple[str, ...] = ("error", "warning")
    ignored_paths: tuple[str, ...] = ()

    def filter_findings(self, findings: Iterable[Finding]) -> list[Finding]:
        return [
            finding
            for finding in findings
            if not any(fnmatch(finding.path.as_posix(), pattern) for pattern in self.ignored_paths)
        ]

    def should_fail(self, findings: Iterable[Finding]) -> bool:
        gates = set(self.fail_on)
        return any(finding.severity in gates for finding in findings)
