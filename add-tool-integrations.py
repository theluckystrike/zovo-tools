#!/usr/bin/env python3
"""
Tool Integration Enhancement Script
Expansion Agent 5 - Autonomous Cross-Tool Integration
Adds comprehensive tool integration widgets to target tools
"""

import os
import re
import json
from pathlib import Path

class ToolIntegrationInjector:
    def __init__(self):
        self.target_tools = [
            # X-Z tools
            'xml-formatter',
            'xml-to-csv-converter',
            'yaml-to-json-converter',
            'yaml-validator',
            'yen-to-usd-converter',
            'youtube-converter',
            'youtube-thumbnail',
            'z-value-table',
            # 0-9 tools
            '1-rep-max-calculator',
            '401k-calculator',
            '529-calculator',
            '60k-a-year-is-how-much-an-hour'
        ]

        self.integration_code = self.get_integration_code()

    def get_integration_code(self):
        return """
<!-- Tool Integration System - Expansion Agent 5 -->
<script src="../tool-integration-system.js"></script>
<script src="../related-tools-widget.js"></script>
<script src="../tool-comparison-system.js"></script>

<div id="tool-ecosystem-integration" style="margin: 32px 0;">
    <div id="related-tools-container"></div>

    <div class="tool-workflow-suggestions" style="background: #12121a; border: 1px solid rgba(0,255,136,0.1); border-radius: 12px; padding: 20px; margin: 20px 0;">
        <h3 style="color: #00ff88; margin: 0 0 16px 0; font-size: 1.2rem;">🔄 Workflow Integration</h3>
        <div id="workflow-suggestions"></div>
    </div>

    <div class="cross-tool-data-flow" style="background: #12121a; border: 1px solid rgba(0,204,255,0.1); border-radius: 12px; padding: 20px; margin: 20px 0;">
        <h3 style="color: #00ccff; margin: 0 0 16px 0; font-size: 1.2rem;">📊 Data Flow Options</h3>
        <div id="data-flow-options"></div>
    </div>
</div>

<script>
// Enhanced Tool Integration for Current Tool
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const toolMatch = currentPath.match(/\/free-tools\/([^\/]+)\//);
    const currentTool = toolMatch ? toolMatch[1] : 'unknown-tool';

    // Initialize workflow suggestions
    initializeWorkflowSuggestions(currentTool);

    // Initialize data flow options
    initializeDataFlowOptions(currentTool);

    // Track advanced analytics
    trackAdvancedAnalytics(currentTool);
});

function initializeWorkflowSuggestions(currentTool) {
    const workflowMap = {
        'xml-formatter': [
            { next: 'xml-to-csv-converter', action: 'Convert formatted XML to CSV', icon: '📊' },
            { next: 'yaml-to-json-converter', action: 'Transform to YAML then JSON', icon: '🔄' },
            { next: 'regex-visualizer', action: 'Extract patterns from XML', icon: '🔍' }
        ],
        'xml-to-csv-converter': [
            { next: 'yaml-validator', action: 'Validate converted data structure', icon: '✅' },
            { next: 'xml-formatter', action: 'Format source XML first', icon: '🎨' },
            { next: 'ebook-reader', action: 'Read CSV as structured data', icon: '📖' }
        ],
        'yaml-validator': [
            { next: 'yaml-to-json-converter', action: 'Convert valid YAML to JSON', icon: '🔄' },
            { next: 'xml-formatter', action: 'Compare with XML structure', icon: '⚖️' },
            { next: 'regex-visualizer', action: 'Extract validation patterns', icon: '🔍' }
        ],
        'yaml-to-json-converter': [
            { next: 'yaml-validator', action: 'Validate YAML before conversion', icon: '✅' },
            { next: 'xml-to-csv-converter', action: 'Further convert to CSV', icon: '📊' },
            { next: 'ai-logo-generator', action: 'Use JSON for design configs', icon: '🎨' }
        ],
        'yen-to-usd-converter': [
            { next: '60k-a-year-is-how-much-an-hour', action: 'Calculate hourly rates in USD', icon: '⏰' },
            { next: 'paycheck-estimator-texas', action: 'Estimate US paycheck', icon: '💰' },
            { next: 'sales-commission-calculator', action: 'Calculate commission in USD', icon: '💼' }
        ],
        '1-rep-max-calculator': [
            { next: 'army-fitness-calculator', action: 'Check military fitness scores', icon: '🏃' },
            { next: 'sleep-cycle-calculator', action: 'Optimize recovery timing', icon: '😴' },
            { next: 'puppy-years-to-human-years', action: 'Age-adjust training intensity', icon: '🐕' }
        ],
        '401k-calculator': [
            { next: '529-calculator', action: 'Plan education savings too', icon: '🎓' },
            { next: 'home-insurance-calculator', action: 'Protect your investments', icon: '🏠' },
            { next: 'bond-yield-calculator', action: 'Diversify with bonds', icon: '📈' }
        ],
        '529-calculator': [
            { next: '401k-calculator', action: 'Coordinate retirement savings', icon: '🏖️' },
            { next: '60k-a-year-is-how-much-an-hour', action: 'Calculate funding requirements', icon: '💰' },
            { next: 'paycheck-estimator-texas', action: 'Budget for contributions', icon: '📊' }
        ],
        'z-value-table': [
            { next: 'three-phase-power-calculator', action: 'Apply statistics to engineering', icon: '⚡' },
            { next: 'mixed-fraction-calculator', action: 'Calculate precise fractions', icon: '🔢' },
            { next: 'acceleration-calculator', action: 'Statistical motion analysis', icon: '🚀' }
        ],
        'youtube-converter': [
            { next: 'youtube-thumbnail', action: 'Generate thumbnails for videos', icon: '🖼️' },
            { next: 'ebook-reader', action: 'Read video transcripts', icon: '📚' },
            { next: 'ai-logo-generator', action: 'Create channel branding', icon: '🎨' }
        ],
        'youtube-thumbnail': [
            { next: 'youtube-converter', action: 'Convert videos with thumbnails', icon: '🎬' },
            { next: 'ai-logo-generator', action: 'Generate matching logos', icon: '🎨' },
            { next: 'border-radius-generator', action: 'Style thumbnail borders', icon: '🖼️' }
        ]
    };

    const workflows = workflowMap[currentTool] || [];
    const container = document.getElementById('workflow-suggestions');

    if (workflows.length === 0) {
        container.innerHTML = '<p style="color: #888; font-style: italic;">Workflow suggestions will be added as tool relationships are discovered.</p>';
        return;
    }

    container.innerHTML = workflows.map(workflow => `
        <div class="workflow-item" style="display: flex; align-items: center; gap: 12px; padding: 12px; background: rgba(0,255,136,0.03); border-radius: 8px; margin-bottom: 8px; cursor: pointer;"
             onclick="navigateToWorkflow('${workflow.next}')">
            <span style="font-size: 1.5rem;">${workflow.icon}</span>
            <div>
                <div style="color: #e0e0e8; font-weight: 500;">${workflow.action}</div>
                <div style="color: #888; font-size: 0.85rem;">Continue to ${workflow.next.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}</div>
            </div>
        </div>
    `).join('');
}

function initializeDataFlowOptions(currentTool) {
    const dataFlowMap = {
        'xml-formatter': {
            exports: ['formatted XML', 'minified XML', 'validation report'],
            imports: ['raw XML files', 'XML snippets'],
            integrations: [
                { tool: 'xml-to-csv-converter', data: 'formatted XML → CSV conversion', bidirectional: false },
                { tool: 'yaml-validator', data: 'validation patterns', bidirectional: true }
            ]
        },
        'xml-to-csv-converter': {
            exports: ['CSV data', 'conversion report', 'field mapping'],
            imports: ['XML files', 'XML schema'],
            integrations: [
                { tool: 'xml-formatter', data: 'pre-formatted XML', bidirectional: false },
                { tool: 'yaml-to-json-converter', data: 'structured data exchange', bidirectional: true }
            ]
        },
        '401k-calculator': {
            exports: ['retirement projections', 'contribution schedules', 'tax calculations'],
            imports: ['salary data', 'employer matching info'],
            integrations: [
                { tool: '529-calculator', data: 'coordinated savings planning', bidirectional: true },
                { tool: 'paycheck-estimator-texas', data: 'net income for planning', bidirectional: false }
            ]
        },
        'yen-to-usd-converter': {
            exports: ['converted amounts', 'exchange rates', 'historical data'],
            imports: ['JPY amounts', 'USD amounts'],
            integrations: [
                { tool: '60k-a-year-is-how-much-an-hour', data: 'converted salary calculations', bidirectional: false },
                { tool: 'sales-commission-calculator', data: 'multi-currency commission', bidirectional: false }
            ]
        }
    };

    const dataFlow = dataFlowMap[currentTool];
    const container = document.getElementById('data-flow-options');

    if (!dataFlow) {
        container.innerHTML = '<p style="color: #888; font-style: italic;">Data flow connections will be established as tool usage patterns are analyzed.</p>';
        return;
    }

    container.innerHTML = `
        <div class="data-flow-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
            <div class="exports-section">
                <h4 style="color: #00ff88; margin: 0 0 8px 0; font-size: 0.95rem;">📤 Exports</h4>
                ${dataFlow.exports.map(exp => `
                    <div style="padding: 4px 8px; background: rgba(0,255,136,0.1); border-radius: 4px; margin-bottom: 4px; font-size: 0.85rem;">
                        ${exp}
                    </div>
                `).join('')}
            </div>
            <div class="imports-section">
                <h4 style="color: #00ccff; margin: 0 0 8px 0; font-size: 0.95rem;">📥 Imports</h4>
                ${dataFlow.imports.map(imp => `
                    <div style="padding: 4px 8px; background: rgba(0,204,255,0.1); border-radius: 4px; margin-bottom: 4px; font-size: 0.85rem;">
                        ${imp}
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="integrations-section">
            <h4 style="color: #ffaa00; margin: 0 0 8px 0; font-size: 0.95rem;">🔗 Active Integrations</h4>
            ${dataFlow.integrations.map(integration => `
                <div class="integration-item" style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: rgba(255,170,0,0.1); border-radius: 6px; margin-bottom: 6px;">
                    <span style="font-size: 0.85rem; color: #e0e0e8;">
                        ${integration.data}
                    </span>
                    <button onclick="connectToTool('${integration.tool}')"
                            style="padding: 4px 8px; background: #ffaa00; color: #0a0a0f; border: none; border-radius: 4px; font-size: 0.75rem; cursor: pointer;">
                        Connect to ${integration.tool.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                    </button>
                </div>
            `).join('')}
        </div>
    `;
}

function navigateToWorkflow(nextTool) {
    window.toolIntegration.trackToolUsage(nextTool);
    window.location.href = `/free-tools/${nextTool}/`;
}

function connectToTool(toolId) {
    window.toolIntegration.trackToolUsage(toolId);
    window.open(`/free-tools/${toolId}/`, '_blank');
}

function trackAdvancedAnalytics(currentTool) {
    // Track integration interactions
    const analytics = JSON.parse(localStorage.getItem('toolIntegrationAnalytics') || '{}');
    const today = new Date().toISOString().split('T')[0];

    if (!analytics[today]) {
        analytics[today] = {};
    }

    if (!analytics[today][currentTool]) {
        analytics[today][currentTool] = { visits: 0, integrations_viewed: 0 };
    }

    analytics[today][currentTool].visits++;
    analytics[today][currentTool].integrations_viewed++;

    localStorage.setItem('toolIntegrationAnalytics', JSON.stringify(analytics));
}
</script>

<style>
.workflow-item:hover {
    background: rgba(0,255,136,0.08) !important;
    transform: translateX(4px);
    transition: all 0.2s ease;
}

.integration-item button:hover {
    background: #e69500 !important;
    transform: scale(1.05);
    transition: all 0.1s ease;
}

@media (max-width: 768px) {
    .data-flow-grid {
        grid-template-columns: 1fr !important;
    }
}
</style>
<!-- End Tool Integration System -->
"""

    def process_tool(self, tool_name):
        """Add integration code to a specific tool"""
        tool_path = Path(f"/Users/mike/zovo-workspaces/zovo-tools/{tool_name}/index.html")

        if not tool_path.exists():
            print(f"⚠️  Tool not found: {tool_name}")
            return False

        try:
            # Read the current file
            content = tool_path.read_text(encoding='utf-8', errors='ignore')

            # Check if integration already exists
            if 'tool-integration-system.js' in content:
                print(f"✅ Integration already exists in {tool_name}")
                return True

            # Find insertion point - before closing </body> or </html>
            insertion_point = None

            # Look for </body> first
            body_match = re.search(r'</body>', content, re.IGNORECASE)
            if body_match:
                insertion_point = body_match.start()

            # If no </body>, look for </html>
            if insertion_point is None:
                html_match = re.search(r'</html>', content, re.IGNORECASE)
                if html_match:
                    insertion_point = html_match.start()

            # If neither found, append to end
            if insertion_point is None:
                insertion_point = len(content)

            # Insert the integration code
            enhanced_content = (
                content[:insertion_point] +
                self.integration_code +
                content[insertion_point:]
            )

            # Write back to file
            tool_path.write_text(enhanced_content, encoding='utf-8')
            print(f"✅ Enhanced {tool_name} with tool integration system")
            return True

        except Exception as e:
            print(f"❌ Error processing {tool_name}: {str(e)}")
            return False

    def process_all_tools(self):
        """Process all target tools"""
        print("🚀 Expansion Agent 5 - Starting Tool Integration Enhancement")
        print(f"🎯 Target tools: {len(self.target_tools)}")

        success_count = 0

        for tool in self.target_tools:
            print(f"\n🔧 Processing: {tool}")
            if self.process_tool(tool):
                success_count += 1

        print(f"\n📊 Integration Summary:")
        print(f"   ✅ Successfully enhanced: {success_count}")
        print(f"   ❌ Failed: {len(self.target_tools) - success_count}")
        print(f"   📈 Success rate: {(success_count/len(self.target_tools)*100):.1f}%")

        return success_count

def main():
    injector = ToolIntegrationInjector()
    return injector.process_all_tools()

if __name__ == "__main__":
    main()