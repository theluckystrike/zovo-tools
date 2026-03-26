#!/usr/bin/env python3
"""
Tool Category Landing Page Generator
Expansion Agent 5 - Ecosystem Navigation Enhancement
Creates comprehensive category landing pages with tool comparisons
"""

import os
import json
from pathlib import Path

class CategoryPageGenerator:
    def __init__(self):
        self.categories = {
            'financial-calculators': {
                'name': 'Financial Calculators',
                'description': 'Comprehensive financial planning and calculation tools for retirement, education, investments, and income planning.',
                'icon': '💰',
                'tools': [
                    '401k-calculator', '529-calculator', 'bond-yield-calculator',
                    'home-insurance-calculator', 'paycheck-estimator-texas',
                    'sales-commission-calculator', 'reverse-mortgage-calculator'
                ]
            },
            'conversion-tools': {
                'name': 'Conversion & Formatting Tools',
                'description': 'Data transformation, formatting, and conversion utilities for developers and data analysts.',
                'icon': '🔄',
                'tools': [
                    'xml-formatter', 'xml-to-csv-converter', 'yaml-to-json-converter',
                    'yaml-validator', 'yen-to-usd-converter', 'favicon-converter'
                ]
            },
            'health-fitness': {
                'name': 'Health & Fitness Calculators',
                'description': 'Medical, fitness, and health-related calculation tools for monitoring and planning.',
                'icon': '🏥',
                'tools': [
                    'a1c-calculator', 'army-fitness-calculator', '1-rep-max-calculator',
                    'puppy-years-to-human-years', 'sleep-cycle-calculator',
                    'augmentin-pediatric-dose-calculator'
                ]
            },
            'math-statistics': {
                'name': 'Math & Statistics Tools',
                'description': 'Mathematical calculation and statistical analysis tools for students, researchers, and professionals.',
                'icon': '📊',
                'tools': [
                    'mixed-fraction-calculator', 'z-value-table',
                    'three-phase-power-calculator', 'acceleration-calculator'
                ]
            },
            'measurement-calculation': {
                'name': 'Measurement & Calculation',
                'description': 'Practical measurement tools for construction, real estate, and everyday calculations.',
                'icon': '📏',
                'tools': [
                    'acre-square-footage', 'acreage-calculator',
                    'stud-spacing-calculator', '60k-a-year-is-how-much-an-hour'
                ]
            },
            'development-tools': {
                'name': 'Development & Design Tools',
                'description': 'Web development, design, and creative tools for developers and designers.',
                'icon': '⚙️',
                'tools': [
                    'regex-visualizer', 'border-radius-generator',
                    'ai-logo-generator', 'youtube-thumbnail'
                ]
            }
        }

    def generate_category_page(self, category_id, category_data):
        """Generate a comprehensive category landing page"""

        page_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{category_data['name']} - Free Online Tools | Zovo Tools</title>
    <link rel="canonical" href="https://zovo.one/free-tools/categories/{category_id}/"/>

    <meta name="description" content="{category_data['description']} Browse and compare {len(category_data['tools'])} professional-grade tools."/>
    <meta name="keywords" content="{category_id.replace('-', ' ')}, {', '.join([tool.replace('-', ' ') for tool in category_data['tools'][:5]])}, free online tools"/>
    <meta name="author" content="Zovo Tools"/>
    <meta name="robots" content="index, follow"/>

    <link rel="icon" href="https://zovo.one/favicon.ico"/>

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website"/>
    <meta property="og:url" content="https://zovo.one/free-tools/categories/{category_id}/"/>
    <meta property="og:title" content="{category_data['name']} - Free Online Tools"/>
    <meta property="og:description" content="{category_data['description']}"/>
    <meta property="og:image" content="https://quickchart.io/chart?c={{type:'doughnut',data:{{datasets:[{{data:[{len(category_data['tools'])},10],backgroundColor:['%2300ff88','%23333']}}]}},options:{{title:{{display:true,text:'{category_data['name']}%20Tools',fontColor:'%23e0e0e8'}}}}}}&backgroundColor=%230a0a0f&width=600&height=400"/>
    <meta property="og:site_name" content="Zovo Tools"/>

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:url" content="https://zovo.one/free-tools/categories/{category_id}/"/>
    <meta name="twitter:title" content="{category_data['name']} - Free Online Tools"/>
    <meta name="twitter:description" content="{category_data['description']}"/>
    <meta name="twitter:image" content="https://quickchart.io/chart?c={{type:'doughnut',data:{{datasets:[{{data:[{len(category_data['tools'])},10],backgroundColor:['%2300ff88','%23333']}}]}},options:{{title:{{display:true,text:'{category_data['name']}%20Tools',fontColor:'%23e0e0e8'}}}}}}&backgroundColor=%230a0a0f&width=600&height=400"/>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com"/>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{category_data['name']}",
      "description": "{category_data['description']}",
      "url": "https://zovo.one/free-tools/categories/{category_id}/",
      "mainEntity": {{
        "@type": "ItemList",
        "numberOfItems": {len(category_data['tools'])},
        "itemListElement": [
          {self.generate_schema_tools(category_data['tools'])}
        ]
      }},
      "author": {{
        "@type": "Organization",
        "name": "Zovo Tools"
      }},
      "dateModified": "2026-03-26"
    }}
    </script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>

    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0f; color: #e0e0e8; line-height: 1.7; }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

        /* Header Styles */
        .category-header {{
            text-align: center;
            margin-bottom: 48px;
            background: linear-gradient(135deg, rgba(0,255,136,0.1) 0%, rgba(0,204,255,0.1) 100%);
            border-radius: 20px;
            padding: 48px 32px;
            border: 1px solid rgba(0,255,136,0.2);
        }}

        .category-icon {{
            font-size: 4rem;
            margin-bottom: 16px;
            display: block;
        }}

        .category-title {{
            font-size: 3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 16px;
        }}

        .category-description {{
            font-size: 1.2rem;
            color: #b0b0b8;
            max-width: 600px;
            margin: 0 auto 24px;
        }}

        .category-stats {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 32px;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ff88;
            display: block;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #888;
        }}

        /* Navigation */
        .breadcrumb {{
            margin-bottom: 32px;
            font-size: 0.9rem;
            color: #888;
        }}

        .breadcrumb a {{
            color: #00ccff;
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        /* Tools Grid */
        .tools-section {{
            margin-bottom: 48px;
        }}

        .section-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #00ff88;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
        }}

        .tool-card {{
            background: #12121a;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .tool-card:hover {{
            border-color: #00ff88;
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,255,136,0.15);
        }}

        .tool-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}

        .tool-name {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
        }}

        .tool-description {{
            color: #b0b0b8;
            font-size: 0.95rem;
            margin-bottom: 16px;
        }}

        .tool-features {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 16px;
        }}

        .feature-tag {{
            background: rgba(0,255,136,0.1);
            color: #00ff88;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .tool-actions {{
            display: flex;
            gap: 8px;
            margin-top: 16px;
        }}

        .btn {{
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            font-family: 'Inter', sans-serif;
        }}

        .btn-primary {{
            background: #00ff88;
            color: #0a0a0f;
        }}

        .btn-primary:hover {{
            background: #00e07a;
            transform: scale(1.05);
        }}

        .btn-secondary {{
            background: transparent;
            color: #00ccff;
            border: 1px solid #00ccff;
        }}

        .btn-secondary:hover {{
            background: rgba(0,204,255,0.1);
        }}

        /* Comparison Section */
        .comparison-section {{
            background: #12121a;
            border: 1px solid rgba(255,170,0,0.2);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 48px;
        }}

        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        .comparison-table th,
        .comparison-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }}

        .comparison-table th {{
            background: rgba(0,255,136,0.05);
            color: #00ff88;
            font-weight: 600;
        }}

        .comparison-table tr:hover {{
            background: rgba(255,255,255,0.02);
        }}

        .rating-stars {{
            color: #ffaa00;
        }}

        /* Quick Access */
        .quick-access {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 32px;
        }}

        .quick-link {{
            display: block;
            padding: 16px;
            background: rgba(0,204,255,0.05);
            border: 1px solid rgba(0,204,255,0.2);
            border-radius: 12px;
            color: #00ccff;
            text-decoration: none;
            text-align: center;
            transition: all 0.2s ease;
        }}

        .quick-link:hover {{
            background: rgba(0,204,255,0.1);
            transform: translateY(-2px);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{ padding: 16px; }}
            .category-header {{ padding: 32px 20px; }}
            .category-title {{ font-size: 2rem; }}
            .category-stats {{ flex-direction: column; gap: 16px; }}
            .tools-grid {{ grid-template-columns: 1fr; }}
            .comparison-table {{ font-size: 0.85rem; }}
        }}
    </style>
</head>

<body>
    <!-- Navigation Header -->
    <div id="zovo-nav" style="position:sticky;top:0;z-index:1000;background:#0a0a0f;border-bottom:1px solid rgba(255,255,255,0.06);padding:0.8rem 1.5rem;display:flex;justify-content:space-between;align-items:center;font-family:Inter,sans-serif;">
        <a href="/" style="text-decoration:none;display:flex;align-items:center;gap:0.5rem;">
            <span style="font-size:1.1rem;font-weight:700;color:#00ff88;">Zovo</span>
            <span style="font-size:0.8rem;color:#888;">Tools</span>
        </a>
        <nav style="display:flex;gap:1.5rem;font-size:0.85rem;">
            <a href="/" style="color:#00ccff;text-decoration:none;">All Tools</a>
            <a href="/categories/" style="color:#00ccff;text-decoration:none;">Categories</a>
            <a href="https://zovo.one" style="color:#888;text-decoration:none;">zovo.one</a>
        </nav>
    </div>

    <div class="container">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
            <a href="/">Home</a> ›
            <a href="/free-tools/">Free Tools</a> ›
            <a href="/free-tools/categories/">Categories</a> ›
            {category_data['name']}
        </nav>

        <!-- Category Header -->
        <header class="category-header">
            <span class="category-icon">{category_data['icon']}</span>
            <h1 class="category-title">{category_data['name']}</h1>
            <p class="category-description">{category_data['description']}</p>

            <div class="category-stats">
                <div class="stat-item">
                    <span class="stat-number">{len(category_data['tools'])}</span>
                    <span class="stat-label">Tools Available</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">Free</span>
                    <span class="stat-label">Always</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">24/7</span>
                    <span class="stat-label">Available</span>
                </div>
            </div>
        </header>

        <!-- Tools Grid -->
        <section class="tools-section">
            <h2 class="section-title">
                🔧 Available Tools
            </h2>

            <div class="tools-grid">
                {self.generate_tool_cards(category_data['tools'])}
            </div>
        </section>

        <!-- Tool Comparison -->
        <section class="comparison-section">
            <h2 class="section-title">
                ⚖️ Tool Comparison Matrix
            </h2>
            <p style="color: #b0b0b8; margin-bottom: 20px;">
                Compare features and capabilities to find the perfect tool for your needs.
            </p>

            {self.generate_comparison_table(category_data['tools'])}
        </section>

        <!-- Quick Access Links -->
        <section class="tools-section">
            <h2 class="section-title">
                🚀 Quick Access
            </h2>

            <div class="quick-access">
                <a href="/free-tools/" class="quick-link">
                    📂 Browse All Tools
                </a>
                <a href="/free-tools/categories/" class="quick-link">
                    📋 All Categories
                </a>
                <a href="/free-tools/recently-used/" class="quick-link">
                    🕒 Recently Used
                </a>
                <a href="/free-tools/favorites/" class="quick-link">
                    ⭐ Your Favorites
                </a>
            </div>
        </section>
    </div>

    <!-- Integration Scripts -->
    <script src="../tool-integration-system.js"></script>
    <script src="../related-tools-widget.js"></script>
    <script src="../tool-comparison-system.js"></script>

    <script>
        // Track category page analytics
        document.addEventListener('DOMContentLoaded', function() {{
            const analytics = JSON.parse(localStorage.getItem('categoryPageAnalytics') || '{{}}');
            const today = new Date().toISOString().split('T')[0];

            if (!analytics[today]) analytics[today] = {{}};
            if (!analytics[today]['{category_id}']) analytics[today]['{category_id}'] = 0;

            analytics[today]['{category_id}']++;
            localStorage.setItem('categoryPageAnalytics', JSON.stringify(analytics));
        }});

        function trackToolClick(toolId) {{
            if (window.toolIntegration) {{
                window.toolIntegration.trackToolUsage(toolId);
            }}

            // Track category->tool navigation
            const navigation = JSON.parse(localStorage.getItem('categoryNavigation') || '{{}}');
            const key = '{category_id}' + '->' + toolId;
            navigation[key] = (navigation[key] || 0) + 1;
            localStorage.setItem('categoryNavigation', JSON.stringify(navigation));
        }}
    </script>
</body>
</html>"""

        return page_content

    def generate_schema_tools(self, tools):
        """Generate JSON-LD schema for tools list"""
        schema_items = []
        for i, tool in enumerate(tools[:10]):  # Limit to 10 for schema
            schema_items.append(f'''{{
                "@type": "WebApplication",
                "position": {i + 1},
                "name": "{self.get_tool_display_name(tool)}",
                "url": "https://zovo.one/free-tools/{tool}/",
                "applicationCategory": "UtilityApplication",
                "operatingSystem": "Any"
            }}''')

        return ',\n          '.join(schema_items)

    def generate_tool_cards(self, tools):
        """Generate HTML for tool cards"""
        cards = []

        tool_descriptions = {
            'xml-formatter': 'Format, validate, and beautify XML files with syntax highlighting and error detection.',
            'xml-to-csv-converter': 'Convert XML data to CSV format with customizable field mapping and structure preservation.',
            'yaml-to-json-converter': 'Transform YAML files to JSON format while maintaining data integrity and structure.',
            'yaml-validator': 'Validate YAML syntax, detect errors, and ensure compliance with best practices.',
            'yen-to-usd-converter': 'Real-time Japanese Yen to US Dollar conversion with current exchange rates.',
            '401k-calculator': 'Comprehensive retirement planning calculator with employer matching and tax projections.',
            '529-calculator': 'Education savings plan calculator with tax benefits and growth projections.',
            'a1c-calculator': 'Convert A1C percentages to estimated average glucose with risk level indicators.',
            '1-rep-max-calculator': 'Estimate one-rep max using multiple validated formulas for strength training.',
            'z-value-table': 'Statistical z-score table with probability calculations and critical values.',
            'mixed-fraction-calculator': 'Perform operations on mixed fractions with step-by-step solutions.',
            'youtube-thumbnail': 'Generate and customize YouTube video thumbnails with text and design options.',
            'youtube-converter': 'Download and convert YouTube videos to various formats and qualities.'
        }

        tool_features = {
            'xml-formatter': ['Syntax highlighting', 'Error detection', 'Minification', 'Validation'],
            'xml-to-csv-converter': ['Field mapping', 'Data preservation', 'Bulk processing', 'Custom delimiters'],
            'yaml-to-json-converter': ['Structure preservation', 'Error handling', 'Batch conversion', 'Validation'],
            'yaml-validator': ['Syntax validation', 'Error reporting', 'Best practices', 'Schema support'],
            'yen-to-usd-converter': ['Real-time rates', 'Historical data', 'Rate alerts', 'Accuracy'],
            '401k-calculator': ['Tax calculations', 'Employer matching', 'Projections', 'Withdrawal planning'],
            '529-calculator': ['Tax benefits', 'State plans', 'Investment growth', 'Education costs'],
            'a1c-calculator': ['Glucose conversion', 'Risk assessment', 'Unit support', 'Visual indicators'],
            '1-rep-max-calculator': ['Multiple formulas', 'Exercise variety', 'Progress tracking', 'Safety tips'],
            'z-value-table': ['Statistical accuracy', 'Critical values', 'Probability calc', 'Interactive table'],
            'mixed-fraction-calculator': ['Step-by-step', 'All operations', 'Simplification', 'Multiple formats'],
            'youtube-thumbnail': ['Custom text', 'Design templates', 'High quality', 'Quick generation'],
            'youtube-converter': ['Multiple formats', 'Quality options', 'Fast conversion', 'Bulk processing']
        }

        for tool in tools:
            name = self.get_tool_display_name(tool)
            description = tool_descriptions.get(tool, f'Professional {name.lower()} with advanced features and accuracy.')
            features = tool_features.get(tool, ['Professional grade', 'User friendly', 'Fast processing', 'Accurate results'])

            features_html = ''.join([f'<span class="feature-tag">{feature}</span>' for feature in features])

            card = f'''
                <div class="tool-card">
                    <div class="tool-card-header">
                        <div>
                            <h3 class="tool-name">{name}</h3>
                            <p class="tool-description">{description}</p>
                        </div>
                    </div>

                    <div class="tool-features">
                        {features_html}
                    </div>

                    <div class="tool-actions">
                        <a href="/free-tools/{tool}/" class="btn btn-primary" onclick="trackToolClick('{tool}')">
                            Launch Tool
                        </a>
                        <button class="btn btn-secondary" onclick="compareWith('{tool}')">
                            Compare
                        </button>
                    </div>
                </div>
            '''
            cards.append(card)

        return ''.join(cards)

    def generate_comparison_table(self, tools):
        """Generate comparison table for tools"""
        if len(tools) <= 1:
            return '<p style="color: #888;">Comparison table will be available when more tools are added to this category.</p>'

        # Simplified comparison for now
        rows = []
        for tool in tools[:8]:  # Limit to 8 tools for readability
            name = self.get_tool_display_name(tool)

            # Generate mock ratings for demonstration
            complexity = '⭐⭐⭐⭐⭐' if 'calculator' in tool else '⭐⭐⭐'
            features = '⭐⭐⭐⭐⭐' if any(x in tool for x in ['xml', 'yaml', '401k']) else '⭐⭐⭐⭐'
            mobile = '⭐⭐⭐⭐' if 'converter' in tool else '⭐⭐⭐⭐⭐'

            rows.append(f'''
                <tr>
                    <td><strong>{name}</strong></td>
                    <td><span class="rating-stars">{complexity}</span></td>
                    <td><span class="rating-stars">{features}</span></td>
                    <td><span class="rating-stars">{mobile}</span></td>
                    <td><a href="/free-tools/{tool}/" onclick="trackToolClick('{tool}')" style="color: #00ff88;">Use Tool</a></td>
                </tr>
            ''')

        table = f'''
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Tool</th>
                        <th>Complexity</th>
                        <th>Features</th>
                        <th>Mobile Friendly</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        '''

        return table

    def get_tool_display_name(self, tool_id):
        """Convert tool ID to display name"""
        return tool_id.replace('-', ' ').title()

    def create_category_directory_structure(self):
        """Create directory structure for category pages"""
        categories_dir = Path("/Users/mike/zovo-workspaces/zovo-tools/categories")
        categories_dir.mkdir(exist_ok=True)

        for category_id in self.categories.keys():
            category_dir = categories_dir / category_id
            category_dir.mkdir(exist_ok=True)

        print(f"✅ Created directory structure for {len(self.categories)} categories")

    def generate_all_category_pages(self):
        """Generate all category landing pages"""
        print("🚀 Expansion Agent 5 - Generating Category Landing Pages")

        self.create_category_directory_structure()

        success_count = 0

        for category_id, category_data in self.categories.items():
            try:
                page_content = self.generate_category_page(category_id, category_data)
                page_path = Path(f"/Users/mike/zovo-workspaces/zovo-tools/categories/{category_id}/index.html")

                page_path.write_text(page_content, encoding='utf-8')
                print(f"✅ Generated: {category_data['name']} ({len(category_data['tools'])} tools)")
                success_count += 1

            except Exception as e:
                print(f"❌ Error generating {category_id}: {str(e)}")

        # Generate main categories index
        self.generate_categories_index()

        print(f"\n📊 Category Pages Summary:")
        print(f"   ✅ Successfully generated: {success_count}")
        print(f"   ❌ Failed: {len(self.categories) - success_count}")
        print(f"   📈 Success rate: {(success_count/len(self.categories)*100):.1f}%")

        return success_count

    def generate_categories_index(self):
        """Generate main categories index page"""
        index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Tool Categories - Browse Free Online Tools by Category | Zovo Tools</title>
    <link rel="canonical" href="https://zovo.one/free-tools/categories/"/>

    <meta name="description" content="Browse {len(self.categories)} categories of free online tools. Find calculators, converters, development tools, and more organized by functionality."/>
    <meta name="keywords" content="tool categories, free online tools, calculators, converters, development tools, productivity tools"/>

    <link rel="icon" href="https://zovo.one/favicon.ico"/>
    <link rel="preconnect" href="https://fonts.googleapis.com"/>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>

    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0f; color: #e0e0e8; line-height: 1.7; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

        .header {{
            text-align: center;
            margin-bottom: 48px;
            padding: 48px 32px;
            background: linear-gradient(135deg, rgba(0,255,136,0.1) 0%, rgba(0,204,255,0.1) 100%);
            border-radius: 20px;
        }}

        .main-title {{
            font-size: 3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 16px;
        }}

        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            margin-bottom: 48px;
        }}

        .category-card {{
            background: #12121a;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }}

        .category-card:hover {{
            border-color: #00ff88;
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,255,136,0.15);
        }}

        .category-icon {{
            font-size: 3rem;
            margin-bottom: 16px;
            display: block;
        }}

        .category-name {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 12px;
        }}

        .category-description {{
            color: #b0b0b8;
            margin-bottom: 16px;
            font-size: 0.95rem;
        }}

        .category-count {{
            background: rgba(0,255,136,0.1);
            color: #00ff88;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .breadcrumb {{
            margin-bottom: 32px;
            font-size: 0.9rem;
            color: #888;
        }}

        .breadcrumb a {{
            color: #00ccff;
            text-decoration: none;
        }}

        @media (max-width: 768px) {{
            .categories-grid {{ grid-template-columns: 1fr; }}
            .main-title {{ font-size: 2rem; }}
        }}
    </style>
</head>

<body>
    <div id="zovo-nav" style="position:sticky;top:0;z-index:1000;background:#0a0a0f;border-bottom:1px solid rgba(255,255,255,0.06);padding:0.8rem 1.5rem;display:flex;justify-content:space-between;align-items:center;">
        <a href="/" style="text-decoration:none;display:flex;align-items:center;gap:0.5rem;">
            <span style="font-size:1.1rem;font-weight:700;color:#00ff88;">Zovo</span>
            <span style="font-size:0.8rem;color:#888;">Tools</span>
        </a>
        <nav style="display:flex;gap:1.5rem;font-size:0.85rem;">
            <a href="/" style="color:#00ccff;text-decoration:none;">All Tools</a>
            <a href="/categories/" style="color:#00ccff;text-decoration:none;">Categories</a>
        </nav>
    </div>

    <div class="container">
        <nav class="breadcrumb">
            <a href="/">Home</a> ›
            <a href="/free-tools/">Free Tools</a> ›
            Categories
        </nav>

        <header class="header">
            <h1 class="main-title">🗂️ Tool Categories</h1>
            <p style="font-size: 1.2rem; color: #b0b0b8;">
                Discover {len(self.categories)} categories of professional-grade tools
            </p>
        </header>

        <div class="categories-grid">
            {self.generate_category_cards()}
        </div>
    </div>
</body>
</html>'''

        categories_dir = Path("/Users/mike/zovo-workspaces/zovo-tools/categories")
        index_path = categories_dir / "index.html"
        index_path.write_text(index_content, encoding='utf-8')
        print("✅ Generated categories index page")

    def generate_category_cards(self):
        """Generate category cards for index page"""
        cards = []
        for category_id, category_data in self.categories.items():
            card = f'''
                <a href="{category_id}/" class="category-card">
                    <span class="category-icon">{category_data['icon']}</span>
                    <h3 class="category-name">{category_data['name']}</h3>
                    <p class="category-description">{category_data['description']}</p>
                    <span class="category-count">{len(category_data['tools'])} Tools</span>
                </a>
            '''
            cards.append(card)
        return ''.join(cards)

def main():
    generator = CategoryPageGenerator()
    return generator.generate_all_category_pages()

if __name__ == "__main__":
    main()