#!/usr/bin/env python3
"""
Continuous Technical QA Runner
Runs technical validation every 45 seconds for 2+ hours with git operations
"""

import time
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mike/zovo-workspaces/zovo-tools/continuous_qa.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContinuousQARunner:
    def __init__(self):
        self.base_dir = Path('/Users/mike/zovo-workspaces/zovo-tools')
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=2, minutes=10)  # 2+ hours
        self.cycle_count = 0
        self.total_issues_fixed = 0

    def git_pull_repos(self):
        """Pull latest changes from git repositories"""
        try:
            # Pull main zovo-tools repo
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info("Git pull successful")
                if "Already up to date" not in result.stdout:
                    logger.info(f"Updates pulled: {result.stdout.strip()}")
            else:
                logger.warning(f"Git pull failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.error("Git pull timed out")
        except Exception as e:
            logger.error(f"Git pull error: {str(e)}")

    def run_technical_validation(self):
        """Run the technical validation suite"""
        try:
            result = subprocess.run(
                ['python3', 'technical_qa_validator.py'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info("Technical validation completed successfully")
                return True
            else:
                logger.error(f"Technical validation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Technical validation timed out")
            return False
        except Exception as e:
            logger.error(f"Technical validation error: {str(e)}")
            return False

    def commit_improvements(self):
        """Commit technical improvements to git"""
        try:
            # Check for changes
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            if status_result.stdout.strip():
                # Add changes
                subprocess.run(
                    ['git', 'add', '.'],
                    cwd=self.base_dir,
                    check=True,
                    timeout=30
                )

                # Get latest QA report for commit message
                qa_reports = list(self.base_dir.glob('technical_qa_report_*.json'))
                if qa_reports:
                    latest_report = max(qa_reports, key=lambda x: x.stat().st_mtime)
                    with open(latest_report) as f:
                        report_data = json.load(f)

                    commit_message = f"""Technical QA improvements - Cycle {self.cycle_count}

- Tools processed: {report_data['tools_processed']}
- Issues found: {report_data['total_issues']}
- Fixes applied: {report_data['fixes_applied']}

Categories fixed:
{chr(10).join(f'- {cat}: {count}' for cat, count in report_data['issues_by_category'].items() if count > 0)}

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"""
                else:
                    commit_message = f"""Technical QA improvements - Cycle {self.cycle_count}

Automated technical validation and fixes applied.

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"""

                # Commit changes
                subprocess.run(
                    ['git', 'commit', '-m', commit_message],
                    cwd=self.base_dir,
                    check=True,
                    timeout=30
                )

                logger.info(f"Committed technical improvements for cycle {self.cycle_count}")
                return True
            else:
                logger.info("No changes to commit")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Git commit timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Git commit failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Git commit error: {str(e)}")
            return False

    def cleanup_old_reports(self):
        """Remove old QA reports to prevent disk space issues"""
        try:
            qa_reports = list(self.base_dir.glob('technical_qa_report_*.json'))
            if len(qa_reports) > 10:  # Keep only latest 10 reports
                old_reports = sorted(qa_reports, key=lambda x: x.stat().st_mtime)[:-10]
                for report in old_reports:
                    report.unlink()
                logger.info(f"Cleaned up {len(old_reports)} old QA reports")
        except Exception as e:
            logger.error(f"Report cleanup error: {str(e)}")

    def generate_cycle_summary(self):
        """Generate summary of current QA cycle"""
        current_time = datetime.now()
        elapsed = current_time - self.start_time
        remaining = self.end_time - current_time

        logger.info("=== QA CYCLE SUMMARY ===")
        logger.info(f"Cycle: {self.cycle_count}")
        logger.info(f"Elapsed time: {elapsed}")
        logger.info(f"Remaining time: {remaining}")
        logger.info(f"Total cycles planned: {int((self.end_time - self.start_time).total_seconds() / 45)}")

        # Get latest report stats
        qa_reports = list(self.base_dir.glob('technical_qa_report_*.json'))
        if qa_reports:
            latest_report = max(qa_reports, key=lambda x: x.stat().st_mtime)
            with open(latest_report) as f:
                report_data = json.load(f)

            logger.info(f"Last cycle results:")
            logger.info(f"  - Tools processed: {report_data['tools_processed']}")
            logger.info(f"  - Issues found: {report_data['total_issues']}")
            logger.info(f"  - Fixes applied: {report_data['fixes_applied']}")

    def run_continuous_qa(self):
        """Main continuous QA loop"""
        logger.info("=== STARTING CONTINUOUS TECHNICAL QA ===")
        logger.info(f"Start time: {self.start_time}")
        logger.info(f"End time: {self.end_time}")
        logger.info("Focus: F-M tools technical validation")
        logger.info("Interval: 45 seconds")

        while datetime.now() < self.end_time:
            self.cycle_count += 1
            cycle_start = datetime.now()

            logger.info(f"\n=== QA CYCLE {self.cycle_count} STARTING ===")

            # Step 1: Git pull
            logger.info("Step 1: Pulling latest changes...")
            self.git_pull_repos()

            # Step 2: Run technical validation
            logger.info("Step 2: Running technical validation suite...")
            validation_success = self.run_technical_validation()

            # Step 3: Commit improvements
            if validation_success:
                logger.info("Step 3: Committing technical improvements...")
                self.commit_improvements()
            else:
                logger.warning("Step 3: Skipping commit due to validation failure")

            # Step 4: Generate cycle summary
            self.generate_cycle_summary()

            # Step 5: Cleanup
            self.cleanup_old_reports()

            # Calculate timing for next cycle
            cycle_duration = datetime.now() - cycle_start
            sleep_time = max(0, 45 - cycle_duration.total_seconds())

            if sleep_time > 0:
                logger.info(f"Cycle completed in {cycle_duration.total_seconds():.1f}s, sleeping for {sleep_time:.1f}s")
                time.sleep(sleep_time)
            else:
                logger.warning(f"Cycle took {cycle_duration.total_seconds():.1f}s, exceeding 45s target")

        logger.info("=== CONTINUOUS QA COMPLETED ===")
        logger.info(f"Total cycles completed: {self.cycle_count}")
        logger.info(f"Total runtime: {datetime.now() - self.start_time}")

def main():
    runner = ContinuousQARunner()
    runner.run_continuous_qa()

if __name__ == "__main__":
    main()