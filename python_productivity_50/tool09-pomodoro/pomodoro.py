#!/usr/bin/env python3
"""
Pomodoro Timer (Console)
Author : Akhilesh Singh (AkhileshSR)
License: MIT (see LICENSE) — Free to use with attribution.

This script is intentionally **well-commented** to be approachable for
experienced programmers who are newer to Python.
"""

import time
import argparse

# --- Implementation notes ---------------------------------------------------
# - Console-only countdowns; simple and portable.
# - Defaults to the classic 25/5 with a 15-min long break every 4 cycles.
# ----------------------------------------------------------------------------

def countdown(minutes: int, label: str):
    seconds = minutes * 60
    while seconds >= 0:
        mm, ss = divmod(seconds, 60)
        print(f"\r{label}: {mm:02d}:{ss:02d}", end='')
        time.sleep(1)
        seconds -= 1
    print()  # newline after phase ends


def run_pomodoro(work: int, short: int, long: int, cycles: int):
    for i in range(1, cycles + 1):
        print(f"\n[Cycle {i}/{cycles}] Focus")
        countdown(work, 'Work')
        if i % 4 == 0:
            print("Long break")
            countdown(long, 'Break')
        else:
            print("Short break")
            countdown(short, 'Break')
    print("\nDone. Great job!")



def main():
    ap = argparse.ArgumentParser(description='Console Pomodoro timer.')
    ap.add_argument('--work', type=int, default=25, help='Work minutes')
    ap.add_argument('--short', type=int, default=5, help='Short break minutes')
    ap.add_argument('--long', type=int, default=15, help='Long break minutes')
    ap.add_argument('--cycles', type=int, default=4, help='Number of focus cycles')
    args = ap.parse_args()
    run_pomodoro(args.work, args.short, args.long, args.cycles)

if __name__ == '__main__':
    main()

