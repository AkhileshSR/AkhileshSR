
#!/usr/bin/env python3
"""
Pomodoro Timer (Console)
------------------------
Simple Pomodoro timer: work/break cycles with progress output.

Example:
    python pomodoro.py --work 25 --short 5 --long 15 --cycles 4
"""
import time
import argparse


def countdown(minutes: int, label: str):
    seconds = minutes * 60
    while seconds >= 0:
        mm, ss = divmod(seconds, 60)
        print(f"{label}: {mm:02d}:{ss:02d}", end='')
        time.sleep(1)
        seconds -= 1
    print()  # newline after phase ends


def run_pomodoro(work: int, short: int, long: int, cycles: int):
    for i in range(1, cycles + 1):
        print(f"
[Cycle {i}/{cycles}] Focus")
        countdown(work, 'Work')
        if i % 4 == 0:
            print("Long break")
            countdown(long, 'Break')
        else:
            print("Short break")
            countdown(short, 'Break')
    print("
Done. Great job!")


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
