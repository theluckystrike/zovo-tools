#!/usr/bin/env python3
"""
Monitor Agent 9 Quality Gate Progress
"""

import time
import subprocess
import re
from datetime import datetime

def get_recent_commits():
    """Get recent commits related to quality gate"""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '-20'],
            cwd='/Users/mike/zovo-workspaces/zovo-tools',
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n')
    except:
        return []

def check_process_running():
    """Check if Agent 9 is still running"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'agent9_safe_quality_gate'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def get_uz_tools_with_duplicates():
    """Count U-Z tools that still have duplicate canonicals"""
    import os
    import glob

    base_dir = '/Users/mike/zovo-workspaces/zovo-tools'
    duplicate_count = 0
    total_uz_tools = 0

    for tool_dir in os.listdir(base_dir):
        if (os.path.isdir(os.path.join(base_dir, tool_dir)) and
            tool_dir[0].lower() in 'uvwxyz'):

            total_uz_tools += 1
            html_file = os.path.join(base_dir, tool_dir, 'index.html')

            if os.path.exists(html_file):
                try:
                    with open(html_file, 'r') as f:
                        content = f.read()
                    if content.count('rel="canonical"') > 1:
                        duplicate_count += 1
                except:
                    pass

    return duplicate_count, total_uz_tools

def main():
    start_time = time.time()
    last_commit_hash = None

    print("🔍 Monitoring Agent 9 - Continuous Quality Gate")
    print("Focus: U-Z tools duplicate canonical URLs")
    print("-" * 50)

    while time.time() - start_time < 7200:  # 2 hours
        current_time = datetime.now().strftime('%H:%M:%S')
        elapsed_minutes = (time.time() - start_time) / 60

        # Check if process is still running
        is_running = check_process_running()
        status = "🟢 RUNNING" if is_running else "🔴 STOPPED"

        # Check for new commits
        commits = get_recent_commits()
        latest_commit = commits[0] if commits else ""

        if latest_commit != last_commit_hash:
            if 'Quality Gate Loop' in latest_commit:
                print(f"✅ {current_time} - NEW COMMIT: {latest_commit}")
            last_commit_hash = latest_commit

        # Check remaining duplicate canonicals
        duplicates, total = get_uz_tools_with_duplicates()

        print(f"📊 {current_time} - {status} | Elapsed: {elapsed_minutes:.0f}min | "
              f"Duplicates remaining: {duplicates}/{total} U-Z tools")

        # Sleep for 2 minutes between checks
        time.sleep(120)

    print("\n🏁 Monitoring complete - 2 hours elapsed")

if __name__ == "__main__":
    main()