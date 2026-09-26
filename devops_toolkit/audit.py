from pathlib import Path

from .checks import run_all_checks
from .inventory import build_inventory
from .models import AuditReport


def run_audit(root: str | Path) -> AuditReport:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError(f"Audit root must be an existing directory: {root_path}")
    inventory = build_inventory(root_path)
    findings = run_all_checks(inventory)
    return AuditReport(root=root_path, inventory=inventory, findings=findings)

