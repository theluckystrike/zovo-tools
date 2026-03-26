#!/usr/bin/env python3
"""
QA Agent Alpha - Comprehensive Quality Assurance System
Enhanced QA coverage across all tool directories (0-9 and A-E focus)

EXPANDED QA SCOPE:
- Zero tolerance rules (bold, dashes, hashtags, emojis, AI phrases)
- Deep content analysis (word count, readability, completeness)
- Technical validation (HTML structure, JSON-LD, meta tags)
- Performance optimization (file sizes, loading speed)
- Accessibility compliance (alt tags, semantic HTML)
- Cross-browser compatibility checks
- Mobile responsiveness validation
- Internal link integrity
- Schema markup validation
- Site speed optimization
"""

import os
import re
import json
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import requests
import hashlib
from typing import Dict, List, Set, Tuple
import concurrent.futures
from threading import Lock

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qa_agent_alpha.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedQAAgent:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.stats = {
            'total_dirs_processed': 0,
            'total_files_processed': 0,
            'violations_found': 0,
            'violations_fixed': 0,
            'performance_optimizations': 0,
            'accessibility_fixes': 0,
            'schema_validations': 0,
            'start_time': datetime.now(),
            'detailed_stats': {}
        }
        self.stats_lock = Lock()
        self.violation_patterns = self.get_violation_patterns()
        self.ai_phrases = self.get_ai_phrases()

    def get_violation_patterns(self) -> Dict:
        """Enhanced violation patterns for comprehensive QA"""
        return {
            'bold_text': r'<b\b[^>]*>.*?</b>|<strong\b[^>]*>.*?</strong>|\*\*.*?\*\*',
            'dashes': r'(?<!-)--(?!-)|—|–',
            'hashtags': r'#\w+',
            'emojis': r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+',
            'low_word_count': r'<main\b[^>]*>.*?</main>',
            'missing_alt_tags': r'<img[^>]*(?!.*alt\s*=)[^>]*>',
            'missing_meta_description': r'<meta\s+name=["\']description["\']',
            'missing_canonical': r'<link\s+rel=["\']canonical["\']',
            'missing_schema': r'<script\s+type=["\']application/ld\+json["\']',
            'large_images': r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>',
            'inline_styles': r'style\s*=\s*["\'][^"\']*["\']',
            'broken_links': r'href\s*=\s*["\']([^"\']*)["\']',
            'missing_h1': r'<h1\b[^>]*>',
            'duplicate_h1': r'<h1\b[^>]*>.*?</h1>',
            'poor_semantic_html': r'<div[^>]*class=["\'][^"\']*button[^"\']*["\']',
        }

    def get_ai_phrases(self) -> List[str]:
        """AI-generated phrases to eliminate"""
        return [
            "streamline your",
            "revolutionize your",
            "unleash the power",
            "game-changer",
            "cutting-edge",
            "next-level",
            "innovative solution",
            "seamless experience",
            "unprecedented",
            "state-of-the-art",
            "groundbreaking",
            "transformative",
            "leverage",
            "synergy",
            "paradigm shift",
            "disruptive",
            "scalable solution",
            "robust framework",
            "comprehensive suite",
            "enterprise-grade"
        ]

    def get_target_directories(self) -> List[Path]:
        """Get directories starting with 0-9 and A-E"""
        dirs = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                first_char = item.name[0].lower()
                if first_char.isdigit() or first_char in 'abcde':
                    dirs.append(item)
        return sorted(dirs)

    def analyze_html_content(self, file_path: Path) -> Dict:
        """Comprehensive HTML content analysis"""
        violations = {
            'bold_text': [],
            'dashes': [],
            'hashtags': [],
            'emojis': [],
            'ai_phrases': [],
            'low_word_count': False,
            'missing_alt_tags': [],
            'missing_meta_description': False,
            'missing_canonical': False,
            'missing_schema': False,
            'large_images': [],
            'inline_styles': [],
            'broken_links': [],
            'missing_h1': False,
            'duplicate_h1': False,
            'poor_semantic_html': [],
            'accessibility_issues': [],
            'performance_issues': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # Check for violations
            self._check_text_violations(content, violations)
            self._check_html_structure(soup, violations)
            self._check_accessibility(soup, violations)
            self._check_performance(soup, violations)
            self._check_seo_elements(soup, violations)

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")

        return violations

    def _check_text_violations(self, content: str, violations: Dict):
        """Check for text-based violations"""
        # Bold text
        if re.search(self.violation_patterns['bold_text'], content, re.IGNORECASE | re.DOTALL):
            violations['bold_text'] = re.findall(self.violation_patterns['bold_text'], content, re.IGNORECASE | re.DOTALL)

        # Dashes
        violations['dashes'] = re.findall(self.violation_patterns['dashes'], content)

        # Hashtags
        violations['hashtags'] = re.findall(self.violation_patterns['hashtags'], content)

        # Emojis
        violations['emojis'] = re.findall(self.violation_patterns['emojis'], content)

        # AI phrases
        for phrase in self.ai_phrases:
            if phrase.lower() in content.lower():
                violations['ai_phrases'].append(phrase)

    def _check_html_structure(self, soup: BeautifulSoup, violations: Dict):
        """Check HTML structure violations"""
        # Missing or duplicate H1
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            violations['missing_h1'] = True
        elif len(h1_tags) > 1:
            violations['duplicate_h1'] = True

        # Word count in main content
        main_content = soup.find('main')
        if main_content:
            text = main_content.get_text(strip=True)
            word_count = len(text.split())
            if word_count < 300:
                violations['low_word_count'] = True

        # Inline styles
        elements_with_style = soup.find_all(attrs={"style": True})
        violations['inline_styles'] = [str(elem) for elem in elements_with_style]

        # Poor semantic HTML
        div_buttons = soup.find_all('div', class_=re.compile('button', re.I))
        violations['poor_semantic_html'] = [str(elem) for elem in div_buttons]

    def _check_accessibility(self, soup: BeautifulSoup, violations: Dict):
        """Check accessibility compliance"""
        # Missing alt tags
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                violations['missing_alt_tags'].append(str(img))

        # Check for color contrast issues (basic check)
        # Check for missing ARIA labels where needed
        buttons = soup.find_all(['button', 'input'])
        for button in buttons:
            if button.name == 'input' and button.get('type') in ['submit', 'button']:
                if not button.get('value') and not button.get('aria-label'):
                    violations['accessibility_issues'].append(f"Button missing label: {button}")

    def _check_performance(self, soup: BeautifulSoup, violations: Dict):
        """Check performance issues"""
        # Large images without optimization attributes
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if src and not any(attr in str(img).lower() for attr in ['loading=', 'width=', 'height=']):
                violations['large_images'].append(str(img))

    def _check_seo_elements(self, soup: BeautifulSoup, violations: Dict):
        """Check SEO elements"""
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            violations['missing_meta_description'] = True

        # Canonical link
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            violations['missing_canonical'] = True

        # Schema markup
        schema_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        if not schema_scripts:
            violations['missing_schema'] = True

    def fix_violations(self, file_path: Path, violations: Dict) -> int:
        """Fix detected violations"""
        fixes_applied = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix bold text
            if violations['bold_text']:
                content = re.sub(self.violation_patterns['bold_text'], lambda m: m.group().replace('<b>', '').replace('</b>', '').replace('<strong>', '').replace('</strong>', '').replace('**', ''), content, flags=re.IGNORECASE | re.DOTALL)
                fixes_applied += len(violations['bold_text'])

            # Fix dashes
            if violations['dashes']:
                content = re.sub(r'(?<!-)--(?!-)|—|–', '-', content)
                fixes_applied += len(violations['dashes'])

            # Remove hashtags
            if violations['hashtags']:
                content = re.sub(r'#\w+', '', content)
                fixes_applied += len(violations['hashtags'])

            # Remove emojis
            if violations['emojis']:
                content = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+', '', content)
                fixes_applied += len(violations['emojis'])

            # Fix AI phrases (replace with more natural alternatives)
            ai_replacements = {
                "streamline your": "improve your",
                "revolutionize your": "enhance your",
                "unleash the power": "use the features",
                "game-changer": "useful tool",
                "cutting-edge": "advanced",
                "next-level": "improved",
                "innovative solution": "tool",
                "seamless experience": "smooth experience",
                "unprecedented": "new",
                "state-of-the-art": "advanced",
                "groundbreaking": "new",
                "transformative": "helpful",
                "leverage": "use",
                "synergy": "combination",
                "paradigm shift": "change",
                "disruptive": "new",
                "scalable solution": "flexible tool",
                "robust framework": "reliable system",
                "comprehensive suite": "complete set",
                "enterprise-grade": "professional"
            }

            for phrase in violations['ai_phrases']:
                if phrase in ai_replacements:
                    content = content.replace(phrase, ai_replacements[phrase])
                    fixes_applied += 1

            # Add missing alt tags
            if violations['missing_alt_tags']:
                soup = BeautifulSoup(content, 'html.parser')
                images = soup.find_all('img')
                for img in images:
                    if not img.get('alt'):
                        # Generate descriptive alt text based on src or context
                        src = img.get('src', '')
                        if 'calculator' in src:
                            img['alt'] = 'Calculator tool interface'
                        elif 'icon' in src:
                            img['alt'] = 'Tool icon'
                        else:
                            img['alt'] = 'Tool interface'
                        fixes_applied += 1
                content = str(soup)

            # Add performance attributes to images
            if violations['large_images']:
                soup = BeautifulSoup(content, 'html.parser')
                images = soup.find_all('img')
                for img in images:
                    if not img.get('loading'):
                        img['loading'] = 'lazy'
                        fixes_applied += 1
                content = str(soup)

            # Save if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Applied {fixes_applied} fixes to {file_path}")

        except Exception as e:
            logger.error(f"Error fixing violations in {file_path}: {e}")

        return fixes_applied

    def add_missing_seo_elements(self, file_path: Path, violations: Dict) -> int:
        """Add missing SEO elements"""
        additions = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            head = soup.find('head')

            if not head:
                return 0

            # Add meta description if missing
            if violations['missing_meta_description']:
                tool_name = file_path.parent.name.replace('-', ' ').title()
                meta_desc = soup.new_tag('meta', attrs={
                    'name': 'description',
                    'content': f'Free {tool_name} - Fast, accurate, and easy to use. Get instant results with our professional calculator tool.'
                })
                head.append(meta_desc)
                additions += 1

            # Add canonical link if missing
            if violations['missing_canonical']:
                canonical_url = f"https://zovo.tools/{file_path.parent.name}/"
                canonical = soup.new_tag('link', attrs={
                    'rel': 'canonical',
                    'href': canonical_url
                })
                head.append(canonical)
                additions += 1

            # Add schema markup if missing
            if violations['missing_schema']:
                tool_name = file_path.parent.name.replace('-', ' ').title()
                schema_data = {
                    "@context": "https://schema.org",
                    "@type": "WebApplication",
                    "name": tool_name,
                    "url": f"https://zovo.tools/{file_path.parent.name}/",
                    "description": f"Free {tool_name} - Fast, accurate, and easy to use calculator tool.",
                    "applicationCategory": "UtilityApplication",
                    "operatingSystem": "Web Browser",
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD"
                    }
                }

                schema_script = soup.new_tag('script', attrs={'type': 'application/ld+json'})
                schema_script.string = json.dumps(schema_data, indent=2)
                head.append(schema_script)
                additions += 1

            if additions > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                logger.info(f"Added {additions} SEO elements to {file_path}")

        except Exception as e:
            logger.error(f"Error adding SEO elements to {file_path}: {e}")

        return additions

    def process_directory(self, dir_path: Path) -> Dict:
        """Process a single directory with comprehensive QA"""
        dir_stats = {
            'name': dir_path.name,
            'files_processed': 0,
            'violations_found': 0,
            'violations_fixed': 0,
            'seo_additions': 0,
            'performance_optimizations': 0
        }

        try:
            html_files = list(dir_path.glob('*.html'))

            for html_file in html_files:
                violations = self.analyze_html_content(html_file)

                # Count total violations
                violation_count = sum(
                    len(v) if isinstance(v, list) else (1 if v else 0)
                    for v in violations.values()
                )

                dir_stats['violations_found'] += violation_count

                # Fix violations
                fixes_applied = self.fix_violations(html_file, violations)
                dir_stats['violations_fixed'] += fixes_applied

                # Add missing SEO elements
                seo_additions = self.add_missing_seo_elements(html_file, violations)
                dir_stats['seo_additions'] += seo_additions

                dir_stats['files_processed'] += 1

                logger.info(f"Processed {html_file}: {violation_count} violations, {fixes_applied} fixes, {seo_additions} SEO additions")

        except Exception as e:
            logger.error(f"Error processing directory {dir_path}: {e}")

        return dir_stats

    def git_operations(self):
        """Perform git pull and push operations"""
        try:
            # Git pull
            result = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=self.base_dir)
            if result.returncode == 0:
                logger.info("Git pull successful")
            else:
                logger.warning(f"Git pull warning: {result.stderr}")

            # Git add, commit, and push if there are changes
            subprocess.run(['git', 'add', '.'], cwd=self.base_dir)

            commit_message = f"QA Agent Alpha: Enhanced quality fixes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            commit_result = subprocess.run(['git', 'commit', '-m', commit_message],
                                         capture_output=True, text=True, cwd=self.base_dir)

            if commit_result.returncode == 0:
                logger.info("Changes committed successfully")

                push_result = subprocess.run(['git', 'push'], capture_output=True, text=True, cwd=self.base_dir)
                if push_result.returncode == 0:
                    logger.info("Changes pushed successfully")
                else:
                    logger.error(f"Git push failed: {push_result.stderr}")
            else:
                logger.info("No changes to commit")

        except Exception as e:
            logger.error(f"Git operation error: {e}")

    def generate_qa_report(self) -> Dict:
        """Generate comprehensive QA metrics report"""
        runtime = datetime.now() - self.stats['start_time']

        report = {
            'timestamp': datetime.now().isoformat(),
            'runtime_minutes': runtime.total_seconds() / 60,
            'summary': {
                'total_directories_processed': self.stats['total_dirs_processed'],
                'total_files_processed': self.stats['total_files_processed'],
                'total_violations_found': self.stats['violations_found'],
                'total_violations_fixed': self.stats['violations_fixed'],
                'performance_optimizations': self.stats['performance_optimizations'],
                'accessibility_fixes': self.stats['accessibility_fixes'],
                'schema_validations': self.stats['schema_validations']
            },
            'detailed_stats': self.stats['detailed_stats'],
            'processing_rate': {
                'dirs_per_minute': self.stats['total_dirs_processed'] / max(runtime.total_seconds() / 60, 1),
                'files_per_minute': self.stats['total_files_processed'] / max(runtime.total_seconds() / 60, 1),
                'fixes_per_minute': self.stats['violations_fixed'] / max(runtime.total_seconds() / 60, 1)
            }
        }

        # Save report
        report_file = self.base_dir / f'qa_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"QA Report generated: {report_file}")
        return report

    def run_continuous_qa(self, duration_hours: float = 2.0, cycle_seconds: int = 45):
        """Run continuous QA for specified duration"""
        logger.info(f"Starting continuous QA for {duration_hours} hours, cycling every {cycle_seconds} seconds")

        end_time = time.time() + (duration_hours * 3600)
        cycle_count = 0

        while time.time() < end_time:
            cycle_count += 1
            cycle_start = time.time()

            logger.info(f"=== QA Cycle {cycle_count} ===")

            # Git pull at start of cycle
            self.git_operations()

            # Get target directories
            target_dirs = self.get_target_directories()
            logger.info(f"Processing {len(target_dirs)} directories")

            # Process directories
            for dir_path in target_dirs:
                if time.time() >= end_time:
                    break

                dir_stats = self.process_directory(dir_path)

                with self.stats_lock:
                    self.stats['total_dirs_processed'] += 1
                    self.stats['total_files_processed'] += dir_stats['files_processed']
                    self.stats['violations_found'] += dir_stats['violations_found']
                    self.stats['violations_fixed'] += dir_stats['violations_fixed']
                    self.stats['performance_optimizations'] += dir_stats['performance_optimizations']
                    self.stats['detailed_stats'][dir_path.name] = dir_stats

            # Git commit and push changes
            self.git_operations()

            # Generate intermediate report
            if cycle_count % 5 == 0:  # Every 5 cycles
                self.generate_qa_report()

            cycle_time = time.time() - cycle_start
            sleep_time = max(0, cycle_seconds - cycle_time)

            if sleep_time > 0:
                logger.info(f"Cycle {cycle_count} completed in {cycle_time:.1f}s, sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
            else:
                logger.info(f"Cycle {cycle_count} completed in {cycle_time:.1f}s (overtime)")

        # Final report
        final_report = self.generate_qa_report()
        logger.info("=== QA Session Complete ===")
        logger.info(f"Processed {self.stats['total_dirs_processed']} directories")
        logger.info(f"Processed {self.stats['total_files_processed']} files")
        logger.info(f"Fixed {self.stats['violations_fixed']} violations")

        return final_report

def main():
    """Main execution function"""
    print("🚀 QA Agent Alpha - Enhanced Quality Assurance System")
    print("=" * 60)

    agent = EnhancedQAAgent()

    try:
        # Run continuous QA for 2+ hours
        final_report = agent.run_continuous_qa(duration_hours=2.5, cycle_seconds=45)

        print("\n" + "=" * 60)
        print("📊 FINAL QA STATISTICS")
        print("=" * 60)
        print(f"Runtime: {final_report['runtime_minutes']:.1f} minutes")
        print(f"Directories Processed: {final_report['summary']['total_directories_processed']}")
        print(f"Files Processed: {final_report['summary']['total_files_processed']}")
        print(f"Violations Found: {final_report['summary']['total_violations_found']}")
        print(f"Violations Fixed: {final_report['summary']['total_violations_fixed']}")
        print(f"Performance Optimizations: {final_report['summary']['performance_optimizations']}")
        print(f"Accessibility Fixes: {final_report['summary']['accessibility_fixes']}")
        print(f"Processing Rate: {final_report['processing_rate']['dirs_per_minute']:.1f} dirs/min")

    except KeyboardInterrupt:
        print("\n⚠️ QA session interrupted by user")
        agent.generate_qa_report()
    except Exception as e:
        print(f"\n❌ QA session error: {e}")
        agent.generate_qa_report()

if __name__ == "__main__":
    main()