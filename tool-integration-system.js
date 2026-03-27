/**
 * Tool Integration System - Cross-tool recommendation and navigation
 * Expansion Agent 5 - Autonomous Integration Enhancement
 */

class ToolIntegrationSystem {
    constructor() {
        this.toolCategories = this.initializeCategories();
        this.toolRelationships = this.buildRelationshipMap();
        this.recentlyUsed = JSON.parse(localStorage.getItem('recentlyUsedTools') || '[]');
        this.favorites = JSON.parse(localStorage.getItem('favoriteTools') || '[]');
        this.usageAnalytics = JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}');
    }

    initializeCategories() {
        return {
            'financial': {
                name: 'Financial Calculators',
                tools: [
                    '401k-calculator', '529-calculator', 'bond-yield-calculator',
                    'home-insurance-calculator', 'paycheck-estimator-texas',
                    'sales-commission-calculator', 'reverse-mortgage-calculator'
                ],
                icon: '💰'
            },
            'health': {
                name: 'Health & Fitness',
                tools: [
                    'a1c-calculator', 'army-fitness-calculator',
                    'puppy-years-to-human-years', 'sleep-cycle-calculator',
                    'augmentin-pediatric-dose-calculator'
                ],
                icon: '🏥'
            },
            'math': {
                name: 'Math & Statistics',
                tools: [
                    'jacobian-calculator', 'mixed-fraction-calculator', 'z-value-table',
                    'three-phase-power-calculator', 'acceleration-calculator'
                ],
                icon: '📊'
            },
            'conversion': {
                name: 'Converters & Formatters',
                tools: [
                    'xml-formatter', 'xml-to-csv-converter', 'yaml-to-json-converter',
                    'yaml-validator', 'yen-to-usd-converter', 'favicon-converter'
                ],
                icon: '🔄'
            },
            'development': {
                name: 'Development Tools',
                tools: [
                    'regex-visualizer', 'border-radius-generator',
                    'ai-logo-generator', 'youtube-thumbnail'
                ],
                icon: '⚙️'
            },
            'measurement': {
                name: 'Measurement & Calculation',
                tools: [
                    'acre-square-footage', 'acreage-calculator',
                    'stud-spacing-calculator', '60k-a-year-is-how-much-an-hour',
                    '1-rep-max-calculator'
                ],
                icon: '📏'
            },
            'creative': {
                name: 'Creative & Entertainment',
                tools: [
                    'acrostic-poem-generator', 'youtube-converter', 'ebook-reader'
                ],
                icon: '🎨'
            }
        };
    }

    buildRelationshipMap() {
        return {
            // Financial relationships
            '401k-calculator': ['529-calculator', 'bond-yield-calculator', 'paycheck-estimator-texas'],
            '529-calculator': ['401k-calculator', 'home-insurance-calculator'],
            'bond-yield-calculator': ['401k-calculator', 'reverse-mortgage-calculator'],

            // Health relationships
            'a1c-calculator': ['augmentin-pediatric-dose-calculator', 'sleep-cycle-calculator'],
            'army-fitness-calculator': ['1-rep-max-calculator', 'sleep-cycle-calculator'],
            '1-rep-max-calculator': ['army-fitness-calculator', 'puppy-years-to-human-years'],

            // Conversion relationships
            'xml-formatter': ['xml-to-csv-converter', 'yaml-to-json-converter'],
            'xml-to-csv-converter': ['xml-formatter', 'yaml-validator'],
            'yaml-to-json-converter': ['yaml-validator', 'xml-formatter'],
            'yaml-validator': ['yaml-to-json-converter', 'xml-to-csv-converter'],
            'yen-to-usd-converter': ['60k-a-year-is-how-much-an-hour'],

            // Math relationships
            'jacobian-calculator': ['mixed-fraction-calculator', 'three-phase-power-calculator', 'acceleration-calculator', 'z-value-table'],
            'mixed-fraction-calculator': ['jacobian-calculator', 'three-phase-power-calculator', 'acceleration-calculator'],
            'z-value-table': ['jacobian-calculator', 'three-phase-power-calculator'],
            'three-phase-power-calculator': ['jacobian-calculator', 'acceleration-calculator', 'mixed-fraction-calculator'],
            'acceleration-calculator': ['jacobian-calculator', 'three-phase-power-calculator'],

            // Development relationships
            'regex-visualizer': ['yaml-validator', 'xml-formatter'],
            'border-radius-generator': ['ai-logo-generator', 'favicon-converter'],
            'ai-logo-generator': ['border-radius-generator', 'youtube-thumbnail'],

            // Measurement relationships
            'acre-square-footage': ['acreage-calculator', 'stud-spacing-calculator'],
            'acreage-calculator': ['acre-square-footage', 'stud-spacing-calculator'],
            'stud-spacing-calculator': ['acre-square-footage', 'acreage-calculator'],

            // Cross-category relationships
            'paycheck-estimator-texas': ['60k-a-year-is-how-much-an-hour', 'sales-commission-calculator'],
            '60k-a-year-is-how-much-an-hour': ['paycheck-estimator-texas', 'yen-to-usd-converter']
        };
    }

    getRelatedTools(currentTool, limit = 5) {
        const related = this.toolRelationships[currentTool] || [];
        const category = this.getToolCategory(currentTool);

        // Add tools from same category if not enough related tools
        if (related.length < limit && category) {
            const categoryTools = this.toolCategories[category].tools
                .filter(tool => tool !== currentTool && !related.includes(tool));
            related.push(...categoryTools.slice(0, limit - related.length));
        }

        return related.slice(0, limit).map(toolId => ({
            id: toolId,
            name: this.getToolDisplayName(toolId),
            url: `/free-tools/${toolId}/`,
            category: this.getToolCategory(toolId),
            usageCount: this.usageAnalytics[toolId] || 0
        }));
    }

    getToolCategory(toolId) {
        for (const [categoryId, category] of Object.entries(this.toolCategories)) {
            if (category.tools.includes(toolId)) {
                return categoryId;
            }
        }
        return null;
    }

    getToolDisplayName(toolId) {
        return toolId
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    trackToolUsage(toolId) {
        // Update usage analytics
        this.usageAnalytics[toolId] = (this.usageAnalytics[toolId] || 0) + 1;
        localStorage.setItem('toolUsageAnalytics', JSON.stringify(this.usageAnalytics));

        // Update recently used
        this.recentlyUsed = this.recentlyUsed.filter(id => id !== toolId);
        this.recentlyUsed.unshift(toolId);
        this.recentlyUsed = this.recentlyUsed.slice(0, 10);
        localStorage.setItem('recentlyUsedTools', JSON.stringify(this.recentlyUsed));
    }

    toggleFavorite(toolId) {
        if (this.favorites.includes(toolId)) {
            this.favorites = this.favorites.filter(id => id !== toolId);
        } else {
            this.favorites.push(toolId);
        }
        localStorage.setItem('favoriteTools', JSON.stringify(this.favorites));
        return this.favorites.includes(toolId);
    }

    getRecentlyUsed(limit = 5) {
        return this.recentlyUsed.slice(0, limit).map(toolId => ({
            id: toolId,
            name: this.getToolDisplayName(toolId),
            url: `/free-tools/${toolId}/`,
            category: this.getToolCategory(toolId)
        }));
    }

    getFavorites() {
        return this.favorites.map(toolId => ({
            id: toolId,
            name: this.getToolDisplayName(toolId),
            url: `/free-tools/${toolId}/`,
            category: this.getToolCategory(toolId)
        }));
    }

    getToolComparisons(toolId) {
        const category = this.getToolCategory(toolId);
        if (!category) return [];

        const categoryTools = this.toolCategories[category].tools
            .filter(tool => tool !== toolId)
            .map(tool => ({
                id: tool,
                name: this.getToolDisplayName(tool),
                url: `/free-tools/${tool}/`,
                features: this.getToolFeatures(tool)
            }));

        return categoryTools.slice(0, 3);
    }

    getToolFeatures(toolId) {
        const featureMap = {
            '401k-calculator': ['Compound interest', 'Employer matching', 'Tax calculations'],
            '529-calculator': ['Education savings', 'Tax benefits', 'State plans'],
            'a1c-calculator': ['Glucose conversion', 'Risk levels', 'Medical accuracy'],
            'xml-formatter': ['Pretty print', 'Validation', 'Minification'],
            'yaml-validator': ['Syntax check', 'Error detection', 'Best practices'],
            'jacobian-calculator': ['Partial derivatives', 'Matrix determinant', 'Coordinate transformations', 'Step-by-step solutions'],
            'mixed-fraction-calculator': ['Fraction arithmetic', 'Decimal conversion', 'Simplification'],
            'three-phase-power-calculator': ['Electrical calculations', 'Power analysis', 'Circuit optimization'],
            'acceleration-calculator': ['Motion analysis', 'Velocity calculations', 'Physics applications'],
            'z-value-table': ['Statistical analysis', 'Normal distribution', 'Probability calculations'],
            // Add more as needed
        };
        return featureMap[toolId] || ['Advanced calculations', 'User-friendly', 'Accurate results'];
    }

    generateToolNavigation() {
        const categories = Object.entries(this.toolCategories).map(([id, category]) => ({
            id,
            name: category.name,
            icon: category.icon,
            tools: category.tools.map(toolId => ({
                id: toolId,
                name: this.getToolDisplayName(toolId),
                url: `/free-tools/${toolId}/`
            }))
        }));

        return {
            categories,
            recentlyUsed: this.getRecentlyUsed(),
            favorites: this.getFavorites(),
            totalTools: Object.values(this.toolCategories).reduce((sum, cat) => sum + cat.tools.length, 0)
        };
    }
}

// Global instance
window.toolIntegration = new ToolIntegrationSystem();

// Auto-track current tool usage
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const toolMatch = currentPath.match(/\/free-tools\/([^\/]+)\//);
    if (toolMatch) {
        window.toolIntegration.trackToolUsage(toolMatch[1]);
    }
});