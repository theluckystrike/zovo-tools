#!/usr/bin/env python3
"""
Monitor Agent 15 Quality Gate Progress
Provides regular progress updates during the 2-hour continuous run
"""

import time
import os
import subprocess
from datetime import datetime

def get_log_stats(log_file):
    """Parse log file for progress stats"""
    if not os.path.exists(log_file):
        return {}

    try:
        with open(log_file, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        stats = {
            'total_lines': len(lines),
            'violations_found': content.count('Violations in'),
            'fixes_applied': content.count('Fixed violations in'),
            'loops_completed': content.count('Master Loop'),
            'tools_scanned': content.count('Scanning ') - content.count('Scanning 738'),  # Exclude the "Scanning X total" lines
            'commits_made': content.count('Committed'),
            'pull_updates': content.count('Pulled:'),
        }

        return stats

    except Exception as e:
        return {'error': str(e)}

def check_process_running(process_name):
    """Check if the quality gate process is still running"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        return len(result.stdout.strip()) > 0
    except:
        return False

def main():
    log_file = "/Users/mike/zovo-workspaces/zovo-tools/quality_gate_output.log"
    process_name = "agent15_quality_master"

    print("🎯 Agent 15 Quality Gate Monitor Started")
    print("=" * 60)

    start_time = datetime.now()
    update_count = 0

    while True:
        update_count += 1
        current_time = datetime.now()
        elapsed = current_time - start_time

        # Check if process is running
        is_running = check_process_running(process_name)

        # Get log stats
        stats = get_log_stats(log_file)

        print(f"\n📊 UPDATE #{update_count} - {current_time.strftime('%H:%M:%S')} - Elapsed: {elapsed.total_seconds()//60:.0f}min")
        print("-" * 40)
        print(f"Process Status: {'🟢 RUNNING' if is_running else '🔴 STOPPED'}")

        if stats:
            print(f"Total Log Lines: {stats.get('total_lines', 0)}")
            print(f"Violations Found: {stats.get('violations_found', 0)}")
            print(f"Fixes Applied: {stats.get('fixes_applied', 0)}")
            print(f"Loops Completed: {stats.get('loops_completed', 0)}")
            print(f"Tools Scanned: {stats.get('tools_scanned', 0)}")
            print(f"Commits Made: {stats.get('commits_made', 0)}")
            print(f"Pull Updates: {stats.get('pull_updates', 0)}")

        # Show latest activity
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                if len(lines) > 10:
                    print("\n📝 Latest Activity:")
                    for line in lines[-5:]:
                        if line.strip():
                            print(f"  {line.strip()}")
            except:
                pass

        if not is_running:
            print("\n⚠️ Process stopped - Quality Gate monitoring ending")
            break

        # Wait 5 minutes before next update
        print(f"\n⏰ Next update in 5 minutes...")
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitor interrupted by user")
        print("✅ Exiting gracefully...")