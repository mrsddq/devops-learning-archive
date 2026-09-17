"""Compatibility entry point for running the archive audit from a checkout."""
import sys
from pathlib import Path

# Direct script execution puts scripts/, not the repository root, on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from devops_toolkit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
