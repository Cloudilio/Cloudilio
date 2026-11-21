"""The scheduled job: Cloudilio runs `python job.py` on the schedule set on the Scheduled Tasks tab.

This example records each run, with a timestamp and a small calculation, to a file in APP_DATA_DIR.
Replace the body of `run()` with your own work: fetching data, sending a report, cleaning up files.
"""
import json
import os
import random
import time

DATA_DIR = os.environ.get("APP_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
RUNS_FILE = os.path.join(DATA_DIR, "runs.json")
KEEP = 50


def run():
    numbers = [random.randint(1, 100) for _ in range(10)]
    return {"sum": sum(numbers), "largest": max(numbers)}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    started = time.time()
    result = run()
    entry = {"at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
             "seconds": round(time.time() - started, 3), "result": result}
    try:
        with open(RUNS_FILE) as f:
            runs = json.load(f)
    except (OSError, ValueError):
        runs = []
    runs = ([entry] + runs)[:KEEP]
    with open(RUNS_FILE, "w") as f:
        json.dump(runs, f, indent=2)
    print(f"Run finished: {entry}", flush=True)


if __name__ == "__main__":
    main()
