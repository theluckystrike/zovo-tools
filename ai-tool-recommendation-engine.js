/**
 * AI-Powered Tool Recommendation Engine
 * Expansion Agent 5 - Intelligent User Experience
 * Machine learning-inspired recommendations based on usage patterns
 */

class AIToolRecommendationEngine {
    constructor() {
        this.userProfile = this.buildUserProfile();
        this.toolGraph = this.buildToolGraph();
        this.contextAnalyzer = new ContextAnalyzer();
        this.temporalAnalyzer = new TemporalAnalyzer();
        this.similarityMatrix = this.computeSimilarityMatrix();
    }

    buildUserProfile() {
        const analytics = JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}');
        const sessions = JSON.parse(localStorage.getItem('toolSessionData') || '[]');
        const preferences = JSON.parse(localStorage.getItem('userPreferences') || '{}');

        return {
            toolUsage: analytics,
            sessionPatterns: this.analyzeSessionPatterns(sessions),
            categoryPreferences: this.calculateCategoryPreferences(analytics),
            complexityLevel: this.inferComplexityLevel(analytics),
            workflowPatterns: this.detectWorkflowPatterns(sessions),
            timePreferences: this.analyzeTimePreferences(sessions),
            expertise: this.assessExpertiseLevel(analytics),
            preferences: preferences
        };
    }

    buildToolGraph() {
        const categories = window.toolIntegration?.toolCategories || {};
        const graph = { nodes: {}, edges: [] };

        // Add tool nodes
        Object.entries(categories).forEach(([categoryId, categoryData]) => {
            if (categoryData.tools) {
                categoryData.tools.forEach(toolId => {
                    graph.nodes[toolId] = {
                        id: toolId,
                        category: categoryId,
                        features: this.getToolFeatures(toolId),
                        complexity: this.getToolComplexity(toolId),
                        popularity: this.getToolPopularity(toolId),
                        keywords: this.getToolKeywords(toolId)
                    };
                });
            }
        });

        // Add relationships (edges)
        graph.edges = this.computeToolRelationships(graph.nodes);

        return graph;
    }

    computeToolRelationships(nodes) {
        const edges = [];
        const nodeIds = Object.keys(nodes);

        for (let i = 0; i < nodeIds.length; i++) {
            for (let j = i + 1; j < nodeIds.length; j++) {
                const tool1 = nodes[nodeIds[i]];
                const tool2 = nodes[nodeIds[j]];

                const similarity = this.calculateToolSimilarity(tool1, tool2);
                if (similarity > 0.3) {
                    edges.push({
                        source: tool1.id,
                        target: tool2.id,
                        weight: similarity,
                        type: this.getRelationshipType(tool1, tool2)
                    });
                }
            }
        }

        return edges;
    }

    calculateToolSimilarity(tool1, tool2) {
        let similarity = 0;

        // Category similarity
        if (tool1.category === tool2.category) {
            similarity += 0.4;
        }

        // Complexity similarity
        const complexityDiff = Math.abs(tool1.complexity - tool2.complexity);
        similarity += Math.max(0, 0.2 - (complexityDiff * 0.1));

        // Keyword similarity
        const keywordSimilarity = this.calculateKeywordSimilarity(tool1.keywords, tool2.keywords);
        similarity += keywordSimilarity * 0.3;

        // Feature similarity
        const featureSimilarity = this.calculateFeatureSimilarity(tool1.features, tool2.features);
        similarity += featureSimilarity * 0.1;

        return Math.min(similarity, 1);
    }

    calculateKeywordSimilarity(keywords1, keywords2) {
        const set1 = new Set(keywords1.map(k => k.toLowerCase()));
        const set2 = new Set(keywords2.map(k => k.toLowerCase()));

        const intersection = new Set([...set1].filter(k => set2.has(k)));
        const union = new Set([...set1, ...set2]);

        return union.size > 0 ? intersection.size / union.size : 0;
    }

    generateRecommendations(context = {}) {
        const recommendations = [];

        // Context-based recommendations
        recommendations.push(...this.getContextualRecommendations(context));

        // Collaborative filtering
        recommendations.push(...this.getCollaborativeRecommendations());

        // Content-based filtering
        recommendations.push(...this.getContentBasedRecommendations());

        // Temporal recommendations
        recommendations.push(...this.getTemporalRecommendations());

        // Serendipity recommendations
        recommendations.push(...this.getSerendipityRecommendations());

        // Merge and rank recommendations
        const rankedRecommendations = this.rankRecommendations(recommendations);

        return rankedRecommendations.slice(0, 10);
    }

    getContextualRecommendations(context) {
        const recommendations = [];
        const currentTime = new Date();

        // Time-based recommendations
        if (currentTime.getHours() >= 9 && currentTime.getHours() <= 17) {
            // Work hours - suggest productivity tools
            recommendations.push(
                { toolId: 'xml-formatter', score: 0.8, reason: 'Developer productivity tool for work hours' },
                { toolId: 'yaml-validator', score: 0.7, reason: 'Configuration validation for development' }
            );
        }

        // Current tool context
        if (context.currentTool) {
            const relatedTools = this.getDirectlyRelatedTools(context.currentTool);
            relatedTools.forEach(tool => {
                recommendations.push({
                    toolId: tool.id,
                    score: 0.9,
                    reason: `Frequently used together with ${context.currentTool}`
                });
            });
        }

        return recommendations;
    }

    getCollaborativeRecommendations() {
        // Simulate collaborative filtering based on user similarity
        const recommendations = [];
        const userProfile = this.userProfile;

        // Find tools used by similar users
        const similarUserPreferences = this.findSimilarUserPreferences();

        similarUserPreferences.forEach(tool => {
            if (!userProfile.toolUsage[tool.id]) {
                recommendations.push({
                    toolId: tool.id,
                    score: 0.7,
                    reason: 'Users with similar preferences also use this tool'
                });
            }
        });

        return recommendations;
    }

    getContentBasedRecommendations() {
        const recommendations = [];
        const userPreferences = this.userProfile.categoryPreferences;

        // Recommend tools from preferred categories
        Object.entries(userPreferences)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 2)
            .forEach(([category, preference]) => {
                const categoryTools = this.getToolsByCategory(category);
                const unusedTools = categoryTools.filter(tool =>
                    !this.userProfile.toolUsage[tool.id]
                );

                unusedTools.slice(0, 3).forEach(tool => {
                    recommendations.push({
                        toolId: tool.id,
                        score: 0.6 + (preference * 0.3),
                        reason: `Matches your preference for ${category} tools`
                    });
                });
            });

        return recommendations;
    }

    getTemporalRecommendations() {
        const recommendations = [];
        const timePatterns = this.userProfile.timePreferences;

        // Recommend tools based on temporal patterns
        const currentHour = new Date().getHours();
        const currentDayType = this.isWeekend() ? 'weekend' : 'weekday';

        if (timePatterns[currentDayType] && timePatterns[currentDayType][currentHour]) {
            const hourlyPreferences = timePatterns[currentDayType][currentHour];

            Object.entries(hourlyPreferences)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 3)
                .forEach(([toolId, frequency]) => {
                    recommendations.push({
                        toolId,
                        score: 0.5 + (frequency * 0.4),
                        reason: `You often use this tool at this time`
                    });
                });
        }

        return recommendations;
    }

    getSerendipityRecommendations() {
        const recommendations = [];
        const allTools = Object.keys(this.toolGraph.nodes);
        const unusedTools = allTools.filter(tool =>
            !this.userProfile.toolUsage[tool] || this.userProfile.toolUsage[tool] < 3
        );

        // Recommend some random high-quality tools for discovery
        const serendipityTools = unusedTools
            .filter(tool => this.toolGraph.nodes[tool].popularity > 0.5)
            .sort(() => Math.random() - 0.5)
            .slice(0, 2);

        serendipityTools.forEach(tool => {
            recommendations.push({
                toolId: tool,
                score: 0.4,
                reason: 'Discover something new - highly rated tool you haven\'t tried'
            });
        });

        return recommendations;
    }

    rankRecommendations(recommendations) {
        // Group by tool ID and merge scores
        const toolMap = {};

        recommendations.forEach(rec => {
            if (!toolMap[rec.toolId]) {
                toolMap[rec.toolId] = {
                    toolId: rec.toolId,
                    totalScore: 0,
                    reasons: [],
                    sourceCount: 0
                };
            }

            toolMap[rec.toolId].totalScore += rec.score;
            toolMap[rec.toolId].reasons.push(rec.reason);
            toolMap[rec.toolId].sourceCount++;
        });

        // Convert to array and calculate final scores
        const ranked = Object.values(toolMap).map(tool => {
            const diversityBonus = Math.min(tool.sourceCount * 0.1, 0.3);
            const finalScore = (tool.totalScore / tool.sourceCount) + diversityBonus;

            return {
                ...tool,
                score: Math.min(finalScore, 1),
                primaryReason: this.selectPrimaryReason(tool.reasons),
                confidence: this.calculateConfidence(tool)
            };
        });

        return ranked.sort((a, b) => b.score - a.score);
    }

    selectPrimaryReason(reasons) {
        // Select the most compelling reason
        const reasonPriority = [
            /frequently used together/i,
            /similar preferences/i,
            /matches your preference/i,
            /often use this tool/i,
            /highly rated/i
        ];

        for (const pattern of reasonPriority) {
            const match = reasons.find(reason => pattern.test(reason));
            if (match) return match;
        }

        return reasons[0] || 'Recommended for you';
    }

    calculateConfidence(tool) {
        // Calculate confidence based on various factors
        let confidence = 0.5;

        // More sources = higher confidence
        confidence += Math.min(tool.sourceCount * 0.1, 0.3);

        // Higher total score = higher confidence
        confidence += tool.totalScore * 0.2;

        return Math.min(confidence, 1);
    }

    // Utility methods
    analyzeSessionPatterns(sessions) {
        const patterns = {
            averageSessionLength: 0,
            toolsPerSession: 0,
            returnFrequency: 0
        };

        if (sessions.length === 0) return patterns;

        patterns.averageSessionLength = sessions.reduce((sum, s) => sum + (s.duration || 0), 0) / sessions.length;
        patterns.toolsPerSession = sessions.reduce((sum, s) => sum + (s.toolsUsed || 0), 0) / sessions.length;

        // Calculate return frequency
        const dates = sessions.map(s => new Date(s.timestamp).toDateString());
        const uniqueDates = new Set(dates);
        patterns.returnFrequency = uniqueDates.size / sessions.length;

        return patterns;
    }

    calculateCategoryPreferences(analytics) {
        const categoryUsage = {};
        const categories = window.toolIntegration?.toolCategories || {};

        Object.entries(analytics).forEach(([toolId, usage]) => {
            const category = this.getToolCategory(toolId, categories);
            categoryUsage[category] = (categoryUsage[category] || 0) + usage;
        });

        // Normalize to percentages
        const total = Object.values(categoryUsage).reduce((sum, val) => sum + val, 0);
        if (total === 0) return {};

        const preferences = {};
        Object.entries(categoryUsage).forEach(([category, usage]) => {
            preferences[category] = usage / total;
        });

        return preferences;
    }

    getToolCategory(toolId, categories) {
        for (const [categoryId, categoryData] of Object.entries(categories)) {
            if (categoryData.tools?.includes(toolId)) {
                return categoryId;
            }
        }
        return 'general';
    }

    inferComplexityLevel(analytics) {
        const complexityMap = {
            'yen-to-usd-converter': 1,
            'yaml-validator': 2,
            '1-rep-max-calculator': 2,
            'xml-formatter': 3,
            'a1c-calculator': 3,
            'xml-to-csv-converter': 4,
            '401k-calculator': 4,
            'z-value-table': 5
        };

        let totalComplexity = 0;
        let totalUsage = 0;

        Object.entries(analytics).forEach(([tool, usage]) => {
            const complexity = complexityMap[tool] || 3;
            totalComplexity += complexity * usage;
            totalUsage += usage;
        });

        return totalUsage > 0 ? totalComplexity / totalUsage : 3;
    }

    detectWorkflowPatterns(sessions) {
        // Simulate workflow pattern detection
        const workflows = [];

        sessions.forEach(session => {
            if (session.toolSequence && session.toolSequence.length > 1) {
                workflows.push(session.toolSequence);
            }
        });

        return this.findCommonSequences(workflows);
    }

    findCommonSequences(workflows) {
        const sequences = {};

        workflows.forEach(workflow => {
            for (let i = 0; i < workflow.length - 1; i++) {
                const sequence = workflow.slice(i, i + 2).join('->');
                sequences[sequence] = (sequences[sequence] || 0) + 1;
            }
        });

        return sequences;
    }

    getToolFeatures(toolId) {
        const featureMap = {
            'xml-formatter': ['validation', 'syntax-highlighting', 'minification'],
            'yaml-validator': ['validation', 'error-detection', 'best-practices'],
            '401k-calculator': ['tax-calculations', 'projections', 'compound-interest'],
            'yen-to-usd-converter': ['real-time-rates', 'currency-conversion']
        };

        return featureMap[toolId] || ['calculation', 'utility'];
    }

    getToolComplexity(toolId) {
        const complexityMap = {
            'yen-to-usd-converter': 1,
            'yaml-validator': 2,
            '1-rep-max-calculator': 2,
            'xml-formatter': 3,
            'a1c-calculator': 3,
            'xml-to-csv-converter': 4,
            '401k-calculator': 4,
            'z-value-table': 5
        };

        return complexityMap[toolId] || 3;
    }

    getToolPopularity(toolId) {
        // Simulate popularity based on usage analytics
        const allUsage = JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}');
        const totalUsage = Object.values(allUsage).reduce((sum, val) => sum + val, 0);

        if (totalUsage === 0) return Math.random() * 0.5 + 0.3; // Random popularity

        const toolUsage = allUsage[toolId] || 0;
        return Math.min(toolUsage / (totalUsage / Object.keys(allUsage).length), 1);
    }

    getToolKeywords(toolId) {
        const keywordMap = {
            'xml-formatter': ['xml', 'format', 'validate', 'developer'],
            'yaml-validator': ['yaml', 'validate', 'configuration', 'syntax'],
            '401k-calculator': ['retirement', 'savings', 'finance', 'tax'],
            'yen-to-usd-converter': ['currency', 'exchange', 'money', 'japan']
        };

        return keywordMap[toolId] || toolId.split('-');
    }

    renderRecommendationWidget(containerId = 'ai-recommendations') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const recommendations = this.generateRecommendations();

        container.innerHTML = `
            <div class="ai-recommendations-widget">
                <h3 class="recommendations-title">🤖 AI Recommendations</h3>
                <div class="recommendations-list">
                    ${recommendations.slice(0, 5).map(rec => this.renderRecommendationItem(rec)).join('')}
                </div>
                <button class="refresh-recommendations" onclick="aiRecommendations.refreshRecommendations()">
                    🔄 Refresh Suggestions
                </button>
            </div>
        `;

        this.attachRecommendationStyles();
    }

    renderRecommendationItem(recommendation) {
        const tool = this.toolGraph.nodes[recommendation.toolId];
        if (!tool) return '';

        const confidenceClass = recommendation.confidence > 0.7 ? 'high' :
                               recommendation.confidence > 0.5 ? 'medium' : 'low';

        return `
            <div class="recommendation-item ${confidenceClass}" onclick="aiRecommendations.selectRecommendation('${recommendation.toolId}')">
                <div class="recommendation-header">
                    <div class="tool-info">
                        <span class="tool-name">${this.getToolDisplayName(recommendation.toolId)}</span>
                        <span class="confidence-badge ${confidenceClass}">
                            ${Math.round(recommendation.confidence * 100)}% match
                        </span>
                    </div>
                    <div class="recommendation-score">
                        ${Math.round(recommendation.score * 100)}
                    </div>
                </div>
                <div class="recommendation-reason">
                    ${recommendation.primaryReason}
                </div>
                <div class="recommendation-actions">
                    <button class="try-tool">Try Tool</button>
                    <button class="learn-more">Learn More</button>
                </div>
            </div>
        `;
    }

    selectRecommendation(toolId) {
        // Track recommendation selection
        this.trackRecommendationClick(toolId);

        // Navigate to tool
        window.location.href = `/free-tools/${toolId}/`;
    }

    refreshRecommendations() {
        this.renderRecommendationWidget();
        this.trackEvent('recommendations_refreshed');
    }

    trackRecommendationClick(toolId) {
        const events = JSON.parse(localStorage.getItem('recommendationEvents') || '[]');
        events.push({
            type: 'recommendation_click',
            toolId: toolId,
            timestamp: new Date().toISOString()
        });

        localStorage.setItem('recommendationEvents', JSON.stringify(events.slice(-100)));
    }

    trackEvent(eventType, data = {}) {
        const events = JSON.parse(localStorage.getItem('aiRecommendationEvents') || '[]');
        events.push({
            type: eventType,
            timestamp: new Date().toISOString(),
            data
        });

        localStorage.setItem('aiRecommendationEvents', JSON.stringify(events.slice(-50)));
    }

    getToolDisplayName(toolId) {
        return toolId
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    attachRecommendationStyles() {
        if (document.getElementById('ai-recommendations-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'ai-recommendations-styles';
        styles.textContent = `
            .ai-recommendations-widget {
                background: linear-gradient(135deg, rgba(138, 43, 226, 0.1) 0%, rgba(75, 0, 130, 0.1) 100%);
                border: 1px solid rgba(138, 43, 226, 0.2);
                border-radius: 16px;
                padding: 20px;
                margin: 20px 0;
            }

            .recommendations-title {
                color: #da70d6;
                margin: 0 0 16px 0;
                font-size: 1.1rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .recommendations-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 16px;
            }

            .recommendation-item {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 16px;
                cursor: pointer;
                transition: all 0.2s ease;
                position: relative;
            }

            .recommendation-item:hover {
                border-color: #da70d6;
                background: rgba(218, 112, 214, 0.05);
                transform: translateY(-2px);
            }

            .recommendation-item.high {
                border-left: 3px solid #00ff88;
            }

            .recommendation-item.medium {
                border-left: 3px solid #ffaa00;
            }

            .recommendation-item.low {
                border-left: 3px solid #ff4444;
            }

            .recommendation-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }

            .tool-info {
                display: flex;
                align-items: center;
                gap: 8px;
                flex: 1;
            }

            .tool-name {
                color: #e0e0e8;
                font-weight: 500;
                font-size: 0.95rem;
            }

            .confidence-badge {
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            }

            .confidence-badge.high {
                background: rgba(0,255,136,0.1);
                color: #00ff88;
            }

            .confidence-badge.medium {
                background: rgba(255,170,0,0.1);
                color: #ffaa00;
            }

            .confidence-badge.low {
                background: rgba(255,68,68,0.1);
                color: #ff4444;
            }

            .recommendation-score {
                background: linear-gradient(135deg, #da70d6, #9370db);
                color: white;
                padding: 4px 8px;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 600;
                min-width: 40px;
                text-align: center;
            }

            .recommendation-reason {
                color: #b0b0b8;
                font-size: 0.85rem;
                margin-bottom: 12px;
                font-style: italic;
            }

            .recommendation-actions {
                display: flex;
                gap: 8px;
            }

            .recommendation-actions button {
                padding: 4px 12px;
                border: 1px solid rgba(218, 112, 214, 0.3);
                background: transparent;
                color: #da70d6;
                border-radius: 6px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s;
            }

            .recommendation-actions button:hover {
                background: rgba(218, 112, 214, 0.1);
            }

            .refresh-recommendations {
                width: 100%;
                padding: 10px;
                background: linear-gradient(135deg, #da70d6, #9370db);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 0.9rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }

            .refresh-recommendations:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(218, 112, 214, 0.3);
            }

            @media (max-width: 768px) {
                .recommendation-header {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 8px;
                }

                .tool-info {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 4px;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

// Context Analyzer helper class
class ContextAnalyzer {
    analyze() {
        return {
            timeOfDay: new Date().getHours(),
            dayOfWeek: new Date().getDay(),
            currentPage: window.location.pathname,
            referrer: document.referrer
        };
    }
}

// Temporal Analyzer helper class
class TemporalAnalyzer {
    analyzeTimePatterns(sessions) {
        const patterns = {
            hourly: {},
            daily: {},
            weekly: {}
        };

        sessions.forEach(session => {
            const date = new Date(session.timestamp);
            const hour = date.getHours();
            const day = date.getDay();
            const week = this.getWeekNumber(date);

            patterns.hourly[hour] = (patterns.hourly[hour] || 0) + 1;
            patterns.daily[day] = (patterns.daily[day] || 0) + 1;
            patterns.weekly[week] = (patterns.weekly[week] || 0) + 1;
        });

        return patterns;
    }

    getWeekNumber(date) {
        const startDate = new Date(date.getFullYear(), 0, 1);
        const diff = date - startDate;
        return Math.ceil(diff / (7 * 24 * 60 * 60 * 1000));
    }
}

// Global instance
window.aiRecommendations = new AIToolRecommendationEngine();