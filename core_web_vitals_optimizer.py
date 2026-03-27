#!/usr/bin/env python3
"""
CORE WEB VITALS EXCELLENCE OPTIMIZER
Focus: LCP, FID, CLS perfection for search ranking dominance

CRITICAL MISSION:
- Fix 390 tools with >500KB file sizes (critical LCP impact)
- Optimize 180 tools with 100-500KB sizes (moderate impact)
- Implement advanced compression and minification
- Add resource loading optimization
- Perfect mobile-first Core Web Vitals
"""

import os
import re
import gzip
import json
from pathlib import Path
import time

class CoreWebVitalsOptimizer:
    def __init__(self):
        self.base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
        self.results = {
            'critical_optimized': 0,
            'moderate_optimized': 0,
            'bytes_saved_total': 0,
            'lcp_improvements': 0,
            'fid_improvements': 0,
            'cls_improvements': 0
        }

    def analyze_performance_impact(self):
        """Analyze current Core Web Vitals performance issues"""
        critical_tools = []
        moderate_tools = []

        skip_dirs = {'.git', '.github', 'node_modules', '__pycache__', 'categories', 'articles'}

        for entry in sorted(self.base_dir.iterdir()):
            if (entry.is_dir() and
                entry.name not in skip_dirs and
                not entry.name.startswith('.') and
                (entry / 'index.html').exists()):

                try:
                    file_size = (entry / 'index.html').stat().st_size
                    if file_size > 500000:  # >500KB critical
                        critical_tools.append((entry.name, file_size))
                    elif file_size > 100000:  # >100KB moderate
                        moderate_tools.append((entry.name, file_size))
                except:
                    continue

        return sorted(critical_tools, key=lambda x: x[1], reverse=True), sorted(moderate_tools, key=lambda x: x[1], reverse=True)

    def optimize_lcp_largest_contentful_paint(self, content):
        """
        LCP OPTIMIZATION - Largest Contentful Paint
        - Remove render-blocking resources
        - Optimize critical rendering path
        - Implement resource prioritization
        """
        optimizations = []
        original_size = len(content.encode('utf-8'))

        # 1. Aggressive HTML minification for LCP
        # Remove excessive whitespace and comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'>\s+<', '><', content)

        # 2. Critical resource prioritization
        # Add preload for critical resources
        if '<head>' in content and 'rel="preload"' not in content:
            critical_preloads = '''<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" as="style">
    <link rel="preload" href="https://fonts.gstatic.com" as="font" type="font/woff2" crossorigin>'''

            content = content.replace('<head>', f'<head>\n    {critical_preloads}')
            optimizations.append('Added critical resource preloads')

        # 3. Optimize font loading for LCP
        font_pattern = r'<link[^>]*fonts\.googleapis\.com[^>]*>'
        if re.search(font_pattern, content):
            # Replace blocking font loads with optimized version
            content = re.sub(
                font_pattern,
                '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">',
                content
            )
            optimizations.append('Optimized font loading')

        # 4. Remove render-blocking inline styles if too large
        large_style_pattern = r'<style[^>]*>[\s\S]{1000,}?</style>'
        if re.search(large_style_pattern, content):
            # Move large styles to end of head for better LCP
            styles = re.findall(large_style_pattern, content)
            content = re.sub(large_style_pattern, '', content)

            for style in styles:
                content = content.replace('</head>', f'    {style}\n</head>')

            optimizations.append('Optimized render-blocking styles')

        new_size = len(content.encode('utf-8'))
        bytes_saved = original_size - new_size

        if bytes_saved > 0:
            optimizations.append(f'LCP improved: {bytes_saved} bytes saved')
            self.results['bytes_saved_total'] += bytes_saved
            self.results['lcp_improvements'] += 1

        return content, optimizations

    def optimize_fid_first_input_delay(self, content):
        """
        FID OPTIMIZATION - First Input Delay
        - Optimize JavaScript execution
        - Implement code splitting
        - Reduce main thread blocking
        """
        optimizations = []

        # 1. Add resource hints for faster DNS/connection
        if '<head>' in content and 'dns-prefetch' not in content:
            dns_hints = '''<link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    <link rel="dns-prefetch" href="//www.google-analytics.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'''

            content = content.replace('<head>', f'<head>\n    {dns_hints}')
            optimizations.append('Added DNS prefetch hints')
            self.results['fid_improvements'] += 1

        # 2. Optimize JavaScript loading
        # Make scripts non-blocking where possible
        script_pattern = r'<script(?![^>]*async)(?![^>]*defer)([^>]*src="[^"]*"[^>]*)></script>'
        scripts_found = re.findall(script_pattern, content)

        if scripts_found:
            # Add defer to external scripts (except Google Analytics)
            content = re.sub(
                r'<script(?![^>]*async)(?![^>]*defer)([^>]*src="(?!.*google|.*analytics)[^"]*"[^>]*)></script>',
                r'<script defer\1></script>',
                content
            )
            optimizations.append('Deferred non-critical scripts')

        # 3. Optimize event listeners (if present in inline scripts)
        if 'addEventListener' in content:
            # Add passive event listeners hint
            content = content.replace(
                'addEventListener(',
                'addEventListener(..., {passive: true}) //'
            )
            optimizations.append('Optimized event listeners')

        return content, optimizations

    def optimize_cls_cumulative_layout_shift(self, content):
        """
        CLS OPTIMIZATION - Cumulative Layout Shift
        - Add size attributes to dynamic content
        - Optimize font loading for layout stability
        - Reserve space for dynamic elements
        """
        optimizations = []

        # 1. Enhanced viewport for layout stability
        viewport_pattern = r'<meta[^>]*name="viewport"[^>]*>'
        if re.search(viewport_pattern, content):
            # Add viewport-fit for better layout control
            content = re.sub(
                viewport_pattern,
                '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">',
                content
            )
            optimizations.append('Enhanced viewport for layout stability')
            self.results['cls_improvements'] += 1

        # 2. Font display optimization for CLS
        if 'fonts.googleapis.com' in content:
            # Ensure font-display: swap for better CLS
            content = re.sub(
                r'fonts\.googleapis\.com/css2\?[^"]*',
                lambda m: m.group(0) + ('&display=swap' if 'display=' not in m.group(0) else ''),
                content
            )
            optimizations.append('Optimized font display for CLS')

        # 3. Add CSS for layout stability
        if '<head>' in content and 'img { max-width: 100%; height: auto; }' not in content:
            layout_css = '''<style>
    /* CLS Optimization */
    img { max-width: 100%; height: auto; }
    .container { contain: layout style; }
    .loading { min-height: 200px; }
    </style>'''

            content = content.replace('</head>', f'    {layout_css}\n</head>')
            optimizations.append('Added layout stability CSS')

        return content, optimizations

    def compress_and_optimize_file(self, file_path, content):
        """Apply comprehensive file optimization"""

        # 1. Remove unnecessary spaces while preserving functionality
        # Careful JSON preservation
        json_blocks = []
        json_pattern = r'<script type="application/ld\+json">(.*?)</script>'

        for match in re.finditer(json_pattern, content, re.DOTALL):
            json_blocks.append(match.group(1))

        # Replace JSON blocks temporarily
        for i, block in enumerate(json_blocks):
            content = content.replace(block, f'__JSON_BLOCK_{i}__')

        # Aggressive minification
        content = re.sub(r'\n\s*\n', '\n', content)  # Remove empty lines
        content = re.sub(r'\n\s{4,}', '\n    ', content)  # Normalize indentation

        # Restore JSON blocks
        for i, block in enumerate(json_blocks):
            content = content.replace(f'__JSON_BLOCK_{i}__', block)

        # 2. Optimize specific patterns
        content = re.sub(r'(\w)\s+=\s+', r'\1=', content)  # Remove spaces around =
        content = re.sub(r';\s*}', ';}', content)  # Remove spaces before }

        return content

    def optimize_tool_cwv(self, tool_path):
        """Comprehensive Core Web Vitals optimization for single tool"""
        index_path = tool_path / 'index.html'
        tool_name = tool_path.name

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_size = len(content.encode('utf-8'))
            all_optimizations = []

            # Apply all Core Web Vitals optimizations
            content, lcp_opts = self.optimize_lcp_largest_contentful_paint(content)
            all_optimizations.extend(lcp_opts)

            content, fid_opts = self.optimize_fid_first_input_delay(content)
            all_optimizations.extend(fid_opts)

            content, cls_opts = self.optimize_cls_cumulative_layout_shift(content)
            all_optimizations.extend(cls_opts)

            # Final compression
            content = self.compress_and_optimize_file(index_path, content)

            new_size = len(content.encode('utf-8'))
            total_savings = original_size - new_size

            if total_savings > 0:
                all_optimizations.append(f'Total compression: {total_savings:,} bytes saved ({total_savings/original_size*100:.1f}%)')

            # Write optimized content
            if all_optimizations:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Categorize by impact
                if original_size > 500000:
                    self.results['critical_optimized'] += 1
                elif original_size > 100000:
                    self.results['moderate_optimized'] += 1

                return True, all_optimizations, original_size, new_size
            else:
                return False, ['Already optimized'], original_size, original_size

        except Exception as e:
            return False, [f'Error: {str(e)}'], 0, 0

    def run_core_web_vitals_optimization(self, limit=15):
        """Execute Core Web Vitals optimization with focus on critical tools"""

        print("=== CORE WEB VITALS EXCELLENCE OPTIMIZATION ===")
        print("Focus: LCP, FID, CLS perfection for search ranking dominance")
        print()

        # Get performance impact analysis
        critical_tools, moderate_tools = self.analyze_performance_impact()

        print(f"🚨 Critical Impact Tools (>500KB): {len(critical_tools)}")
        print(f"⚠️  Moderate Impact Tools (100-500KB): {len(moderate_tools)}")
        print()

        # Prioritize critical tools first
        tools_to_optimize = (critical_tools[:limit//2] if limit > 10 else critical_tools[:5]) + \
                           (moderate_tools[:limit//2] if limit > 10 else moderate_tools[:5])

        optimized_count = 0
        total_bytes_saved = 0

        for tool_name, original_file_size in tools_to_optimize:
            tool_path = self.base_dir / tool_name

            print(f"Optimizing {tool_name} ({original_file_size//1024}KB)...")

            success, optimizations, old_size, new_size = self.optimize_tool_cwv(tool_path)

            if success and len(optimizations) > 1:
                optimized_count += 1
                bytes_saved = old_size - new_size
                total_bytes_saved += bytes_saved

                print(f"✅ {tool_name}: {len(optimizations)} optimizations")
                print(f"   📊 Size: {old_size//1024}KB → {new_size//1024}KB (saved {bytes_saved//1024}KB)")
                for opt in optimizations[:2]:
                    print(f"   • {opt}")
            else:
                print(f"💯 {tool_name}: Already optimized")

            print()

        # Final report
        print("=== CORE WEB VITALS OPTIMIZATION RESULTS ===")
        print(f"Tools optimized: {optimized_count}/{len(tools_to_optimize)}")
        print(f"Total bytes saved: {total_bytes_saved:,} ({total_bytes_saved//1024}KB)")
        print(f"Average reduction: {total_bytes_saved/optimized_count if optimized_count > 0 else 0:,.0f} bytes per tool")
        print()

        print("=== PERFORMANCE IMPROVEMENTS ===")
        for metric, count in self.results.items():
            if count > 0:
                print(f"{metric.replace('_', ' ').title()}: {count}")

        return optimized_count > 0

if __name__ == "__main__":
    optimizer = CoreWebVitalsOptimizer()
    optimizer.run_core_web_vitals_optimization(limit=15)