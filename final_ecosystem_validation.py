#!/usr/bin/env python3
"""
Zovo Ecosystem Final Validation - Agent 5
Comprehensive quality validation and reporting system
"""

import os
import re
import json
import time
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
import subprocess

class ZovoEcosystemValidator:
    def __init__(self, base_path="/Users/mike/zovo-workspaces/zovo-tools"):
        self.base_path = Path(base_path)
        self.results = {
            'tools': {},
            'articles': {},
            'global_metrics': {},
            'quality_scores': {},
            'violations': [],
            'summary': {}
        }
        self.start_time = time.time()

    def log(self, message):
        elapsed = time.time() - self.start_time
        print(f"[{elapsed:6.1f}s] {message}")

    def validate_canonical_urls(self, html_content, expected_path):
        """Validate canonical URL compliance"""
        soup = BeautifulSoup(html_content, 'html.parser')
        canonical = soup.find('link', rel='canonical')

        if not canonical:
            return {'compliant': False, 'error': 'No canonical URL found'}

        href = canonical.get('href', '')
        expected_url = f"https://tools.zovo.one/{expected_path}/"

        return {
            'compliant': href == expected_url,
            'found': href,
            'expected': expected_url
        }

    def validate_schema_markup(self, html_content):
        """Validate Schema.org markup presence and quality"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for JSON-LD structured data
        json_ld = soup.find_all('script', type='application/ld+json')

        schema_score = 0
        schema_types = []

        for script in json_ld:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and '@type' in data:
                    schema_types.append(data['@type'])
                    schema_score += 1
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@type' in item:
                            schema_types.append(item['@type'])
                            schema_score += 1
            except:
                continue

        return {
            'has_schema': len(json_ld) > 0,
            'schema_count': len(json_ld),
            'schema_types': schema_types,
            'schema_score': schema_score
        }

    def validate_anti_ai_compliance(self, html_content):
        """Check for AI-related violations"""
        violations = []

        # Check for bold tags
        bold_tags = re.findall(r'<b\b[^>]*>|</b>', html_content)
        if bold_tags:
            violations.append(f"Found {len(bold_tags)} bold tags")

        # Check for em-dashes
        em_dashes = re.findall(r'—', html_content)
        if em_dashes:
            violations.append(f"Found {len(em_dashes)} em-dashes")

        # Check for AI mentions
        ai_mentions = re.findall(r'\b(?:AI|artificial intelligence|machine learning|Claude|GPT|ChatGPT)\b',
                                html_content, re.IGNORECASE)
        if ai_mentions:
            violations.append(f"Found {len(ai_mentions)} AI mentions")

        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }

    def validate_zovo_navbar(self, html_content):
        """Check for Zovo navbar presence"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Look for Zovo navbar indicators
        navbar_indicators = [
            soup.find('nav'),
            soup.find(class_=re.compile(r'navbar', re.I)),
            soup.find(string=re.compile(r'zovo', re.I)),
            soup.find('a', href=re.compile(r'zovo\.one', re.I))
        ]

        has_navbar = any(indicator for indicator in navbar_indicators)

        return {'has_navbar': has_navbar}

    def count_words(self, html_content):
        """Count meaningful words in content"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script, style, nav elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()

        text = soup.get_text()
        words = len(re.findall(r'\b\w+\b', text))

        return words

    def validate_seo_basics(self, html_content):
        """Validate basic SEO elements"""
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        h1 = soup.find('h1')

        return {
            'has_title': title is not None,
            'title_length': len(title.get_text()) if title else 0,
            'has_meta_description': meta_desc is not None,
            'meta_desc_length': len(meta_desc.get('content', '')) if meta_desc else 0,
            'has_h1': h1 is not None,
            'h1_text': h1.get_text() if h1 else ''
        }

    def validate_single_page(self, html_file_path, page_type='tool'):
        """Validate a single HTML page"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Extract relative path for canonical URL
            rel_path = str(html_file_path.relative_to(self.base_path)).replace('/index.html', '')

            validation = {
                'path': str(html_file_path),
                'relative_path': rel_path,
                'page_type': page_type,
                'file_size': html_file_path.stat().st_size,
                'word_count': self.count_words(html_content),
                'canonical': self.validate_canonical_urls(html_content, rel_path),
                'schema': self.validate_schema_markup(html_content),
                'anti_ai': self.validate_anti_ai_compliance(html_content),
                'navbar': self.validate_zovo_navbar(html_content),
                'seo': self.validate_seo_basics(html_content)
            }

            return validation

        except Exception as e:
            return {'path': str(html_file_path), 'error': str(e)}

    def scan_ecosystem(self):
        """Scan entire ecosystem"""
        self.log("Starting comprehensive ecosystem scan...")

        total_pages = 0

        # Scan tools
        self.log("Scanning tool directories...")
        tool_count = 0
        for item in self.base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
                index_file = item / 'index.html'
                if index_file.exists():
                    validation = self.validate_single_page(index_file, 'tool')
                    self.results['tools'][item.name] = validation
                    tool_count += 1

                    if tool_count % 50 == 0:
                        self.log(f"Processed {tool_count} tools...")

        total_pages += tool_count
        self.log(f"Completed tool scan: {tool_count} tools")

        # Scan articles
        self.log("Scanning article directories...")
        articles_dir = self.base_path / 'articles'
        article_count = 0

        if articles_dir.exists():
            for item in articles_dir.iterdir():
                if item.is_dir():
                    index_file = item / 'index.html'
                    if index_file.exists():
                        validation = self.validate_single_page(index_file, 'article')
                        self.results['articles'][item.name] = validation
                        article_count += 1

        total_pages += article_count
        self.log(f"Completed article scan: {article_count} articles")

        self.results['summary']['total_pages'] = total_pages
        self.results['summary']['total_tools'] = tool_count
        self.results['summary']['total_articles'] = article_count

    def calculate_metrics(self):
        """Calculate comprehensive metrics"""
        self.log("Calculating ecosystem metrics...")

        all_pages = list(self.results['tools'].values()) + list(self.results['articles'].values())

        # Word count metrics
        word_counts = [page.get('word_count', 0) for page in all_pages if 'word_count' in page]
        total_words = sum(word_counts)
        avg_words = total_words / len(word_counts) if word_counts else 0

        # Canonical compliance
        canonical_compliant = sum(1 for page in all_pages if page.get('canonical', {}).get('compliant', False))
        canonical_rate = (canonical_compliant / len(all_pages) * 100) if all_pages else 0

        # Schema markup coverage
        has_schema = sum(1 for page in all_pages if page.get('schema', {}).get('has_schema', False))
        schema_rate = (has_schema / len(all_pages) * 100) if all_pages else 0

        # Anti-AI compliance
        anti_ai_compliant = sum(1 for page in all_pages if page.get('anti_ai', {}).get('compliant', False))
        anti_ai_rate = (anti_ai_compliant / len(all_pages) * 100) if all_pages else 0

        # Navbar presence
        has_navbar = sum(1 for page in all_pages if page.get('navbar', {}).get('has_navbar', False))
        navbar_rate = (has_navbar / len(all_pages) * 100) if all_pages else 0

        # SEO compliance
        good_seo = sum(1 for page in all_pages
                      if (page.get('seo', {}).get('has_title', False) and
                          page.get('seo', {}).get('has_meta_description', False) and
                          page.get('seo', {}).get('has_h1', False)))
        seo_rate = (good_seo / len(all_pages) * 100) if all_pages else 0

        self.results['global_metrics'] = {
            'total_word_count': total_words,
            'average_words_per_page': avg_words,
            'canonical_compliance_rate': canonical_rate,
            'schema_markup_coverage': schema_rate,
            'anti_ai_compliance_rate': anti_ai_rate,
            'navbar_presence_rate': navbar_rate,
            'seo_compliance_rate': seo_rate,
            'pages_over_2000_words': sum(1 for wc in word_counts if wc >= 2000),
            'pages_under_1000_words': sum(1 for wc in word_counts if wc < 1000)
        }

    def generate_quality_report(self):
        """Generate comprehensive quality report"""
        self.log("Generating quality report...")

        metrics = self.results['global_metrics']

        # Calculate overall quality score
        quality_factors = [
            ('Canonical URLs', metrics['canonical_compliance_rate'], 20),
            ('Schema Markup', metrics['schema_markup_coverage'], 20),
            ('Anti-AI Compliance', metrics['anti_ai_compliance_rate'], 25),
            ('SEO Compliance', metrics['seo_compliance_rate'], 20),
            ('Content Depth', min(100, metrics['average_words_per_page'] / 20), 15)
        ]

        total_score = sum(score * weight / 100 for _, score, weight in quality_factors)

        self.results['quality_scores'] = {
            'overall_score': total_score,
            'factor_scores': quality_factors,
            'grade': self.score_to_grade(total_score)
        }

    def score_to_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 95: return 'A+'
        elif score >= 90: return 'A'
        elif score >= 85: return 'B+'
        elif score >= 80: return 'B'
        elif score >= 75: return 'C+'
        elif score >= 70: return 'C'
        else: return 'F'

    def save_results(self):
        """Save validation results"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = self.base_path / f"ecosystem_validation_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        self.log(f"Results saved to {results_file}")
        return results_file

    def print_executive_summary(self):
        """Print executive summary"""
        print("\n" + "="*80)
        print("ZOVO ECOSYSTEM FINAL VALIDATION REPORT")
        print("="*80)

        summary = self.results['summary']
        metrics = self.results['global_metrics']
        quality = self.results['quality_scores']

        print(f"\nECOSYSTEM OVERVIEW:")
        print(f"  Total Pages: {summary['total_pages']:,}")
        print(f"  Tools: {summary['total_tools']:,}")
        print(f"  Articles: {summary['total_articles']:,}")
        print(f"  Total Words: {metrics['total_word_count']:,}")
        print(f"  Average Words/Page: {metrics['average_words_per_page']:,.0f}")

        print(f"\nQUALITY METRICS:")
        print(f"  Overall Score: {quality['overall_score']:.1f}/100 (Grade: {quality['grade']})")
        print(f"  Canonical URL Compliance: {metrics['canonical_compliance_rate']:.1f}%")
        print(f"  Schema Markup Coverage: {metrics['schema_markup_coverage']:.1f}%")
        print(f"  Anti-AI Compliance: {metrics['anti_ai_compliance_rate']:.1f}%")
        print(f"  SEO Compliance: {metrics['seo_compliance_rate']:.1f}%")
        print(f"  Navbar Presence: {metrics['navbar_presence_rate']:.1f}%")

        print(f"\nCONTENT DEPTH:")
        print(f"  Pages ≥2000 words: {metrics['pages_over_2000_words']:,}")
        print(f"  Pages <1000 words: {metrics['pages_under_1000_words']:,}")

        elapsed = time.time() - self.start_time
        print(f"\nValidation completed in {elapsed:.1f} seconds")
        print("="*80)

    def run_full_validation(self):
        """Execute complete validation process"""
        self.scan_ecosystem()
        self.calculate_metrics()
        self.generate_quality_report()
        results_file = self.save_results()
        self.print_executive_summary()
        return results_file

if __name__ == "__main__":
    validator = ZovoEcosystemValidator()
    validator.run_full_validation()