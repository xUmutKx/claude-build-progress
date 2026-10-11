#!/usr/bin/env python3
"""Read a Gradle log and print where the build is: running, done or failed."""
import glob
import os
import re
import sys
import time

LOG_DIRS = [os.environ.get("BUILD_LOG_DIR", ""), "_logs", "."]
PATTERNS = ("*_compile*.log", "*_build*.log", "build*.log")


def newest_log(arg):
    if arg and os.path.isfile(arg):
        return arg
    folder = arg if arg and os.path.isdir(arg) else None
    dirs = [folder] if folder else [d for d in LOG_DIRS if d and os.path.isdir(d)]
    found = []
    for d in dirs:
        for p in PATTERNS:
            found += glob.glob(os.path.join(d, p))
    return max(found, key=os.path.getmtime) if found else None


def fmt(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s:02d}s" if m else f"{s}s"


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    path = newest_log(arg)
    if not path:
        print("No Gradle log found. Pass a log file or set BUILD_LOG_DIR.")
        return
    with open(path, errors="replace") as f:
        lines = [l.rstrip("\n") for l in f]

    tasks = [l for l in lines if l.startswith("> Task ")]
    errors = [l for l in lines if l.startswith("e: ")]
    exit_line = next((l for l in lines if l.startswith("exit=")), None)
    result = next((l for l in lines if l.startswith("BUILD ")), None)
    summary = next((l for l in lines if re.match(r"\d+ actionable tasks", l)), None)

    if exit_line:
        state = "OK" if exit_line.startswith("exit=0") else "FAILED"
    elif result:
        state = "OK" if "SUCCESSFUL" in result else "FAILED"
    else:
        state = "RUNNING"

    print(f"Log: {path}")
    print(f"Status: {state}" + (f" ({result})" if result else ""))
    print(f"Tasks seen: {len(tasks)}" + (f" | {summary}" if summary else ""))
    if state == "RUNNING":
        print(f"Running for: {fmt(time.time() - os.path.getmtime(path))} since last log write")
        if tasks:
            print(f"Current task: {tasks[-1][len('> Task '):]}")
    if exit_line:
        print(exit_line)
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors[:5]:
            print(f"  {e}")


if __name__ == "__main__":
    main()
