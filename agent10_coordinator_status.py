#!/usr/bin/env python3
"""
Agent 10: Real-time Status Monitor
Tracks progress of continuous quality monitoring
"""

import os
import time
import subprocess
from pathlib import Path
from datetime import datetime

def get_git_status():
    """Get current git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'],
                              capture_output=True, text=True,
                              cwd='/Users/mike/zovo-workspaces/zovo-tools')
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return 0

def get_recent_commits():
    """Get recent commits count from last hour"""
    try:
        result = subprocess.run(['git', 'log', '--since="1 hour ago"', '--oneline'],
                              capture_output=True, text=True,
                              cwd='/Users/mike/zovo-workspaces/zovo-tools')
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return 0

def count_html_files():
    """Count total HTML files"""
    base_dir = Path('/Users/mike/zovo-workspaces/zovo-tools')
    return len(list(base_dir.glob('*/index.html')))

def monitor_coordination():
    """Monitor coordination status"""
    start_time = time.time()

    print("=== AGENT 10 COORDINATION STATUS MONITOR ===")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print("Monitoring quality gate coordination...")
    print()

    loop_count = 0

    while True:
        loop_count += 1
        elapsed_mins = (time.time() - start_time) / 60

        # Get current status
        changed_files = get_git_status()
        recent_commits = get_recent_commits()
        html_files = count_html_files()

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Loop #{loop_count} | "
              f"Runtime: {elapsed_mins:.1f}min | "
              f"HTML files: {html_files} | "
              f"Changed: {changed_files} | "
              f"Recent commits: {recent_commits}")

        # Check if main quality loop is still running
        try:
            with open('/private/tmp/claude-501/-Users-mike/tasks/bpst798dp.output', 'r') as f:
                output = f.read()
                if 'AGENT 10:' in output[-1000:]:  # Check last 1000 chars
                    last_activity = "Active"
                else:
                    last_activity = "Quiet"
        except:
            last_activity = "Unknown"

        print(f"    Quality loop status: {last_activity}")

        # Report every 5 minutes
        if loop_count % 10 == 0:  # Every 10 loops (5 minutes)
            print("\n" + "="*60)
            print(f"COORDINATION REPORT - {elapsed_mins:.1f} minutes elapsed")
            print(f"Total HTML files monitored: {html_files}")
            print(f"Files currently changed: {changed_files}")
            print(f"Commits in last hour: {recent_commits}")
            print(f"Main quality loop: {last_activity}")
            print("="*60 + "\n")

        time.sleep(30)  # Status update every 30 seconds

if __name__ == "__main__":
    monitor_coordination()