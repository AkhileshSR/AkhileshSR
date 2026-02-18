#!/usr/bin/env python3
"""
Time Tracker (CLI)
Author : Akhilesh Singh (AkhileshSR)
License: MIT (see LICENSE) — Free to use with attribution.

This script is intentionally **well-commented** to be approachable for
experienced programmers who are newer to Python.
"""

from pathlib import Path
import argparse
from datetime import datetime, date
import csv

# --- Implementation notes ---------------------------------------------------
# - Minimal state file to track a single running task.
# - Appends sessions to a CSV for simple analytics and portability.
# - Report shows totals per task for a given day.
# ----------------------------------------------------------------------------

DATA_DIR = Path.home() / '.time_tracker'
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / 'state.txt'
LOG_FILE = DATA_DIR / 'events.csv'


def now_iso():
    return datetime.now().isoformat(timespec='seconds')


def start_task(task: str):
    if STATE_FILE.exists():
        print('[ERR] A task is already running. Stop it first.')
        return
    STATE_FILE.write_text(task + '\n' + now_iso(), encoding='utf-8')
    print(f"[OK] Started: {task}")


def stop_task():
    if not STATE_FILE.exists():
        print('[ERR] No running task.')
        return
    task, start = STATE_FILE.read_text(encoding='utf-8').splitlines()[:2]
    STATE_FILE.unlink(missing_ok=True)
    end = now_iso()
    duration = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds()

    new = not LOG_FILE.exists()
    with LOG_FILE.open('a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if new:
            w.writerow(['date', 'task', 'start', 'end', 'seconds'])
        w.writerow([start[:10], task, start, end, int(duration)])
    print(f"[OK] Stopped: {task} ({int(duration//60)} min)")


def report(day: str | None):
    if not LOG_FILE.exists():
        print('No data yet.')
        return
    day = day or date.today().isoformat()
    total = 0
    by_task = {}
    with LOG_FILE.open('r', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            if row['date'] == day:
                s = int(row['seconds'])
                total += s
                by_task[row['task']] = by_task.get(row['task'], 0) + s
    print(f"Report for {day}:")
    for t, s in sorted(by_task.items(), key=lambda x: x[1], reverse=True):
        print(f" - {t}: {int(s//60)} min")
    print(f"Total: {int(total//60)} min")


def main():
    ap = argparse.ArgumentParser(description='Simple CLI time tracker (CSV backend).')
    sub = ap.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('start', help='Start a task')
    s.add_argument('--task', required=True)

    e = sub.add_parser('stop', help='Stop running task')

    r = sub.add_parser('report', help='Show totals for a date (default today)')
    r.add_argument('--date', type=str)

    args = ap.parse_args()
    if args.cmd == 'start':
        start_task(args.task)
    elif args.cmd == 'stop':
        stop_task()
    else:
        report(args.date)

if __name__ == '__main__':
    main()

