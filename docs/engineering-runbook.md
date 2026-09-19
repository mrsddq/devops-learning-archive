# DevOps Learning Archive: Engineering Runbook

This repository preserves DevOps coursework and reference labs. Its maintained
Python auditor checks repository files; it does not provision cloud resources or
validate historical deployments. See the [README](../README.md) for the learning
path and the distinction between archive material and the standalone audit toolkit.

## Verify the auditor

Use Python 3.11 or later from the repository root. The auditor and its unit tests
use the standard library and need no package installation.

```bash
python -m unittest discover -s tests
python -m devops_toolkit.cli --json
python scripts/devops_audit.py --strict
```

The unit tests exercise audit rules and the command-line entry point. The JSON
command produces an inventory and findings report. The strict command returns a
nonzero status when findings remain; a historical lab can legitimately trigger
that gate. Review each finding instead of changing policy only to obtain a pass.

These are static heuristic checks. They do not run Terraform plans, deploy
Kubernetes workloads, or prove that a lab is secure. Before executing a historical
deployment example, inspect its target account, credentials, costs and cleanup
instructions. Keep course attribution and original lesson context intact.

## Maintain changes

Run the auditor tests after changes to `devops_toolkit/` or its entry point. Check
the changed files with `git diff --check` and review `git status --short` before
committing. Do not commit credentials, generated environments or tool caches.
