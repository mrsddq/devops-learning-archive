from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .policy import AuditPolicy


@dataclass(frozen=True)
class AuditConfig:
    policy: AuditPolicy = AuditPolicy()
    default_format: str = "text"


def load_config(path: str | Path | None) -> AuditConfig:
    if path is None:
        return AuditConfig()
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    policy = raw.get("policy", raw)
    return AuditConfig(
        policy=AuditPolicy(
            fail_on=tuple(str(item) for item in policy.get("fail_on", ["error", "warning"])),
            ignored_paths=tuple(str(item) for item in policy.get("ignored_paths", [])),
        ),
        default_format=str(raw.get("default_format", "text")),
    )
