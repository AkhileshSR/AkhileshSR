import argparse
import os
import runpy
import sys
from textwrap import dedent

# Map subcommands to the existing tool scripts (relative to this package dir)
TOOLS = {
    "folder-organizer": {
        "path": "tool01-folder-organizer/folder_organizer.py",
        "help": "Sort files by extension/date",
    },
    "duplicate-finder": {
        "path": "tool02-duplicate-finder/duplicate_finder.py",
        "help": "Find duplicate files by hash",
    },
    "smart-renamer": {
        "path": "tool03-smart-renamer/smart_renamer.py",
        "help": "Batch rename with prefix/suffix/patterns",
    },
    "pdf-tool": {
        "path": "tool04-pdf-tool/pdf_tool.py",
        "help": "Merge/split PDFs (page ranges)",
    },
    "disk-usage-report": {
        "path": "tool05-disk-usage-report/disk_usage_report.py",
        "help": "Largest files & dir size summary",
    },
    "log-summarizer": {
        "path": "tool06-log-summarizer/log_summarizer.py",
        "help": "Extract errors/warnings via regex",
    },
    "daily-planner": {
        "path": "tool07-daily-planner/daily_planner.py",
        "help": "Generate Markdown day planner",
    },
    "time-tracker": {
        "path": "tool08-time-tracker/time_tracker.py",
        "help": "Start/stop tasks, CSV reports",
    },
    "pomodoro": {
        "path": "tool09-pomodoro/pomodoro.py",
        "help": "Pomodoro focus timer (console)",
    },
    "image-resizer": {
        "path": "tool10-image-resizer/image_resizer.py",
        "help": "Bulk resize/compress images (Pillow)",
    },
}


def _run_script(rel_path: str, args: list[str]) -> int:
    """Execute a tool script as if run directly, preserving its own argparse UX."""
    pkg_dir = os.path.dirname(__file__)
    script_path = os.path.join(pkg_dir, rel_path)

    if not os.path.exists(script_path):
        available = "\n".join(
            f"  - {name:18} -> {meta['path']}" for name, meta in TOOLS.items()
        )
        print(
            f"[pp50] Script not found: {script_path}\nAvailable tools:\n{available}",
            file=sys.stderr,
        )
        return 2

    # Rebuild argv for the tool (so its argparse works normally)
    sys.argv = [script_path] + args

    # Run the script in __main__ context
    runpy.run_path(script_path, run_name="__main__")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pp50",
        description="Python Productivity 50 — unified CLI for the tools collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Pass arguments to a tool after `--`. Examples:

              pp50 folder-organizer -- --source . --dest sorted
              pp50 pdf-tool -- --merge A.pdf B.pdf -o merged.pdf
              pp50 image-resizer -- --input images --width 1024 --quality 85

            List tools:
              pp50 list
            """
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<tool|list>")

    # List command
    sp_list = subparsers.add_parser("list", help="List available tools")
    sp_list.set_defaults(handler=_handle_list)

    # Tool subcommands (forward the remainder)
    for name, meta in TOOLS.items():
        sp = subparsers.add_parser(name, help=meta["help"])
        sp.add_argument(
            "tool_args",
            nargs=argparse.REMAINDER,
            help="Arguments to pass to the tool (prefix with --)",
        )
        sp.set_defaults(handler=_make_tool_handler(name))

    return parser


def _handle_list(_ns: argparse.Namespace) -> int:
    print("Available tools:")
    for name, meta in TOOLS.items():
        print(f"  {name:18} - {meta['help']}  [{meta['path']}]")
    return 0


def _make_tool_handler(name: str):
    def _handler(ns: argparse.Namespace) -> int:
        args = ns.tool_args or []
        # Drop a leading '--' if present (common pattern to separate args)
        if args and args[0] == "--":
            args = args[1:]
        rel_path = TOOLS[name]["path"]
        return _run_script(rel_path, args)

    return _handler


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    ns = parser.parse_args(argv)

    if ns.command is None:
        parser.print_help()
        print("\nTip: run `pp50 list` to see available tools.")
        return 0

    handler = getattr(ns, "handler", None)
    if handler is None:
        parser.print_help()
        return 2

    return int(handler(ns) or 0)


if __name__ == "__main__":
    raise SystemExit(main())