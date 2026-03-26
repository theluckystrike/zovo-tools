/**
 * Tool Comparison System - Feature comparison and decision matrix
 * Expansion Agent 5 - Advanced Integration Enhancement
 */

class ToolComparisonSystem {
    constructor() {
        this.comparisonMatrix = this.buildComparisonMatrix();
        this.featureWeights = this.getFeatureWeights();
    }

    buildComparisonMatrix() {
        return {
            'financial-calculators': {
                category: 'financial',
                tools: {
                    '401k-calculator': {
                        features: {
                            'compound_interest': 5,
                            'employer_matching': 5,
                            'tax_calculations': 5,
                            'withdrawal_planning': 4,
                            'contribution_limits': 5,
                            'mobile_friendly': 4,
                            'data_export': 3,
                            'historical_tracking': 3
                        },
                        strengths: ['Comprehensive retirement planning', 'Tax-advantaged calculations', 'Employer matching scenarios'],
                        limitations: ['Complex for beginners', 'US-focused regulations'],
                        bestFor: 'Long-term retirement planning with employer benefits'
                    },
                    '529-calculator': {
                        features: {
                            'education_savings': 5,
                            'tax_benefits': 5,
                            'state_plans': 4,
                            'investment_growth': 4,
                            'beneficiary_changes': 3,
                            'mobile_friendly': 4,
                            'data_export': 3,
                            'historical_tracking': 3
                        },
                        strengths: ['Education-specific savings', 'State tax benefits', 'Flexible beneficiary options'],
                        limitations: ['Education use restrictions', 'State-specific variations'],
                        bestFor: 'College and education savings planning'
                    },
                    'bond-yield-calculator': {
                        features: {
                            'yield_calculations': 5,
                            'price_analysis': 4,
                            'maturity_planning': 4,
                            'interest_comparison': 5,
                            'risk_assessment': 3,
                            'mobile_friendly': 4,
                            'data_export': 4,
                            'historical_tracking': 2
                        },
                        strengths: ['Fixed income analysis', 'Yield optimization', 'Investment comparison'],
                        limitations: ['Requires bond market knowledge', 'Limited to basic calculations'],
                        bestFor: 'Fixed income investment analysis'
                    }
                }
            },
            'health-calculators': {
                category: 'health',
                tools: {
                    'a1c-calculator': {
                        features: {
                            'glucose_conversion': 5,
                            'risk_assessment': 5,
                            'unit_conversion': 5,
                            'medical_accuracy': 5,
                            'visual_indicators': 4,
                            'mobile_friendly': 4,
                            'data_export': 3,
                            'historical_tracking': 4
                        },
                        strengths: ['Medical-grade accuracy', 'Clear risk visualization', 'Multiple unit support'],
                        limitations: ['Not a replacement for medical advice', 'Basic tracking only'],
                        bestFor: 'Diabetes monitoring and glucose management'
                    },
                    'army-fitness-calculator': {
                        features: {
                            'fitness_scoring': 5,
                            'standard_compliance': 5,
                            'age_adjustment': 5,
                            'progress_tracking': 3,
                            'goal_setting': 4,
                            'mobile_friendly': 4,
                            'data_export': 3,
                            'historical_tracking': 3
                        },
                        strengths: ['Military standard compliance', 'Age-specific scoring', 'Comprehensive fitness metrics'],
                        limitations: ['Military-specific requirements', 'Limited to Army standards'],
                        bestFor: 'Military fitness preparation and assessment'
                    },
                    '1-rep-max-calculator': {
                        features: {
                            'strength_estimation': 5,
                            'multiple_formulas': 4,
                            'exercise_variety': 4,
                            'progression_planning': 4,
                            'safety_guidelines': 3,
                            'mobile_friendly': 5,
                            'data_export': 2,
                            'historical_tracking': 3
                        },
                        strengths: ['Multiple calculation methods', 'Exercise-specific calculations', 'Simple interface'],
                        limitations: ['Estimation only', 'Safety considerations needed'],
                        bestFor: 'Strength training program design'
                    }
                }
            },
            'conversion-tools': {
                category: 'conversion',
                tools: {
                    'xml-formatter': {
                        features: {
                            'syntax_highlighting': 4,
                            'validation': 5,
                            'minification': 4,
                            'error_detection': 5,
                            'large_file_support': 3,
                            'mobile_friendly': 3,
                            'data_export': 5,
                            'batch_processing': 2
                        },
                        strengths: ['Comprehensive XML handling', 'Error detection', 'Multiple output formats'],
                        limitations: ['Large file performance', 'Limited mobile interface'],
                        bestFor: 'XML development and debugging'
                    },
                    'yaml-validator': {
                        features: {
                            'syntax_validation': 5,
                            'error_reporting': 5,
                            'best_practices': 4,
                            'schema_validation': 3,
                            'large_file_support': 3,
                            'mobile_friendly': 3,
                            'data_export': 4,
                            'batch_processing': 2
                        },
                        strengths: ['Accurate validation', 'Clear error messages', 'Best practice suggestions'],
                        limitations: ['Limited schema support', 'Basic mobile interface'],
                        bestFor: 'YAML configuration validation'
                    },
                    'yen-to-usd-converter': {
                        features: {
                            'real_time_rates': 4,
                            'historical_data': 3,
                            'rate_alerts': 2,
                            'multiple_currencies': 2,
                            'accuracy': 5,
                            'mobile_friendly': 5,
                            'data_export': 2,
                            'offline_mode': 1
                        },
                        strengths: ['Real-time exchange rates', 'Simple interface', 'High accuracy'],
                        limitations: ['Limited to JPY-USD', 'No historical analysis'],
                        bestFor: 'Quick currency conversion'
                    }
                }
            },
            'math-tools': {
                category: 'math',
                tools: {
                    'mixed-fraction-calculator': {
                        features: {
                            'fraction_operations': 5,
                            'mixed_numbers': 5,
                            'step_by_step': 4,
                            'simplification': 5,
                            'multiple_formats': 4,
                            'mobile_friendly': 5,
                            'data_export': 3,
                            'educational_value': 5
                        },
                        strengths: ['Complete fraction handling', 'Educational explanations', 'Multiple input formats'],
                        limitations: ['Basic operations only', 'Limited advanced features'],
                        bestFor: 'Educational math and cooking measurements'
                    },
                    'z-value-table': {
                        features: {
                            'statistical_accuracy': 5,
                            'probability_calculation': 5,
                            'critical_values': 5,
                            'confidence_intervals': 4,
                            'interactive_table': 4,
                            'mobile_friendly': 3,
                            'data_export': 4,
                            'educational_value': 4
                        },
                        strengths: ['Statistical precision', 'Comprehensive z-table', 'Academic standard'],
                        limitations: ['Requires statistics knowledge', 'Limited explanations'],
                        bestFor: 'Statistical analysis and hypothesis testing'
                    },
                    'three-phase-power-calculator': {
                        features: {
                            'power_calculations': 5,
                            'voltage_options': 5,
                            'efficiency_factors': 4,
                            'load_analysis': 4,
                            'safety_considerations': 3,
                            'mobile_friendly': 4,
                            'data_export': 4,
                            'professional_accuracy': 5
                        },
                        strengths: ['Professional electrical calculations', 'Multiple configuration support', 'Safety awareness'],
                        limitations: ['Requires electrical knowledge', 'Complex interface'],
                        bestFor: 'Professional electrical engineering'
                    }
                }
            }
        };
    }

    getFeatureWeights() {
        return {
            accuracy: 0.25,
            usability: 0.20,
            features: 0.20,
            mobile_friendly: 0.15,
            data_management: 0.10,
            educational_value: 0.10
        };
    }

    compareTools(toolIds, category = null) {
        if (category) {
            const categoryData = this.comparisonMatrix[category];
            if (!categoryData) return null;

            const tools = toolIds.map(id => ({
                id,
                data: categoryData.tools[id],
                scores: this.calculateToolScore(categoryData.tools[id])
            })).filter(tool => tool.data);

            return this.generateComparisonReport(tools, category);
        }

        // Cross-category comparison
        const tools = [];
        for (const [catId, categoryData] of Object.entries(this.comparisonMatrix)) {
            for (const toolId of toolIds) {
                if (categoryData.tools[toolId]) {
                    tools.push({
                        id: toolId,
                        category: catId,
                        data: categoryData.tools[toolId],
                        scores: this.calculateToolScore(categoryData.tools[toolId])
                    });
                }
            }
        }

        return this.generateComparisonReport(tools);
    }

    calculateToolScore(toolData) {
        if (!toolData || !toolData.features) return null;

        const features = toolData.features;
        const scores = {
            accuracy: (features.medical_accuracy || features.statistical_accuracy || features.accuracy || features.professional_accuracy || 3) / 5,
            usability: (features.mobile_friendly + (features.educational_value || 3)) / 10,
            features: Object.values(features).reduce((sum, val) => sum + val, 0) / (Object.keys(features).length * 5),
            mobile_friendly: features.mobile_friendly / 5,
            data_management: (features.data_export + (features.historical_tracking || 3)) / 10,
            educational_value: (features.educational_value || features.step_by_step || 3) / 5
        };

        const weightedScore = Object.entries(scores).reduce((total, [key, score]) => {
            return total + (score * (this.featureWeights[key] || 0));
        }, 0);

        return {
            individual: scores,
            weighted: weightedScore,
            rating: this.getScoreRating(weightedScore)
        };
    }

    getScoreRating(score) {
        if (score >= 0.9) return { level: 'excellent', emoji: '🌟', description: 'Excellent' };
        if (score >= 0.8) return { level: 'very-good', emoji: '⭐', description: 'Very Good' };
        if (score >= 0.7) return { level: 'good', emoji: '👍', description: 'Good' };
        if (score >= 0.6) return { level: 'fair', emoji: '👌', description: 'Fair' };
        return { level: 'basic', emoji: '📝', description: 'Basic' };
    }

    generateComparisonReport(tools, category = null) {
        if (!tools.length) return null;

        // Sort by weighted score
        tools.sort((a, b) => (b.scores?.weighted || 0) - (a.scores?.weighted || 0));

        const report = {
            category,
            tools: tools.map(tool => ({
                id: tool.id,
                name: this.getToolDisplayName(tool.id),
                category: tool.category,
                score: tool.scores,
                strengths: tool.data.strengths,
                limitations: tool.data.limitations,
                bestFor: tool.data.bestFor,
                features: tool.data.features,
                recommendation: this.generateRecommendation(tool)
            })),
            summary: this.generateSummary(tools),
            matrix: this.buildFeatureMatrix(tools)
        };

        return report;
    }

    generateRecommendation(tool) {
        const score = tool.scores?.weighted || 0;
        const rating = tool.scores?.rating || { level: 'basic', emoji: '📝', description: 'Basic' };

        let recommendation = `${rating.emoji} ${rating.description} choice`;

        if (score >= 0.8) {
            recommendation += ' - Highly recommended for professional use';
        } else if (score >= 0.7) {
            recommendation += ' - Great for most use cases';
        } else if (score >= 0.6) {
            recommendation += ' - Good for basic needs';
        } else {
            recommendation += ' - Consider alternatives for complex requirements';
        }

        return recommendation;
    }

    generateSummary(tools) {
        const topTool = tools[0];
        const categories = [...new Set(tools.map(t => t.category))];

        return {
            topChoice: {
                id: topTool.id,
                name: this.getToolDisplayName(topTool.id),
                score: topTool.scores?.weighted || 0,
                reason: topTool.data.bestFor
            },
            categorySpread: categories.length,
            averageScore: tools.reduce((sum, tool) => sum + (tool.scores?.weighted || 0), 0) / tools.length,
            recommendations: this.generateCategoryRecommendations(tools)
        };
    }

    generateCategoryRecommendations(tools) {
        const recommendations = [];

        // Find best in each category
        const byCategory = {};
        tools.forEach(tool => {
            const cat = tool.category || 'general';
            if (!byCategory[cat] || (tool.scores?.weighted || 0) > (byCategory[cat].scores?.weighted || 0)) {
                byCategory[cat] = tool;
            }
        });

        Object.entries(byCategory).forEach(([category, tool]) => {
            recommendations.push({
                category,
                tool: tool.id,
                name: this.getToolDisplayName(tool.id),
                reason: `Best ${category} tool for ${tool.data.bestFor}`
            });
        });

        return recommendations;
    }

    buildFeatureMatrix(tools) {
        const allFeatures = new Set();
        tools.forEach(tool => {
            if (tool.data.features) {
                Object.keys(tool.data.features).forEach(feature => allFeatures.add(feature));
            }
        });

        const matrix = {
            features: Array.from(allFeatures),
            tools: tools.map(tool => ({
                id: tool.id,
                name: this.getToolDisplayName(tool.id),
                values: Array.from(allFeatures).map(feature =>
                    tool.data.features?.[feature] || 0
                )
            }))
        };

        return matrix;
    }

    getToolDisplayName(toolId) {
        return toolId
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    findAlternatives(toolId, limit = 3) {
        // Find tools in same category first
        let category = null;
        let currentTool = null;

        for (const [catId, categoryData] of Object.entries(this.comparisonMatrix)) {
            if (categoryData.tools[toolId]) {
                category = catId;
                currentTool = categoryData.tools[toolId];
                break;
            }
        }

        if (!category || !currentTool) return [];

        const categoryTools = Object.entries(this.comparisonMatrix[category].tools)
            .filter(([id]) => id !== toolId)
            .map(([id, data]) => ({
                id,
                data,
                scores: this.calculateToolScore(data),
                similarity: this.calculateSimilarity(currentTool, data)
            }))
            .sort((a, b) => b.similarity - a.similarity)
            .slice(0, limit);

        return categoryTools.map(tool => ({
            id: tool.id,
            name: this.getToolDisplayName(tool.id),
            similarity: tool.similarity,
            reason: this.generateAlternativeReason(currentTool, tool.data),
            score: tool.scores
        }));
    }

    calculateSimilarity(tool1, tool2) {
        const features1 = Object.keys(tool1.features || {});
        const features2 = Object.keys(tool2.features || {});

        const commonFeatures = features1.filter(f => features2.includes(f));
        const totalFeatures = new Set([...features1, ...features2]).size;

        return totalFeatures > 0 ? commonFeatures.length / totalFeatures : 0;
    }

    generateAlternativeReason(currentTool, alternativeTool) {
        const currentStrengths = currentTool.strengths || [];
        const altStrengths = alternativeTool.strengths || [];

        const uniqueStrengths = altStrengths.filter(s =>
            !currentStrengths.some(cs => cs.toLowerCase().includes(s.toLowerCase().split(' ')[0]))
        );

        if (uniqueStrengths.length > 0) {
            return `Offers ${uniqueStrengths[0].toLowerCase()}`;
        }

        return 'Similar functionality with different approach';
    }
}

// Global instance
window.toolComparison = new ToolComparisonSystem();