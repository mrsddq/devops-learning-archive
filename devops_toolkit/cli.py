import argparse
from pathlib import Path

from .audit import run_audit
from .baseline import filter_new_findings, write_baseline
from .config import load_config
from .reporting import format_json_report, format_text_report
from .sarif import render_sarif


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and validate a DevOps repository.")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], help="Repository root to scan.")
    parser.add_argument("--config", type=Path, help="Optional JSON policy configuration.")
    parser.add_argument("--baseline", type=Path, help="Existing baseline JSON; only new findings are reported.")
    parser.add_argument("--write-baseline", type=Path, help="Write a baseline JSON for current findings.")
    parser.add_argument("--format", choices=["text", "json", "sarif"], help="Report format.")
    parser.add_argument("--output", type=Path, help="Optional report output path.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when warnings are found.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    parser.add_argument("--include-info", action="store_true", help="Include informational findings in text output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    report = run_audit(args.root)
    report.findings = config.policy.filter_findings(report.findings)
    if args.write_baseline:
        write_baseline(args.write_baseline, report.findings)
    report.findings = filter_new_findings(report.findings, args.baseline)

    report_format = "json" if args.json else (args.format or config.default_format)
    if report_format == "json":
        output = format_json_report(report)
    elif report_format == "sarif":
        output = render_sarif(report)
    else:
        output = format_text_report(report, include_info=args.include_info)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)

    return 1 if args.strict and config.policy.should_fail(report.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
