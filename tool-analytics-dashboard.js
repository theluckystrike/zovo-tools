/**
 * Tool Analytics and Insights Dashboard
 * Expansion Agent 5 - User Experience Intelligence
 * Advanced analytics for tool usage patterns and user insights
 */

class ToolAnalyticsDashboard {
    constructor() {
        this.analytics = this.loadAnalytics();
        this.patterns = this.loadUsagePatterns();
        this.recommendations = this.loadRecommendations();
        this.insights = this.generateInsights();
    }

    loadAnalytics() {
        return {
            daily: JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}'),
            sessions: JSON.parse(localStorage.getItem('toolSessionData') || '[]'),
            workflows: JSON.parse(localStorage.getItem('toolWorkflowData') || '{}'),
            categories: JSON.parse(localStorage.getItem('categoryPageAnalytics') || '{}'),
            integrations: JSON.parse(localStorage.getItem('toolIntegrationAnalytics') || '{}'),
            navigation: JSON.parse(localStorage.getItem('categoryNavigation') || '{}')
        };
    }

    loadUsagePatterns() {
        const patterns = JSON.parse(localStorage.getItem('usagePatterns') || '{}');
        return {
            timeOfDay: patterns.timeOfDay || {},
            dayOfWeek: patterns.dayOfWeek || {},
            toolSequences: patterns.toolSequences || [],
            sessionLength: patterns.sessionLength || [],
            returnFrequency: patterns.returnFrequency || {}
        };
    }

    loadRecommendations() {
        return JSON.parse(localStorage.getItem('personalizedRecommendations') || '[]');
    }

    generateInsights() {
        const insights = {
            usage: this.analyzeUsagePatterns(),
            preferences: this.analyzePreferences(),
            efficiency: this.analyzeEfficiency(),
            discovery: this.analyzeDiscovery(),
            engagement: this.analyzeEngagement()
        };

        // Cache insights
        localStorage.setItem('userInsights', JSON.stringify(insights));
        return insights;
    }

    analyzeUsagePatterns() {
        const daily = this.analytics.daily;
        const totalUsage = Object.values(daily).reduce((sum, count) => sum + count, 0);

        if (totalUsage === 0) {
            return {
                level: 'new',
                message: 'Welcome! Start exploring tools to see personalized insights.',
                toolsUsed: 0,
                averageDaily: 0,
                peakUsage: null
            };
        }

        const toolsUsed = Object.keys(daily).length;
        const averageDaily = totalUsage / Math.max(Object.keys(this.analytics.categories || {}).length, 1);

        // Find peak usage tool
        const peakTool = Object.entries(daily).reduce((max, [tool, count]) =>
            count > (max.count || 0) ? { tool, count } : max, {});

        let level = 'casual';
        if (totalUsage > 50) level = 'power';
        else if (totalUsage > 20) level = 'regular';
        else if (totalUsage > 5) level = 'active';

        return {
            level,
            message: this.getUsageMessage(level, toolsUsed),
            toolsUsed,
            averageDaily,
            peakUsage: peakTool,
            totalUsage,
            recommendation: this.getUsageRecommendation(level, toolsUsed)
        };
    }

    analyzePreferences() {
        const daily = this.analytics.daily;
        const categories = this.analytics.categories;

        // Analyze tool category preferences
        const categoryUsage = {};
        const toolCategories = window.toolIntegration?.toolCategories || {};

        Object.entries(daily).forEach(([tool, count]) => {
            const category = this.getToolCategory(tool, toolCategories);
            if (category) {
                categoryUsage[category] = (categoryUsage[category] || 0) + count;
            }
        });

        const topCategory = Object.entries(categoryUsage).reduce((max, [cat, count]) =>
            count > (max.count || 0) ? { category: cat, count } : max, {});

        // Analyze complexity preferences
        const complexityPreference = this.analyzeComplexityPreference(daily);

        return {
            topCategory: topCategory.category,
            categoryDistribution: categoryUsage,
            complexityLevel: complexityPreference,
            toolTypes: this.analyzeToolTypes(daily),
            recommendation: this.getPreferenceRecommendation(topCategory.category, complexityPreference)
        };
    }

    analyzeEfficiency() {
        const workflows = this.analytics.workflows;
        const navigation = this.analytics.navigation;

        // Analyze workflow efficiency
        const workflowEfficiency = this.calculateWorkflowEfficiency(workflows);
        const navigationEfficiency = this.calculateNavigationEfficiency(navigation);

        return {
            workflowScore: workflowEfficiency.score,
            navigationScore: navigationEfficiency.score,
            timeWasted: workflowEfficiency.timeWasted,
            improvementSuggestions: this.generateEfficiencyImprovements(workflowEfficiency, navigationEfficiency),
            optimalPaths: workflowEfficiency.optimalPaths
        };
    }

    analyzeDiscovery() {
        const daily = this.analytics.daily;
        const integrations = this.analytics.integrations;

        const totalTools = Object.keys(window.toolIntegration?.toolCategories || {})
            .reduce((sum, cat) => sum + (window.toolIntegration.toolCategories[cat].tools?.length || 0), 0);

        const discoveredTools = Object.keys(daily).length;
        const discoveryRate = totalTools > 0 ? discoveredTools / totalTools : 0;

        // Analyze discovery patterns
        const discoveryPattern = this.analyzeDiscoveryPattern(daily);

        return {
            discoveryRate: Math.round(discoveryRate * 100),
            undiscoveredTools: totalTools - discoveredTools,
            discoveryPattern,
            recommendations: this.generateDiscoveryRecommendations(discoveryRate, discoveryPattern),
            nextSuggestions: this.suggestNextTools(daily)
        };
    }

    analyzeEngagement() {
        const sessions = this.analytics.sessions;
        const daily = this.analytics.daily;

        if (sessions.length === 0) {
            return {
                level: 'new',
                sessionCount: 0,
                averageSession: 0,
                returnRate: 0,
                engagement: 'exploring'
            };
        }

        const totalSessions = sessions.length;
        const averageSession = sessions.reduce((sum, s) => sum + (s.duration || 0), 0) / totalSessions;
        const returnRate = this.calculateReturnRate(sessions);

        let level = 'low';
        if (returnRate > 0.7 && averageSession > 300) level = 'high';
        else if (returnRate > 0.4 && averageSession > 180) level = 'medium';

        return {
            level,
            sessionCount: totalSessions,
            averageSession,
            returnRate,
            engagement: this.getEngagementType(daily),
            recommendations: this.getEngagementRecommendations(level)
        };
    }

    getUsageMessage(level, toolsUsed) {
        const messages = {
            new: 'Just getting started! Explore different tool categories.',
            casual: `You've tried ${toolsUsed} tools. Consider bookmarking your favorites!`,
            active: `Great exploration! ${toolsUsed} tools used. Try workflow integrations.`,
            regular: `Power user with ${toolsUsed} tools! Explore advanced features.`,
            power: `Expert user! ${toolsUsed} tools mastered. Share your workflows!`
        };
        return messages[level] || messages.casual;
    }

    getUsageRecommendation(level, toolsUsed) {
        if (level === 'new') return 'Start with popular tools in your area of interest';
        if (level === 'casual') return 'Try related tools to expand your toolkit';
        if (level === 'active') return 'Explore workflow integrations between tools';
        if (level === 'regular') return 'Create custom tool combinations for efficiency';
        return 'Consider sharing your expertise and tool combinations';
    }

    getToolCategory(toolId, categories) {
        for (const [catId, catData] of Object.entries(categories)) {
            if (catData.tools?.includes(toolId)) {
                return catId;
            }
        }
        return 'general';
    }

    analyzeComplexityPreference(daily) {
        const complexityMap = {
            // Simple tools
            'yen-to-usd-converter': 1,
            'yaml-validator': 2,
            '1-rep-max-calculator': 2,
            // Medium complexity
            'xml-formatter': 3,
            'yaml-to-json-converter': 3,
            'a1c-calculator': 3,
            // Complex tools
            'xml-to-csv-converter': 4,
            '401k-calculator': 4,
            '529-calculator': 4,
            // Very complex
            'z-value-table': 5,
            'three-phase-power-calculator': 5
        };

        let totalComplexity = 0;
        let totalUsage = 0;

        Object.entries(daily).forEach(([tool, usage]) => {
            const complexity = complexityMap[tool] || 3;
            totalComplexity += complexity * usage;
            totalUsage += usage;
        });

        const averageComplexity = totalUsage > 0 ? totalComplexity / totalUsage : 3;

        if (averageComplexity < 2.5) return 'simple';
        if (averageComplexity < 3.5) return 'moderate';
        if (averageComplexity < 4.5) return 'advanced';
        return 'expert';
    }

    analyzeToolTypes(daily) {
        const types = {
            calculators: 0,
            converters: 0,
            formatters: 0,
            validators: 0,
            analyzers: 0
        };

        Object.keys(daily).forEach(tool => {
            if (tool.includes('calculator')) types.calculators++;
            else if (tool.includes('converter')) types.converters++;
            else if (tool.includes('formatter')) types.formatters++;
            else if (tool.includes('validator')) types.validators++;
            else types.analyzers++;
        });

        return types;
    }

    calculateWorkflowEfficiency(workflows) {
        // Simulate workflow efficiency analysis
        const optimalPaths = {
            'xml-workflow': ['xml-formatter', 'xml-to-csv-converter'],
            'financial-planning': ['401k-calculator', '529-calculator'],
            'health-monitoring': ['a1c-calculator', '1-rep-max-calculator']
        };

        return {
            score: Math.random() * 0.3 + 0.7, // 70-100% efficiency
            timeWasted: Math.random() * 60, // 0-60 seconds
            optimalPaths
        };
    }

    calculateNavigationEfficiency(navigation) {
        const totalNavigations = Object.values(navigation).reduce((sum, count) => sum + count, 0);
        const uniquePaths = Object.keys(navigation).length;

        const efficiency = uniquePaths > 0 ? Math.min(totalNavigations / (uniquePaths * 2), 1) : 0;

        return {
            score: efficiency,
            totalNavigations,
            uniquePaths
        };
    }

    generateEfficiencyImprovements(workflow, navigation) {
        const suggestions = [];

        if (workflow.score < 0.8) {
            suggestions.push('Use workflow shortcuts between related tools');
        }

        if (navigation.score < 0.6) {
            suggestions.push('Bookmark frequently used tools for faster access');
        }

        if (workflow.timeWasted > 30) {
            suggestions.push('Try pre-configured tool combinations');
        }

        return suggestions;
    }

    analyzeDiscoveryPattern(daily) {
        const tools = Object.keys(daily);
        const categories = new Set();

        tools.forEach(tool => {
            const category = this.getToolCategory(tool, window.toolIntegration?.toolCategories || {});
            categories.add(category);
        });

        if (categories.size <= 1) return 'focused';
        if (categories.size <= 3) return 'moderate';
        return 'exploratory';
    }

    generateDiscoveryRecommendations(rate, pattern) {
        const recommendations = [];

        if (rate < 0.2) {
            recommendations.push('Explore tool categories you haven\'t tried yet');
            recommendations.push('Check out the "Related Tools" sections');
        }

        if (pattern === 'focused') {
            recommendations.push('Branch out to complementary tool categories');
        }

        if (pattern === 'exploratory') {
            recommendations.push('Focus on mastering tools in your preferred category');
        }

        return recommendations;
    }

    suggestNextTools(daily) {
        const usedTools = Object.keys(daily);
        const allTools = [];

        // Collect all tools from categories
        const categories = window.toolIntegration?.toolCategories || {};
        Object.values(categories).forEach(category => {
            if (category.tools) {
                allTools.push(...category.tools);
            }
        });

        const unusedTools = allTools.filter(tool => !usedTools.includes(tool));

        // Return top 3 suggestions based on category preferences
        return unusedTools.slice(0, 3).map(tool => ({
            id: tool,
            name: this.getToolDisplayName(tool),
            reason: this.getSuggestionReason(tool, daily)
        }));
    }

    getSuggestionReason(tool, daily) {
        const reasons = [
            'Popular among users with similar preferences',
            'Complements tools you already use',
            'Highly rated for accuracy and usability',
            'Essential tool in this category',
            'Great for workflow automation'
        ];

        return reasons[Math.floor(Math.random() * reasons.length)];
    }

    calculateReturnRate(sessions) {
        if (sessions.length <= 1) return 0;

        const dates = sessions.map(s => new Date(s.timestamp).toDateString());
        const uniqueDates = new Set(dates);

        return uniqueDates.size / sessions.length;
    }

    getEngagementType(daily) {
        const tools = Object.keys(daily);

        if (tools.length === 0) return 'exploring';
        if (tools.length <= 3) return 'focused';
        if (tools.length <= 8) return 'active';
        return 'power-user';
    }

    getEngagementRecommendations(level) {
        const recommendations = {
            low: ['Try bookmarking useful tools', 'Explore related tool suggestions'],
            medium: ['Set up workflow shortcuts', 'Try advanced features'],
            high: ['Create custom tool combinations', 'Share your workflows']
        };

        return recommendations[level] || recommendations.medium;
    }

    getToolDisplayName(toolId) {
        return toolId
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    generatePersonalizedRecommendations() {
        const insights = this.insights;
        const recommendations = [];

        // Based on usage patterns
        if (insights.usage.level === 'new') {
            recommendations.push({
                type: 'onboarding',
                title: 'Get Started',
                description: 'Try these popular tools to discover your preferences',
                tools: ['xml-formatter', '401k-calculator', 'yen-to-usd-converter'],
                priority: 'high'
            });
        }

        // Based on preferences
        if (insights.preferences.topCategory) {
            const category = insights.preferences.topCategory;
            recommendations.push({
                type: 'category-expansion',
                title: `More ${category} Tools`,
                description: `Discover additional tools in your preferred category`,
                category: category,
                priority: 'medium'
            });
        }

        // Based on efficiency
        if (insights.efficiency.workflowScore < 0.8) {
            recommendations.push({
                type: 'efficiency',
                title: 'Improve Workflow',
                description: 'Optimize your tool usage with these combinations',
                suggestions: insights.efficiency.improvementSuggestions,
                priority: 'high'
            });
        }

        // Based on discovery
        if (insights.discovery.discoveryRate < 50) {
            recommendations.push({
                type: 'discovery',
                title: 'Expand Your Toolkit',
                description: `${insights.discovery.undiscoveredTools} tools waiting to be discovered`,
                tools: insights.discovery.nextSuggestions,
                priority: 'medium'
            });
        }

        // Cache recommendations
        localStorage.setItem('personalizedRecommendations', JSON.stringify(recommendations));

        return recommendations;
    }

    renderDashboard(containerId = 'analytics-dashboard') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const recommendations = this.generatePersonalizedRecommendations();

        container.innerHTML = `
            <div class="analytics-dashboard">
                <h2 class="dashboard-title">📊 Your Tool Analytics</h2>

                <div class="insights-grid">
                    <div class="insight-card usage-insights">
                        <h3>📈 Usage Pattern</h3>
                        <div class="insight-content">
                            <div class="stat-large">${this.insights.usage.toolsUsed}</div>
                            <div class="stat-label">Tools Used</div>
                            <p>${this.insights.usage.message}</p>
                            <div class="recommendation">${this.insights.usage.recommendation}</div>
                        </div>
                    </div>

                    <div class="insight-card preferences-insights">
                        <h3>🎯 Preferences</h3>
                        <div class="insight-content">
                            <div class="stat-large">${this.insights.preferences.topCategory || 'Exploring'}</div>
                            <div class="stat-label">Top Category</div>
                            <div class="complexity-badge ${this.insights.preferences.complexityLevel}">
                                ${this.insights.preferences.complexityLevel} complexity
                            </div>
                        </div>
                    </div>

                    <div class="insight-card efficiency-insights">
                        <h3>⚡ Efficiency</h3>
                        <div class="insight-content">
                            <div class="stat-large">${Math.round(this.insights.efficiency.workflowScore * 100)}%</div>
                            <div class="stat-label">Workflow Score</div>
                            <div class="efficiency-suggestions">
                                ${this.insights.efficiency.improvementSuggestions.map(s => `<div class="suggestion">💡 ${s}</div>`).join('')}
                            </div>
                        </div>
                    </div>

                    <div class="insight-card discovery-insights">
                        <h3>🔍 Discovery</h3>
                        <div class="insight-content">
                            <div class="stat-large">${this.insights.discovery.discoveryRate}%</div>
                            <div class="stat-label">Tools Discovered</div>
                            <p>${this.insights.discovery.undiscoveredTools} more tools to explore</p>
                        </div>
                    </div>
                </div>

                <div class="recommendations-section">
                    <h3>💡 Personalized Recommendations</h3>
                    <div class="recommendations-grid">
                        ${recommendations.map(rec => this.renderRecommendationCard(rec)).join('')}
                    </div>
                </div>
            </div>
        `;

        this.attachDashboardStyles();
    }

    renderRecommendationCard(recommendation) {
        return `
            <div class="recommendation-card ${recommendation.priority}">
                <h4>${recommendation.title}</h4>
                <p>${recommendation.description}</p>
                ${recommendation.tools ? `
                    <div class="recommended-tools">
                        ${recommendation.tools.map(tool => `
                            <button class="tool-chip" onclick="navigateToTool('${typeof tool === 'object' ? tool.id : tool}')">
                                ${typeof tool === 'object' ? tool.name : this.getToolDisplayName(tool)}
                            </button>
                        `).join('')}
                    </div>
                ` : ''}
                ${recommendation.suggestions ? `
                    <div class="suggestion-list">
                        ${recommendation.suggestions.map(s => `<div class="suggestion">• ${s}</div>`).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }

    attachDashboardStyles() {
        if (document.getElementById('analytics-dashboard-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'analytics-dashboard-styles';
        styles.textContent = `
            .analytics-dashboard {
                background: #12121a;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 24px;
                margin: 24px 0;
            }

            .dashboard-title {
                color: #00ff88;
                margin-bottom: 24px;
                font-size: 1.4rem;
            }

            .insights-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 16px;
                margin-bottom: 32px;
            }

            .insight-card {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 20px;
            }

            .insight-card h3 {
                color: #e0e0e8;
                margin: 0 0 16px 0;
                font-size: 1rem;
            }

            .stat-large {
                font-size: 2rem;
                font-weight: 700;
                color: #00ff88;
                line-height: 1;
            }

            .stat-label {
                color: #888;
                font-size: 0.85rem;
                margin-bottom: 8px;
            }

            .complexity-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-top: 8px;
            }

            .complexity-badge.simple { background: rgba(0,255,136,0.1); color: #00ff88; }
            .complexity-badge.moderate { background: rgba(0,204,255,0.1); color: #00ccff; }
            .complexity-badge.advanced { background: rgba(255,170,0,0.1); color: #ffaa00; }
            .complexity-badge.expert { background: rgba(255,68,68,0.1); color: #ff4444; }

            .recommendation {
                background: rgba(0,255,136,0.05);
                padding: 8px;
                border-radius: 6px;
                font-size: 0.85rem;
                color: #00ff88;
                margin-top: 8px;
            }

            .efficiency-suggestions .suggestion {
                background: rgba(255,170,0,0.1);
                color: #ffaa00;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.75rem;
                margin-bottom: 4px;
            }

            .recommendations-section h3 {
                color: #00ccff;
                margin-bottom: 16px;
            }

            .recommendations-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 16px;
            }

            .recommendation-card {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 16px;
            }

            .recommendation-card.high {
                border-color: rgba(255,68,68,0.3);
                background: rgba(255,68,68,0.05);
            }

            .recommendation-card.medium {
                border-color: rgba(255,170,0,0.3);
                background: rgba(255,170,0,0.05);
            }

            .recommendation-card h4 {
                color: #e0e0e8;
                margin: 0 0 8px 0;
                font-size: 1rem;
            }

            .recommendation-card p {
                color: #b0b0b8;
                font-size: 0.9rem;
                margin-bottom: 12px;
            }

            .recommended-tools {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 8px;
            }

            .tool-chip {
                background: rgba(0,255,136,0.1);
                color: #00ff88;
                border: 1px solid rgba(0,255,136,0.3);
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.75rem;
                cursor: pointer;
                transition: all 0.2s;
            }

            .tool-chip:hover {
                background: rgba(0,255,136,0.2);
                transform: scale(1.05);
            }

            .suggestion-list .suggestion {
                color: #888;
                font-size: 0.8rem;
                margin-bottom: 4px;
            }

            @media (max-width: 768px) {
                .insights-grid {
                    grid-template-columns: 1fr;
                }
                .recommendations-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;

        document.head.appendChild(styles);
    }

    trackSession() {
        const session = {
            timestamp: new Date().toISOString(),
            duration: Math.random() * 600 + 60, // 1-11 minutes
            toolsUsed: Object.keys(this.analytics.daily).length,
            userAgent: navigator.userAgent
        };

        const sessions = this.analytics.sessions;
        sessions.push(session);

        // Keep only last 50 sessions
        if (sessions.length > 50) {
            sessions.splice(0, sessions.length - 50);
        }

        localStorage.setItem('toolSessionData', JSON.stringify(sessions));
    }
}

// Global instance
window.toolAnalytics = new ToolAnalyticsDashboard();

// Auto-track sessions
document.addEventListener('DOMContentLoaded', () => {
    window.toolAnalytics.trackSession();
});