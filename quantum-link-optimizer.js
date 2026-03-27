/**
 * QUANTUM INTERNAL LINKING OPTIMIZATION ENGINE
 * Advanced Authority Flow and Semantic Clustering System
 * Quantum Agent Delta - Excellence Protocol
 */

class QuantumLinkOptimizer {
    constructor() {
        this.baseUrl = 'https://zovo.one';
        this.maxLinksPerPage = 8;
        this.semanticThreshold = 0.7;
        this.authorityDecayFactor = 0.85;

        // Tool categories for semantic clustering
        this.toolCategories = {
            'Finance': ['mortgage', 'loan', 'investment', 'savings', 'tax', 'retirement', 'budget'],
            'Health': ['bmi', 'calorie', 'fitness', 'medical', 'dosage', 'health', 'nutrition'],
            'Business': ['payroll', 'invoice', 'profit', 'roi', 'business', 'revenue', 'cost'],
            'Education': ['grade', 'gpa', 'student', 'academic', 'learning', 'study'],
            'Utilities': ['converter', 'generator', 'formatter', 'validator', 'analyzer'],
            'Construction': ['concrete', 'materials', 'building', 'construction', 'renovation'],
            'Engineering': ['calculator', 'formula', 'technical', 'measurement', 'conversion']
        };

        // High-authority pages that should receive more internal links
        this.authorityPages = [
            '/free-tools/',
            '/articles/',
            '/finance-tools/',
            '/health-tools/',
            '/business-tools/'
        ];
    }

    /**
     * Generate quantum-optimized internal linking strategy
     * @param {Array} pages - All site pages with metadata
     * @returns {Object} Complete linking strategy
     */
    generateQuantumLinkingStrategy(pages) {
        const semanticClusters = this.createSemanticClusters(pages);
        const authorityFlow = this.calculateAuthorityFlow(pages);
        const linkingMatrix = this.buildLinkingMatrix(pages, semanticClusters, authorityFlow);

        return {
            clusters: semanticClusters,
            authorityFlow: authorityFlow,
            linkingMatrix: linkingMatrix,
            recommendations: this.generateLinkingRecommendations(linkingMatrix)
        };
    }

    /**
     * Create semantic clusters based on content similarity
     * @param {Array} pages - All site pages
     * @returns {Object} Semantic clusters
     */
    createSemanticClusters(pages) {
        const clusters = {};

        // Initialize category clusters
        Object.keys(this.toolCategories).forEach(category => {
            clusters[category] = [];
        });

        // Assign pages to clusters based on semantic analysis
        pages.forEach(page => {
            const categories = this.analyzePageSemantics(page);
            categories.forEach(category => {
                if (clusters[category]) {
                    clusters[category].push({
                        ...page,
                        semanticScore: this.calculateSemanticScore(page, category)
                    });
                }
            });
        });

        // Sort clusters by semantic score
        Object.keys(clusters).forEach(category => {
            clusters[category].sort((a, b) => b.semanticScore - a.semanticScore);
        });

        return clusters;
    }

    /**
     * Analyze page semantics to determine categories
     * @param {Object} page - Page data
     * @returns {Array} Matching categories
     */
    analyzePageSemantics(page) {
        const { title, description, keywords, url, content } = page;
        const textToAnalyze = `${title} ${description} ${keywords} ${url}`.toLowerCase();

        const matchingCategories = [];

        Object.keys(this.toolCategories).forEach(category => {
            const categoryKeywords = this.toolCategories[category];
            const matches = categoryKeywords.filter(keyword =>
                textToAnalyze.includes(keyword.toLowerCase())
            ).length;

            if (matches > 0) {
                matchingCategories.push({
                    category: category,
                    score: matches / categoryKeywords.length
                });
            }
        });

        // Return top matching categories
        return matchingCategories
            .sort((a, b) => b.score - a.score)
            .slice(0, 2)
            .map(match => match.category);
    }

    /**
     * Calculate semantic similarity score
     * @param {Object} page - Page data
     * @param {string} category - Target category
     * @returns {number} Semantic score
     */
    calculateSemanticScore(page, category) {
        const categoryKeywords = this.toolCategories[category];
        const pageText = `${page.title} ${page.description} ${page.keywords}`.toLowerCase();

        let matches = 0;
        let totalKeywords = categoryKeywords.length;

        categoryKeywords.forEach(keyword => {
            if (pageText.includes(keyword.toLowerCase())) {
                matches++;
            }
        });

        // Boost score for exact category matches
        if (page.category && page.category.toLowerCase() === category.toLowerCase()) {
            matches += 2;
        }

        return Math.min(1.0, matches / totalKeywords);
    }

    /**
     * Calculate authority flow across pages
     * @param {Array} pages - All site pages
     * @returns {Object} Authority flow data
     */
    calculateAuthorityFlow(pages) {
        const authorityScores = {};

        // Initialize authority scores
        pages.forEach(page => {
            let baseAuthority = 0.5; // Default authority

            // Boost authority for specific page types
            if (this.authorityPages.some(authPage => page.url.includes(authPage))) {
                baseAuthority = 0.9;
            }

            // Boost based on traffic and engagement
            if (page.traffic > 1000) baseAuthority += 0.1;
            if (page.engagement > 0.7) baseAuthority += 0.1;
            if (page.backlinks > 10) baseAuthority += 0.1;

            // Category-specific authority boosts
            if (page.category === 'Finance') baseAuthority += 0.05;
            if (page.type === 'article') baseAuthority += 0.05;

            authorityScores[page.url] = Math.min(1.0, baseAuthority);
        });

        return authorityScores;
    }

    /**
     * Build comprehensive linking matrix
     * @param {Array} pages - All site pages
     * @param {Object} clusters - Semantic clusters
     * @param {Object} authorityFlow - Authority scores
     * @returns {Object} Linking matrix
     */
    buildLinkingMatrix(pages, clusters, authorityFlow) {
        const matrix = {};

        pages.forEach(sourcePage => {
            matrix[sourcePage.url] = {
                page: sourcePage,
                recommendedLinks: [],
                linkTypes: {}
            };

            // Find related pages in same semantic cluster
            const sourceCategories = this.analyzePageSemantics(sourcePage);

            sourceCategories.forEach(category => {
                if (clusters[category]) {
                    const relatedPages = clusters[category]
                        .filter(page => page.url !== sourcePage.url)
                        .slice(0, 4); // Top 4 related pages

                    relatedPages.forEach(relatedPage => {
                        const linkStrength = this.calculateLinkStrength(
                            sourcePage,
                            relatedPage,
                            authorityFlow
                        );

                        matrix[sourcePage.url].recommendedLinks.push({
                            targetUrl: relatedPage.url,
                            targetTitle: relatedPage.title,
                            anchorText: this.generateAnchorText(relatedPage),
                            linkStrength: linkStrength,
                            linkType: 'semantic',
                            category: category
                        });
                    });
                }
            });

            // Add authority flow links
            const authorityLinks = this.findAuthorityFlowTargets(sourcePage, pages, authorityFlow);
            authorityLinks.forEach(link => {
                matrix[sourcePage.url].recommendedLinks.push(link);
            });

            // Sort and limit links
            matrix[sourcePage.url].recommendedLinks = matrix[sourcePage.url].recommendedLinks
                .sort((a, b) => b.linkStrength - a.linkStrength)
                .slice(0, this.maxLinksPerPage);

            // Group by link type
            matrix[sourcePage.url].linkTypes = this.groupLinksByType(
                matrix[sourcePage.url].recommendedLinks
            );
        });

        return matrix;
    }

    /**
     * Calculate link strength between two pages
     * @param {Object} sourcePage - Source page
     * @param {Object} targetPage - Target page
     * @param {Object} authorityFlow - Authority scores
     * @returns {number} Link strength score
     */
    calculateLinkStrength(sourcePage, targetPage, authorityFlow) {
        let strength = 0.5;

        // Semantic similarity boost
        const semanticSimilarity = this.calculatePageSimilarity(sourcePage, targetPage);
        strength += semanticSimilarity * 0.3;

        // Authority flow consideration
        const targetAuthority = authorityFlow[targetPage.url] || 0.5;
        strength += targetAuthority * 0.2;

        // Category match boost
        if (sourcePage.category === targetPage.category) {
            strength += 0.2;
        }

        // Traffic and engagement consideration
        if (targetPage.traffic > 500) strength += 0.1;
        if (targetPage.engagement > 0.6) strength += 0.1;

        return Math.min(1.0, strength);
    }

    /**
     * Calculate similarity between two pages
     * @param {Object} page1 - First page
     * @param {Object} page2 - Second page
     * @returns {number} Similarity score
     */
    calculatePageSimilarity(page1, page2) {
        const text1 = `${page1.title} ${page1.description} ${page1.keywords}`.toLowerCase();
        const text2 = `${page2.title} ${page2.description} ${page2.keywords}`.toLowerCase();

        const words1 = new Set(text1.split(/\\s+/));
        const words2 = new Set(text2.split(/\\s+/));

        const intersection = new Set([...words1].filter(x => words2.has(x)));
        const union = new Set([...words1, ...words2]);

        return intersection.size / union.size;
    }

    /**
     * Find authority flow target pages
     * @param {Object} sourcePage - Source page
     * @param {Array} allPages - All site pages
     * @param {Object} authorityFlow - Authority scores
     * @returns {Array} Authority flow links
     */
    findAuthorityFlowTargets(sourcePage, allPages, authorityFlow) {
        const authorityLinks = [];

        // Link to high-authority pages in same category
        const highAuthorityPages = allPages
            .filter(page => page.url !== sourcePage.url)
            .filter(page => authorityFlow[page.url] > 0.8)
            .slice(0, 2);

        highAuthorityPages.forEach(page => {
            authorityLinks.push({
                targetUrl: page.url,
                targetTitle: page.title,
                anchorText: this.generateAnchorText(page),
                linkStrength: authorityFlow[page.url],
                linkType: 'authority',
                category: page.category
            });
        });

        return authorityLinks;
    }

    /**
     * Generate contextual anchor text
     * @param {Object} targetPage - Target page
     * @returns {string} Optimized anchor text
     */
    generateAnchorText(targetPage) {
        const { title, keywords, category } = targetPage;

        // Extract primary keyword from title
        const titleWords = title.toLowerCase().split(' ');
        const stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'];
        const meaningfulWords = titleWords.filter(word => !stopWords.includes(word));

        // Generate variations
        const variations = [
            meaningfulWords.slice(0, 3).join(' '),
            title.split(' - ')[0],
            keywords.split(',')[0].trim(),
            `${category.toLowerCase()} calculator`,
            meaningfulWords.slice(0, 2).join(' ')
        ];

        // Return the shortest meaningful variation
        return variations
            .filter(text => text.length > 0 && text.length < 50)
            .sort((a, b) => a.length - b.length)[0] || title.substring(0, 30);
    }

    /**
     * Group links by type for better organization
     * @param {Array} links - Recommended links
     * @returns {Object} Links grouped by type
     */
    groupLinksByType(links) {
        const grouped = {
            semantic: [],
            authority: [],
            category: []
        };

        links.forEach(link => {
            if (grouped[link.linkType]) {
                grouped[link.linkType].push(link);
            }
        });

        return grouped;
    }

    /**
     * Generate HTML for internal links section
     * @param {Object} linkData - Link data for a page
     * @returns {string} HTML for internal links
     */
    generateLinksHTML(linkData) {
        if (!linkData.recommendedLinks || linkData.recommendedLinks.length === 0) {
            return '';
        }

        const links = linkData.recommendedLinks;

        return `
<!-- Quantum-Optimized Internal Links -->
<section class="quantum-internal-links" style="margin: 2rem 0; padding: 1.5rem; background: #0a0a0f; border: 1px solid #1a1a2e; border-radius: 12px;">
    <h3 style="color: #00ff88; margin-bottom: 1rem; font-size: 1.1rem;">Related Tools & Resources</h3>
    <div class="link-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        ${links.map(link => `
        <a href="${link.targetUrl}" class="internal-link-card" style="display: block; padding: 1rem; background: #12121a; border: 1px solid #1e1e2e; border-radius: 8px; text-decoration: none; transition: border-color 0.2s;" onmouseover="this.style.borderColor='#00ff88'" onmouseout="this.style.borderColor='#1e1e2e'">
            <div style="color: #00ccff; font-weight: 600; margin-bottom: 0.5rem;">${link.anchorText}</div>
            <div style="color: #a0a0b0; font-size: 0.9rem;">${link.targetTitle}</div>
            <div style="color: #666; font-size: 0.8rem; margin-top: 0.5rem;">${link.category} • ${link.linkType}</div>
        </a>`).join('')}
    </div>
</section>`;
    }

    /**
     * Generate linking recommendations report
     * @param {Object} linkingMatrix - Complete linking matrix
     * @returns {Object} Optimization recommendations
     */
    generateLinkingRecommendations(linkingMatrix) {
        const recommendations = {
            totalPages: Object.keys(linkingMatrix).length,
            totalLinks: 0,
            averageLinksPerPage: 0,
            strongestClusters: [],
            weakestPages: [],
            authorityFlowOptimization: []
        };

        // Calculate total links and identify patterns
        Object.keys(linkingMatrix).forEach(pageUrl => {
            const pageData = linkingMatrix[pageUrl];
            recommendations.totalLinks += pageData.recommendedLinks.length;

            // Identify pages with insufficient links
            if (pageData.recommendedLinks.length < 3) {
                recommendations.weakestPages.push({
                    url: pageUrl,
                    linkCount: pageData.recommendedLinks.length,
                    title: pageData.page.title
                });
            }
        });

        recommendations.averageLinksPerPage = Math.round(
            recommendations.totalLinks / recommendations.totalPages
        );

        return recommendations;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumLinkOptimizer;
}

/**
 * QUANTUM LINK OPTIMIZER USAGE EXAMPLE
 *
 * const linkOptimizer = new QuantumLinkOptimizer();
 *
 * const pages = [
 *     {
 *         url: 'https://zovo.one/free-tools/mortgage-calculator/',
 *         title: 'Mortgage Calculator - Monthly Payment Calculator',
 *         description: 'Calculate monthly mortgage payments with taxes and insurance',
 *         keywords: 'mortgage calculator, home loan, monthly payment',
 *         category: 'Finance',
 *         type: 'tool',
 *         traffic: 5000,
 *         engagement: 0.8,
 *         backlinks: 25
 *     }
 * ];
 *
 * const linkingStrategy = linkOptimizer.generateQuantumLinkingStrategy(pages);
 * console.log(linkingStrategy);
 *
 * // Generate HTML for a specific page
 * const linkData = linkingStrategy.linkingMatrix['https://zovo.one/free-tools/mortgage-calculator/'];
 * const linksHTML = linkOptimizer.generateLinksHTML(linkData);
 * console.log(linksHTML);
 */