#!/usr/bin/env python3
"""
Surgical Performance Optimizer - Microsecond-level precision optimization
Extracts embedded data URIs and optimizes for performance
"""
import re
import os
import hashlib
from urllib.parse import unquote
import json

class SurgicalOptimizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.base_dir = os.path.dirname(file_path)
        self.assets_dir = os.path.join(self.base_dir, 'assets', 'images')
        self.extracted_assets = {}

    def ensure_assets_dir(self):
        """Create assets directory with surgical precision"""
        os.makedirs(self.assets_dir, exist_ok=True)

    def extract_data_uris(self, content):
        """Extract all data URIs with surgical precision"""
        # Pattern to match data URIs
        pattern = r'data:image/([^;,]+)(?:;[^,]*)?,(.*?)(?=[\'\">\s])'
        matches = re.finditer(pattern, content)

        extracted_count = 0
        for match in matches:
            mime_type = match.group(1)
            data = match.group(2)
            full_uri = match.group(0)

            # Create hash for unique filename
            uri_hash = hashlib.md5(full_uri.encode()).hexdigest()[:8]

            # Determine file extension
            ext_map = {
                'svg+xml': 'svg',
                'png': 'png',
                'jpeg': 'jpg',
                'jpg': 'jpg',
                'webp': 'webp'
            }
            ext = ext_map.get(mime_type, 'dat')
            filename = f"img_{uri_hash}.{ext}"

            # Save the asset
            asset_path = os.path.join(self.assets_dir, filename)

            if mime_type == 'svg+xml':
                # SVG data is URL encoded
                svg_content = unquote(data)
                with open(asset_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
            else:
                # Base64 encoded data
                import base64
                decoded_data = base64.b64decode(data)
                with open(asset_path, 'wb') as f:
                    f.write(decoded_data)

            # Store replacement mapping
            relative_path = f"assets/images/{filename}"
            self.extracted_assets[full_uri] = relative_path
            extracted_count += 1

        return extracted_count

    def optimize_html(self, content):
        """Apply surgical HTML optimizations"""
        # Replace data URIs with external references
        for data_uri, asset_path in self.extracted_assets.items():
            content = content.replace(data_uri, asset_path)

        # Add performance optimizations
        optimizations = []

        # Add resource hints if not present
        if 'rel="preconnect"' not in content:
            optimizations.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
            optimizations.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')

        # Add critical CSS loading optimization
        css_optimization = '''
        <style>
        /* Critical CSS - Above the fold */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; }
        .loader { display: none; }
        </style>
        '''

        # Add lazy loading script
        lazy_loading_script = '''
        <script>
        // Surgical precision lazy loading
        const imgs = document.querySelectorAll('img[data-src]');
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        imgs.forEach(img => imgObserver.observe(img));
        </script>
        '''

        # Insert optimizations before closing head tag
        if '</head>' in content:
            head_insertion = css_optimization + lazy_loading_script
            content = content.replace('</head>', head_insertion + '</head>')

        return content

    def run_surgical_optimization(self):
        """Execute surgical precision optimization"""
        print("🔬 SURGICAL PERFORMANCE OPTIMIZATION INITIATED")

        # Read original file
        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        original_size = len(original_content)
        print(f"📊 Original size: {original_size:,} bytes ({original_size/1024/1024:.2f}MB)")

        # Ensure assets directory exists
        self.ensure_assets_dir()

        # Extract data URIs
        extracted_count = self.extract_data_uris(original_content)
        print(f"🎯 Extracted {extracted_count} data URIs to external files")

        # Optimize HTML
        optimized_content = self.optimize_html(original_content)

        # Calculate size reduction
        optimized_size = len(optimized_content)
        size_reduction = original_size - optimized_size
        reduction_percent = (size_reduction / original_size) * 100

        # Create backup
        backup_path = self.file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)

        # Write optimized version
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)

        print(f"✅ Optimization complete!")
        print(f"📉 Size reduction: {size_reduction:,} bytes ({reduction_percent:.1f}%)")
        print(f"📁 New size: {optimized_size:,} bytes ({optimized_size/1024:.1f}KB)")
        print(f"🔒 Backup created: {backup_path}")

        return {
            'original_size': original_size,
            'optimized_size': optimized_size,
            'size_reduction': size_reduction,
            'reduction_percent': reduction_percent,
            'extracted_assets': len(self.extracted_assets)
        }

if __name__ == "__main__":
    file_path = "/Users/mike/zovo-workspaces/zovo-tools/qr-code-designer/index.html"
    optimizer = SurgicalOptimizer(file_path)
    results = optimizer.run_surgical_optimization()
    print(f"\n🎯 SURGICAL PRECISION METRICS:")
    print(json.dumps(results, indent=2))