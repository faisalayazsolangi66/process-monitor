#!/usr/bin/env python3
"""List the top processes by CPU or memory usage (via `ps`)."""
import argparse
import subprocess
import sys


def get_processes(sort_by):
    # ps columns: %cpu, %mem, pid, user, command
    cmd = ["ps", "aux", "--sort", f"-{sort_by}"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("Error: the `ps` command was not found on this system.", file=sys.stderr)
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error running ps: {e}", file=sys.stderr)
        return []
    lines = out.stdout.strip().splitlines()
    rows = []
    for line in lines[1:]:  # skip header
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        rows.append({
            "user": parts[0], "pid": parts[1], "cpu": parts[2],
            "mem": parts[3], "command": parts[10],
        })
    return rows


def main():
    p = argparse.ArgumentParser(description="List the top processes by CPU or memory usage.")
    p.add_argument("--sort", choices=["cpu", "mem"], default="cpu",
                   help="Sort by CPU or memory usage (default: cpu)")
    p.add_argument("--limit", type=int, default=10,
                   help="How many processes to show (default: 10)")
    p.add_argument("--user", help="Only show processes owned by this user")
    args = p.parse_args()
    if args.limit < 1:
        p.error("--limit must be at least 1")

    sort_key = "%cpu" if args.sort == "cpu" else "%mem"
    rows = get_processes(sort_key)
    if args.user:
        rows = [r for r in rows if r["user"] == args.user]
    rows = rows[: args.limit]
    if not rows:
        print("No processes found.")
        return 0

    print(f"{'PID':>7} {'USER':<12} {'%CPU':>6} {'%MEM':>6}  COMMAND")
    print("-" * 80)
    for r in rows:
        cmd = r["command"][:60]
        print(f"{r['pid']:>7} {r['user']:<12} {r['cpu']:>6} {r['mem']:>6}  {cmd}")
    print(f"\nShowing {len(rows)} process(es) sorted by {args.sort.upper()} usage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
