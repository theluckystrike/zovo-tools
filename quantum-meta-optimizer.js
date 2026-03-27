/**
 * QUANTUM META TAG OPTIMIZATION ENGINE
 * Advanced SEO Meta Tag Generation System
 * Quantum Agent Delta - Excellence Protocol
 */

class QuantumMetaOptimizer {
    constructor() {
        this.emotionalTriggers = [
            'Ultimate', 'Advanced', 'Professional', 'Instant', 'Precise', 'Expert',
            'Complete', 'Comprehensive', 'Powerful', 'Smart', 'Free', 'Fast'
        ];

        this.actionWords = [
            'Calculate', 'Compute', 'Estimate', 'Analyze', 'Generate', 'Convert',
            'Determine', 'Evaluate', 'Optimize', 'Discover', 'Compare', 'Plan'
        ];

        this.yearTargeting = '2026';
        this.brandName = 'Zovo';
        this.maxTitleLength = 60;
        this.maxDescriptionLength = 160;
    }

    /**
     * Generate quantum-optimized title tags
     * @param {string} toolName - Primary tool name
     * @param {string} category - Tool category
     * @param {string} primaryKeyword - Main target keyword
     * @returns {string} Optimized title tag
     */
    generateQuantumTitle(toolName, category, primaryKeyword) {
        const trigger = this.getRandomElement(this.emotionalTriggers);
        const action = this.getRandomElement(this.actionWords);

        const variations = [
            `${trigger} ${toolName} - ${action} ${category} | ${this.brandName} ${this.yearTargeting}`,
            `${toolName} ${this.yearTargeting} - ${trigger} ${category} Calculator | ${this.brandName}`,
            `${action} ${category} with ${trigger} ${toolName} - Free ${this.yearTargeting} Tool`,
            `${primaryKeyword} - ${trigger} ${toolName} Calculator | ${this.brandName} ${this.yearTargeting}`,
            `${trigger} Free ${toolName} - ${action} ${category} Online | ${this.yearTargeting}`
        ];

        return variations.find(title => title.length <= this.maxTitleLength) || variations[0].substring(0, this.maxTitleLength);
    }

    /**
     * Generate quantum-optimized meta descriptions
     * @param {string} toolName - Primary tool name
     * @param {string} functionality - Tool functionality
     * @param {string} benefits - Key benefits
     * @param {string} keywords - Target keywords
     * @returns {string} Optimized meta description
     */
    generateQuantumDescription(toolName, functionality, benefits, keywords) {
        const socialProof = 'Trusted by professionals worldwide';
        const cta = 'Start calculating now';
        const privacy = 'No signup required';
        const speed = 'Instant results';

        const templates = [
            `${functionality} with our ${toolName.toLowerCase()}. ${benefits}. ${speed}, ${privacy}. ${socialProof}. ${cta}!`,
            `Professional ${toolName.toLowerCase()} for ${this.yearTargeting}. ${functionality}. ${benefits}. Free, accurate, ${speed.toLowerCase()}.`,
            `${speed} ${toolName.toLowerCase()} - ${functionality}. ${benefits}. ${privacy}, no tracking. ${cta}!`,
            `Advanced ${toolName.toLowerCase()} tool. ${functionality} with precision. ${benefits}. Free ${this.yearTargeting} calculator.`,
            `${functionality} using our ${toolName.toLowerCase()}. ${benefits}. Professional-grade, ${speed.toLowerCase()}, ${privacy.toLowerCase()}.`
        ];

        const optimizedDescription = templates.find(desc => desc.length <= this.maxDescriptionLength) ||
                                   templates[0].substring(0, this.maxDescriptionLength);

        // Ensure keywords are included
        return this.ensureKeywordsIncluded(optimizedDescription, keywords);
    }

    /**
     * Generate quantum Open Graph meta tags
     * @param {Object} toolData - Tool information object
     * @returns {Object} Open Graph optimization object
     */
    generateQuantumOpenGraph(toolData) {
        const { toolName, category, description, url, primaryKeyword } = toolData;

        return {
            title: `${toolName} ${this.yearTargeting} - Advanced ${category} Calculator | ${this.brandName}`,
            description: `Professional ${toolName.toLowerCase()} with instant results. ${description} Free, accurate, no signup required.`,
            type: 'website',
            url: url,
            siteName: this.brandName,
            image: this.generateDynamicImageUrl(toolName, category),
            imageAlt: `${toolName} interface preview showing ${category.toLowerCase()} calculations`,
            locale: 'en_US'
        };
    }

    /**
     * Generate quantum Twitter Card meta tags
     * @param {Object} toolData - Tool information object
     * @returns {Object} Twitter Card optimization object
     */
    generateQuantumTwitterCard(toolData) {
        const { toolName, category, description, url } = toolData;

        return {
            card: 'summary_large_image',
            title: `${toolName} Calculator - Professional ${category} Tool ${this.yearTargeting}`,
            description: `Advanced ${toolName.toLowerCase()} for ${this.yearTargeting}. ${description} Free, instant, accurate.`,
            image: this.generateDynamicImageUrl(toolName, category),
            imageAlt: `${toolName} calculator interface preview`,
            creator: '@ZovoTools'
        };
    }

    /**
     * Generate dynamic image URL for social sharing
     * @param {string} toolName - Tool name
     * @param {string} category - Tool category
     * @returns {string} Dynamic image URL
     */
    generateDynamicImageUrl(toolName, category) {
        const encodedParams = encodeURIComponent(JSON.stringify({
            title: toolName,
            subtitle: category,
            year: this.yearTargeting,
            brand: this.brandName,
            style: 'professional'
        }));

        return `https://zovo.one/api/og-image?params=${encodedParams}`;
    }

    /**
     * Generate comprehensive meta tags HTML
     * @param {Object} toolData - Complete tool data
     * @returns {string} Complete meta tags HTML
     */
    generateCompleteMetaTags(toolData) {
        const title = this.generateQuantumTitle(toolData.toolName, toolData.category, toolData.primaryKeyword);
        const description = this.generateQuantumDescription(
            toolData.toolName,
            toolData.functionality,
            toolData.benefits,
            toolData.keywords
        );
        const og = this.generateQuantumOpenGraph(toolData);
        const twitter = this.generateQuantumTwitterCard(toolData);

        return `
<!-- Quantum-Optimized Meta Tags - Generated ${new Date().toISOString()} -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title}</title>
<link rel="canonical" href="${toolData.url}">

<!-- Primary Meta Tags -->
<meta name="title" content="${title}">
<meta name="description" content="${description}">
<meta name="keywords" content="${toolData.keywords}">
<meta name="author" content="${toolData.author || 'Zovo Team'}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow">

<!-- Advanced SEO Meta Tags -->
<meta name="revisit-after" content="7 days">
<meta name="language" content="English">
<meta name="distribution" content="global">
<meta name="rating" content="general">
<meta name="HandheldFriendly" content="True">
<meta name="MobileOptimized" content="320">

<!-- Open Graph Meta Tags -->
<meta property="og:type" content="${og.type}">
<meta property="og:title" content="${og.title}">
<meta property="og:description" content="${og.description}">
<meta property="og:url" content="${og.url}">
<meta property="og:site_name" content="${og.siteName}">
<meta property="og:image" content="${og.image}">
<meta property="og:image:alt" content="${og.imageAlt}">
<meta property="og:locale" content="${og.locale}">

<!-- Twitter Card Meta Tags -->
<meta name="twitter:card" content="${twitter.card}">
<meta name="twitter:title" content="${twitter.title}">
<meta name="twitter:description" content="${twitter.description}">
<meta name="twitter:image" content="${twitter.image}">
<meta name="twitter:image:alt" content="${twitter.imageAlt}">
<meta name="twitter:creator" content="${twitter.creator}">

<!-- Additional SEO Enhancement -->
<meta name="theme-color" content="#00ff88">
<meta name="msapplication-TileColor" content="#00ff88">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
`;
    }

    /**
     * Helper methods
     */
    getRandomElement(array) {
        return array[Math.floor(Math.random() * array.length)];
    }

    ensureKeywordsIncluded(description, keywords) {
        const keywordArray = keywords.split(',').map(k => k.trim());
        let optimizedDescription = description;

        keywordArray.slice(0, 2).forEach(keyword => {
            if (!optimizedDescription.toLowerCase().includes(keyword.toLowerCase())) {
                optimizedDescription = keyword + '. ' + optimizedDescription;
            }
        });

        return optimizedDescription.length <= this.maxDescriptionLength ?
               optimizedDescription :
               optimizedDescription.substring(0, this.maxDescriptionLength);
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumMetaOptimizer;
}

/**
 * QUANTUM META OPTIMIZATION USAGE EXAMPLE
 *
 * const optimizer = new QuantumMetaOptimizer();
 * const toolData = {
 *     toolName: 'Mortgage Points Calculator',
 *     category: 'Mortgage',
 *     functionality: 'Calculate whether buying mortgage discount points saves money',
 *     benefits: 'Compare 0-3 points with breakeven analysis',
 *     keywords: 'mortgage points calculator, discount points, mortgage rate reduction',
 *     primaryKeyword: 'mortgage points calculator',
 *     url: 'https://zovo.one/free-tools/mortgage-points-calculator/',
 *     author: 'Michael Lip'
 * };
 *
 * const metaTags = optimizer.generateCompleteMetaTags(toolData);
 * console.log(metaTags);
 */