#!/usr/bin/env python3
"""
Content QA Analyzer for Zovo Tools
Focuses on tools N-S for comprehensive content quality analysis
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess
import time
from datetime import datetime

class ContentQAAnalyzer:
    def __init__(self, tools_dir):
        self.tools_dir = tools_dir
        self.results = []

    def get_n_s_tools(self):
        """Get all tool directories starting with N-S"""
        tools = []
        for item in os.listdir(self.tools_dir):
            if (os.path.isdir(os.path.join(self.tools_dir, item)) and
                item[0].lower() in 'nopqrs'):
                tools.append(item)
        return sorted(tools)

    def analyze_html_content(self, filepath):
        """Analyze HTML content for quality metrics"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # Basic metrics
            word_count = len(content.split())

            # Count headings
            h1_count = len(soup.find_all('h1'))
            h2_count = len(soup.find_all('h2'))
            h3_count = len(soup.find_all('h3'))

            # Check for FAQ section
            has_faq = bool(soup.find(text=re.compile('FAQ|frequently asked', re.I)))

            # Check for meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            has_meta_desc = bool(meta_desc and meta_desc.get('content', '').strip())

            # Check for schema markup
            has_schema = bool(soup.find('script', type='application/ld+json'))

            # Check for table of contents
            has_toc = bool(soup.find(class_=re.compile('toc', re.I)) or
                          soup.find(text=re.compile('table of contents', re.I)))

            # Check for examples/usage section
            has_examples = bool(soup.find(text=re.compile('example|how to|usage', re.I)))

            # Look for mathematical formulas (for calculators)
            has_formulas = bool(soup.find(text=re.compile('formula|equation|calculation', re.I)))

            # Check for related tools links
            has_related = bool(soup.find(text=re.compile('related tools|see also', re.I)))

            return {
                'word_count': word_count,
                'headings': {
                    'h1': h1_count,
                    'h2': h2_count,
                    'h3': h3_count
                },
                'has_faq': has_faq,
                'has_meta_desc': has_meta_desc,
                'has_schema': has_schema,
                'has_toc': has_toc,
                'has_examples': has_examples,
                'has_formulas': has_formulas,
                'has_related': has_related
            }

        except Exception as e:
            return {'error': str(e)}

    def identify_content_gaps(self, tool_name, analysis):
        """Identify content gaps and improvement opportunities"""
        gaps = []

        if analysis.get('word_count', 0) < 1500:
            gaps.append('Content under 1500 words - needs expansion')

        if not analysis.get('has_faq'):
            gaps.append('Missing FAQ section')

        if not analysis.get('has_examples'):
            gaps.append('Missing usage examples')

        if analysis.get('headings', {}).get('h2', 0) < 3:
            gaps.append('Insufficient H2 headings for content structure')

        if not analysis.get('has_toc'):
            gaps.append('Missing table of contents')

        if 'calculator' in tool_name.lower() and not analysis.get('has_formulas'):
            gaps.append('Calculator missing mathematical formulas/explanations')

        if not analysis.get('has_related'):
            gaps.append('Missing related tools cross-references')

        return gaps

    def suggest_content_enhancements(self, tool_name, analysis):
        """Suggest specific content enhancements"""
        suggestions = []

        # Content expansion suggestions
        if analysis.get('word_count', 0) < 2000:
            suggestions.append('Add more detailed usage scenarios and examples')

        # Tool-specific suggestions
        if 'calculator' in tool_name.lower():
            suggestions.append('Add mathematical background and formula explanations')
            suggestions.append('Include accuracy notes and limitations')

        if 'converter' in tool_name.lower():
            suggestions.append('Add conversion rate explanations and factors')
            suggestions.append('Include historical context or rate trends')

        if 'generator' in tool_name.lower():
            suggestions.append('Add customization options and best practices')
            suggestions.append('Include security considerations if applicable')

        # General enhancements
        suggestions.extend([
            'Add more comprehensive FAQ section',
            'Include troubleshooting section',
            'Add educational content about the topic',
            'Include tips and best practices',
            'Add comparison with alternatives'
        ])

        return suggestions

    def analyze_tool(self, tool_name):
        """Analyze a single tool comprehensively"""
        tool_path = os.path.join(self.tools_dir, tool_name)
        index_path = os.path.join(tool_path, 'index.html')

        if not os.path.exists(index_path):
            return {
                'tool': tool_name,
                'error': 'No index.html found'
            }

        analysis = self.analyze_html_content(index_path)
        gaps = self.identify_content_gaps(tool_name, analysis)
        suggestions = self.suggest_content_enhancements(tool_name, analysis)

        return {
            'tool': tool_name,
            'analysis': analysis,
            'content_gaps': gaps,
            'enhancement_suggestions': suggestions,
            'priority': 'HIGH' if len(gaps) > 3 else 'MEDIUM' if len(gaps) > 1 else 'LOW'
        }

    def run_comprehensive_analysis(self):
        """Run analysis on all N-S tools"""
        tools = self.get_n_s_tools()
        print(f"Starting content QA analysis for {len(tools)} N-S tools...")

        for i, tool in enumerate(tools):
            print(f"Analyzing {tool} ({i+1}/{len(tools)})")
            result = self.analyze_tool(tool)
            self.results.append(result)

        return self.results

    def generate_report(self):
        """Generate comprehensive QA report"""
        high_priority = [r for r in self.results if r.get('priority') == 'HIGH']
        medium_priority = [r for r in self.results if r.get('priority') == 'MEDIUM']
        low_priority = [r for r in self.results if r.get('priority') == 'LOW']

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tools': len(self.results),
            'summary': {
                'high_priority_tools': len(high_priority),
                'medium_priority_tools': len(medium_priority),
                'low_priority_tools': len(low_priority)
            },
            'high_priority_tools': high_priority,
            'recommendations': self.get_top_recommendations()
        }

        return report

    def get_top_recommendations(self):
        """Get top content enhancement recommendations"""
        all_gaps = []
        for result in self.results:
            all_gaps.extend(result.get('content_gaps', []))

        gap_counts = {}
        for gap in all_gaps:
            gap_counts[gap] = gap_counts.get(gap, 0) + 1

        return sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    analyzer = ContentQAAnalyzer('/Users/mike/zovo-workspaces/zovo-tools')
    results = analyzer.run_comprehensive_analysis()
    report = analyzer.generate_report()

    # Save report
    with open('/Users/mike/zovo-workspaces/zovo-tools/content_qa_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nContent QA Analysis Complete!")
    print(f"Total tools analyzed: {report['total_tools']}")
    print(f"High priority: {report['summary']['high_priority_tools']}")
    print(f"Medium priority: {report['summary']['medium_priority_tools']}")
    print(f"Low priority: {report['summary']['low_priority_tools']}")
    print(f"\nReport saved to: content_qa_report.json")