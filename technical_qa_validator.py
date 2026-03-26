#!/usr/bin/env python3
"""
Technical QA Validator for F-M Tools
Comprehensive validation suite focusing on technical excellence standards
"""

import os
import re
import json
import time
import subprocess
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mike/zovo-workspaces/zovo-tools/qa_technical.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TechnicalQAValidator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.issues = []
        self.fixes_applied = []
        self.tools_processed = 0

    def validate_html_structure(self, html_content, tool_name):
        """Validate HTML structure and W3C compliance"""
        issues = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Check for DOCTYPE
            if not str(html_content).strip().startswith('<!DOCTYPE html>'):
                issues.append(f"{tool_name}: Missing DOCTYPE declaration")

            # Check for required meta tags
            required_metas = ['charset', 'viewport', 'description']
            for meta in required_metas:
                if meta == 'charset':
                    if not soup.find('meta', charset=True):
                        issues.append(f"{tool_name}: Missing charset meta tag")
                elif meta == 'viewport':
                    if not soup.find('meta', attrs={'name': 'viewport'}):
                        issues.append(f"{tool_name}: Missing viewport meta tag")
                elif meta == 'description':
                    if not soup.find('meta', attrs={'name': 'description'}):
                        issues.append(f"{tool_name}: Missing description meta tag")

            # Check for semantic HTML structure
            if not soup.find('main'):
                issues.append(f"{tool_name}: Missing <main> semantic element")
            if not soup.find('h1'):
                issues.append(f"{tool_name}: Missing H1 tag")

            # Check for duplicate IDs
            ids = [elem.get('id') for elem in soup.find_all(id=True)]
            duplicates = set([x for x in ids if ids.count(x) > 1])
            if duplicates:
                issues.append(f"{tool_name}: Duplicate IDs found: {duplicates}")

        except Exception as e:
            issues.append(f"{tool_name}: HTML parsing error: {str(e)}")

        return issues

    def validate_css_optimization(self, css_content, tool_name):
        """Validate CSS structure and optimization opportunities"""
        issues = []

        try:
            # Check for unused vendor prefixes
            vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
            for prefix in vendor_prefixes:
                if prefix in css_content:
                    # Check if modern property exists
                    property_name = re.search(rf'{prefix}([a-z-]+)', css_content)
                    if property_name:
                        modern_prop = property_name.group(1)
                        if modern_prop not in css_content.replace(prefix + modern_prop, ''):
                            issues.append(f"{tool_name}: Missing modern property for {prefix}{modern_prop}")

            # Check for color accessibility
            color_patterns = re.findall(r'color:\s*([^;]+)', css_content)
            for color in color_patterns:
                if color.strip() in ['#fff', '#ffffff', 'white'] and 'background' not in css_content:
                    issues.append(f"{tool_name}: White text may have accessibility issues")

            # Check for minification opportunities
            if len(css_content) > 1000 and '  ' in css_content:
                issues.append(f"{tool_name}: CSS could be minified")

        except Exception as e:
            issues.append(f"{tool_name}: CSS validation error: {str(e)}")

        return issues

    def validate_javascript_errors(self, js_content, tool_name):
        """Validate JavaScript for common errors and best practices"""
        issues = []

        try:
            # Check for console.log statements
            if 'console.log' in js_content:
                issues.append(f"{tool_name}: Console.log statements should be removed in production")

            # Check for var usage instead of let/const
            if re.search(r'\bvar\s+', js_content):
                issues.append(f"{tool_name}: Consider using let/const instead of var")

            # Check for missing semicolons
            lines = js_content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line and not line.endswith((';', '{', '}', ':', ',')):
                    if re.search(r'(return|break|continue|throw)\s', line):
                        issues.append(f"{tool_name}: Missing semicolon on line {i+1}")

            # Check for jQuery usage
            if '$(' in js_content or 'jQuery' in js_content:
                issues.append(f"{tool_name}: Consider modern vanilla JS instead of jQuery")

        except Exception as e:
            issues.append(f"{tool_name}: JavaScript validation error: {str(e)}")

        return issues

    def validate_json_ld_schema(self, html_content, tool_name):
        """Validate JSON-LD schema markup"""
        issues = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            json_ld_scripts = soup.find_all('script', type='application/ld+json')

            if not json_ld_scripts:
                issues.append(f"{tool_name}: Missing JSON-LD schema markup")
            else:
                for script in json_ld_scripts:
                    try:
                        schema_data = json.loads(script.string)

                        # Validate required schema.org properties
                        if '@type' not in schema_data:
                            issues.append(f"{tool_name}: JSON-LD missing @type")
                        if 'name' not in schema_data:
                            issues.append(f"{tool_name}: JSON-LD missing name property")
                        if 'description' not in schema_data:
                            issues.append(f"{tool_name}: JSON-LD missing description property")

                    except json.JSONDecodeError:
                        issues.append(f"{tool_name}: Invalid JSON-LD syntax")

        except Exception as e:
            issues.append(f"{tool_name}: Schema validation error: {str(e)}")

        return issues

    def validate_meta_tags(self, html_content, tool_name):
        """Validate meta tag completeness and optimization"""
        issues = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Check OpenGraph tags
            og_tags = ['og:title', 'og:description', 'og:type', 'og:url', 'og:image']
            for tag in og_tags:
                if not soup.find('meta', property=tag):
                    issues.append(f"{tool_name}: Missing OpenGraph tag: {tag}")

            # Check Twitter Card tags
            twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description']
            for tag in twitter_tags:
                if not soup.find('meta', name=tag):
                    issues.append(f"{tool_name}: Missing Twitter Card tag: {tag}")

            # Check canonical URL
            if not soup.find('link', rel='canonical'):
                issues.append(f"{tool_name}: Missing canonical URL")

            # Validate meta description length
            description_tag = soup.find('meta', attrs={'name': 'description'})
            if description_tag:
                description = description_tag.get('content', '')
                if len(description) < 120 or len(description) > 160:
                    issues.append(f"{tool_name}: Meta description length should be 120-160 characters (current: {len(description)})")

        except Exception as e:
            issues.append(f"{tool_name}: Meta tag validation error: {str(e)}")

        return issues

    def validate_images(self, html_content, tool_name):
        """Validate image optimization and accessibility"""
        issues = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            images = soup.find_all('img')

            for img in images:
                # Check alt text
                if not img.get('alt'):
                    issues.append(f"{tool_name}: Image missing alt attribute: {img.get('src', 'unknown')}")

                # Check loading attribute
                if not img.get('loading'):
                    issues.append(f"{tool_name}: Image missing loading attribute: {img.get('src', 'unknown')}")

                # Check width/height attributes
                if not (img.get('width') and img.get('height')):
                    issues.append(f"{tool_name}: Image missing width/height attributes: {img.get('src', 'unknown')}")

        except Exception as e:
            issues.append(f"{tool_name}: Image validation error: {str(e)}")

        return issues

    def validate_performance(self, html_content, tool_name):
        """Validate performance optimization opportunities"""
        issues = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Check for external scripts without async/defer
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                if not (script.get('async') or script.get('defer')):
                    issues.append(f"{tool_name}: External script should use async/defer: {script.get('src')}")

            # Check for critical CSS inlining
            external_css = soup.find_all('link', rel='stylesheet')
            if len(external_css) > 3:
                issues.append(f"{tool_name}: Consider inlining critical CSS ({len(external_css)} external stylesheets)")

            # Check for preload opportunities
            if not soup.find('link', rel='preload'):
                issues.append(f"{tool_name}: Consider preloading critical resources")

        except Exception as e:
            issues.append(f"{tool_name}: Performance validation error: {str(e)}")

        return issues

    def fix_html_issues(self, file_path, issues):
        """Apply automatic fixes for common HTML issues"""
        fixes = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # Add missing viewport meta tag
            if 'Missing viewport meta tag' in str(issues):
                if '<meta charset="UTF-8">' in content and 'viewport' not in content:
                    content = content.replace(
                        '<meta charset="UTF-8">',
                        '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
                    )
                    fixes.append("Added viewport meta tag")
                    modified = True

            # Add loading="lazy" to images
            if 'Image missing loading attribute' in str(issues):
                content = re.sub(
                    r'(<img(?![^>]*loading=)[^>]*?)>',
                    r'\1 loading="lazy">',
                    content
                )
                if 'loading="lazy"' in content:
                    fixes.append("Added lazy loading to images")
                    modified = True

            # Add alt attributes to images missing them
            if 'Image missing alt attribute' in str(issues):
                content = re.sub(
                    r'(<img(?![^>]*alt=)[^>]*?)>',
                    r'\1 alt="">',
                    content
                )
                fixes.append("Added empty alt attributes to decorative images")
                modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            logger.error(f"Error fixing HTML issues in {file_path}: {str(e)}")

        return fixes

    def validate_tool(self, tool_dir):
        """Validate a single tool directory"""
        tool_name = tool_dir.name
        html_file = tool_dir / 'index.html'

        if not html_file.exists():
            self.issues.append(f"{tool_name}: No index.html found")
            return

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Run all validations
            all_issues = []
            all_issues.extend(self.validate_html_structure(html_content, tool_name))
            all_issues.extend(self.validate_json_ld_schema(html_content, tool_name))
            all_issues.extend(self.validate_meta_tags(html_content, tool_name))
            all_issues.extend(self.validate_images(html_content, tool_name))
            all_issues.extend(self.validate_performance(html_content, tool_name))

            # Check for inline CSS/JS to validate
            soup = BeautifulSoup(html_content, 'html.parser')

            # Validate CSS
            style_tags = soup.find_all('style')
            for style in style_tags:
                if style.string:
                    all_issues.extend(self.validate_css_optimization(style.string, tool_name))

            # Validate JavaScript
            script_tags = soup.find_all('script', src=False)
            for script in script_tags:
                if script.string and script.get('type') != 'application/ld+json':
                    all_issues.extend(self.validate_javascript_errors(script.string, tool_name))

            # Apply fixes
            fixes = self.fix_html_issues(html_file, all_issues)
            self.fixes_applied.extend(fixes)

            # Store issues
            self.issues.extend(all_issues)
            self.tools_processed += 1

            if all_issues:
                logger.warning(f"{tool_name}: Found {len(all_issues)} issues")
            else:
                logger.info(f"{tool_name}: No issues found")

        except Exception as e:
            logger.error(f"Error validating {tool_name}: {str(e)}")
            self.issues.append(f"{tool_name}: Validation error: {str(e)}")

    def generate_report(self):
        """Generate comprehensive technical QA report"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        report_file = self.base_dir / f'technical_qa_report_{timestamp}.json'

        report = {
            'timestamp': timestamp,
            'tools_processed': self.tools_processed,
            'total_issues': len(self.issues),
            'fixes_applied': len(self.fixes_applied),
            'issues_by_category': {},
            'detailed_issues': self.issues,
            'applied_fixes': self.fixes_applied
        }

        # Categorize issues
        categories = {
            'HTML Structure': ['DOCTYPE', 'Missing', 'semantic', 'Duplicate'],
            'CSS Optimization': ['vendor prefixes', 'minified', 'accessibility'],
            'JavaScript': ['console.log', 'var', 'semicolon', 'jQuery'],
            'Schema Markup': ['JSON-LD', 'schema'],
            'Meta Tags': ['OpenGraph', 'Twitter', 'canonical', 'description'],
            'Images': ['alt attribute', 'loading', 'width/height'],
            'Performance': ['async/defer', 'CSS', 'preload']
        }

        for category, keywords in categories.items():
            count = sum(1 for issue in self.issues if any(keyword in issue for keyword in keywords))
            report['issues_by_category'][category] = count

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report generated: {report_file}")
        return report

def main():
    """Main QA validation loop"""
    validator = TechnicalQAValidator('/Users/mike/zovo-workspaces/zovo-tools')

    # Get F-M tools
    fm_tools = []
    for item in validator.base_dir.iterdir():
        if item.is_dir() and re.match(r'^[f-mF-M]', item.name):
            fm_tools.append(item)

    logger.info(f"Starting technical QA validation for {len(fm_tools)} F-M tools")

    # Process tools in batches
    batch_size = 10
    for i in range(0, len(fm_tools), batch_size):
        batch = fm_tools[i:i + batch_size]

        logger.info(f"Processing batch {i//batch_size + 1}: {len(batch)} tools")

        for tool_dir in batch:
            validator.validate_tool(tool_dir)

        # Generate interim report every batch
        if (i + batch_size) % 50 == 0:
            report = validator.generate_report()
            logger.info(f"Interim report: {report['tools_processed']} tools, {report['total_issues']} issues, {report['fixes_applied']} fixes")

    # Generate final report
    final_report = validator.generate_report()

    logger.info("=== TECHNICAL QA VALIDATION COMPLETE ===")
    logger.info(f"Tools processed: {final_report['tools_processed']}")
    logger.info(f"Total issues found: {final_report['total_issues']}")
    logger.info(f"Fixes applied: {final_report['fixes_applied']}")
    logger.info("Issues by category:")
    for category, count in final_report['issues_by_category'].items():
        if count > 0:
            logger.info(f"  {category}: {count}")

if __name__ == "__main__":
    main()