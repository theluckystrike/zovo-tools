#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Audit criteria configuration
const AUDIT_CRITERIA = {
    // Content depth (5 points)
    WORD_COUNT_3000: { weight: 1, description: "3000+ words" },
    WORD_COUNT_2000: { weight: 1, description: "2000+ words (minimum)" },
    HAS_TABLES: { weight: 1, description: "Contains tables" },
    HAS_CODE_BLOCKS: { weight: 1, description: "Contains code examples" },
    HAS_FAQ: { weight: 1, description: "Has FAQ section" },

    // SEO (5 points)
    HAS_CANONICAL: { weight: 1, description: "Canonical URL" },
    HAS_OG_TAGS: { weight: 1, description: "Open Graph tags" },
    HAS_SCHEMA: { weight: 1, description: "Schema markup" },
    HAS_H1: { weight: 1, description: "H1 tag present" },
    HAS_META_DESC: { weight: 1, description: "Meta description" },

    // Enrichment (3 points)
    HAS_TOOL_LINKS: { weight: 1, description: "Links to Zovo tools" },
    HAS_WIKIPEDIA_REFS: { weight: 1, description: "Wikipedia references" },
    HAS_STACKOVERFLOW_REFS: { weight: 1, description: "StackOverflow references" },

    // Branding (2 points)
    HAS_ZOVO_NAVBAR: { weight: 1, description: "Zovo navbar" },
    HAS_MICHAEL_LIP_AUTHOR: { weight: 1, description: "Michael Lip author attribution" },

    // Anti-AI (1 point)
    NO_BOLD_TAGS: { weight: 1, description: "No <b> or <strong> tags" }
};

const MAX_SCORE = Object.keys(AUDIT_CRITERIA).length;

function countWords(text) {
    return text.replace(/\s+/g, ' ').trim().split(' ').filter(word => word.length > 0).length;
}

function auditArticle(articlePath) {
    const htmlPath = path.join(articlePath, 'index.html');

    if (!fs.existsSync(htmlPath)) {
        return {
            error: 'No index.html found',
            score: 0,
            maxScore: MAX_SCORE,
            issues: ['Missing index.html file']
        };
    }

    const htmlContent = fs.readFileSync(htmlPath, 'utf8');
    const dom = new JSDOM(htmlContent);
    const document = dom.window.document;

    const results = {
        score: 0,
        maxScore: MAX_SCORE,
        issues: [],
        passes: [],
        wordCount: 0
    };

    // Get text content for word counting
    const textContent = document.body ? document.body.textContent : '';
    results.wordCount = countWords(textContent);

    // Check each criterion

    // 1. Word count 3000+
    if (results.wordCount >= 3000) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.WORD_COUNT_3000.description);
    } else {
        results.issues.push(`Word count: ${results.wordCount} (need 3000+)`);
    }

    // 2. Word count 2000+ (minimum)
    if (results.wordCount >= 2000) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.WORD_COUNT_2000.description);
    } else {
        results.issues.push(`Word count: ${results.wordCount} (need 2000+ minimum)`);
    }

    // 3. Has tables
    const tables = document.querySelectorAll('table');
    if (tables.length > 0) {
        results.score++;
        results.passes.push(`${AUDIT_CRITERIA.HAS_TABLES.description} (${tables.length} found)`);
    } else {
        results.issues.push('No tables found');
    }

    // 4. Has code blocks
    const codeBlocks = document.querySelectorAll('pre, code, .code-block');
    if (codeBlocks.length > 0) {
        results.score++;
        results.passes.push(`${AUDIT_CRITERIA.HAS_CODE_BLOCKS.description} (${codeBlocks.length} found)`);
    } else {
        results.issues.push('No code blocks found');
    }

    // 5. Has FAQ
    const faqElements = document.querySelectorAll('[class*="faq"], [id*="faq"], h2, h3, h4');
    let hasFAQ = false;
    faqElements.forEach(el => {
        if (el.textContent.toLowerCase().includes('faq') ||
            el.textContent.toLowerCase().includes('frequently asked') ||
            el.textContent.toLowerCase().includes('common questions')) {
            hasFAQ = true;
        }
    });
    if (hasFAQ) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_FAQ.description);
    } else {
        results.issues.push('No FAQ section found');
    }

    // 6. Canonical URL
    const canonical = document.querySelector('link[rel="canonical"]');
    if (canonical && canonical.href && canonical.href.includes('zovo.one/free-tools/articles/')) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_CANONICAL.description);
    } else {
        results.issues.push('Missing or incorrect canonical URL');
    }

    // 7. Open Graph tags
    const ogTags = document.querySelectorAll('meta[property^="og:"]');
    if (ogTags.length >= 3) { // title, description, url minimum
        results.score++;
        results.passes.push(`${AUDIT_CRITERIA.HAS_OG_TAGS.description} (${ogTags.length} found)`);
    } else {
        results.issues.push(`Insufficient Open Graph tags (${ogTags.length}/3 minimum)`);
    }

    // 8. Schema markup
    const schemaElements = document.querySelectorAll('[type="application/ld+json"], [itemscope], [vocab]');
    if (schemaElements.length > 0) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_SCHEMA.description);
    } else {
        results.issues.push('No schema markup found');
    }

    // 9. H1 tag
    const h1 = document.querySelector('h1');
    if (h1) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_H1.description);
    } else {
        results.issues.push('No H1 tag found');
    }

    // 10. Meta description
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && metaDesc.content && metaDesc.content.length > 100) {
        results.score++;
        results.passes.push(`${AUDIT_CRITERIA.HAS_META_DESC.description} (${metaDesc.content.length} chars)`);
    } else {
        results.issues.push('Missing or short meta description');
    }

    // 11. Tool links
    const links = document.querySelectorAll('a[href]');
    let hasToolLinks = false;
    links.forEach(link => {
        if (link.href.includes('zovo.one') || link.href.includes('/tools/') || link.href.includes('../')) {
            hasToolLinks = true;
        }
    });
    if (hasToolLinks) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_TOOL_LINKS.description);
    } else {
        results.issues.push('No links to Zovo tools found');
    }

    // 12. Wikipedia references
    let hasWikipedia = false;
    links.forEach(link => {
        if (link.href.includes('wikipedia.org')) {
            hasWikipedia = true;
        }
    });
    if (hasWikipedia) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_WIKIPEDIA_REFS.description);
    } else {
        results.issues.push('No Wikipedia references found');
    }

    // 13. StackOverflow references
    let hasStackOverflow = false;
    links.forEach(link => {
        if (link.href.includes('stackoverflow.com') || link.href.includes('stackexchange.com')) {
            hasStackOverflow = true;
        }
    });
    if (hasStackOverflow) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_STACKOVERFLOW_REFS.description);
    } else {
        results.issues.push('No StackOverflow references found');
    }

    // 14. Zovo navbar
    const navbar = document.querySelector('nav, .navbar, header');
    let hasZovoNavbar = false;
    if (navbar && navbar.innerHTML.toLowerCase().includes('zovo')) {
        hasZovoNavbar = true;
    }
    if (hasZovoNavbar) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_ZOVO_NAVBAR.description);
    } else {
        results.issues.push('No Zovo navbar found');
    }

    // 15. Michael Lip author
    const hasMichaelLip = htmlContent.toLowerCase().includes('michael lip') ||
                         htmlContent.toLowerCase().includes('author: michael');
    if (hasMichaelLip) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.HAS_MICHAEL_LIP_AUTHOR.description);
    } else {
        results.issues.push('No Michael Lip author attribution found');
    }

    // 16. No bold tags (anti-AI)
    const boldTags = document.querySelectorAll('b, strong');
    if (boldTags.length === 0) {
        results.score++;
        results.passes.push(AUDIT_CRITERIA.NO_BOLD_TAGS.description);
    } else {
        results.issues.push(`Found ${boldTags.length} bold tags (anti-AI violation)`);
    }

    return results;
}

function main() {
    const articlesDir = './articles';
    const auditResults = {};

    if (!fs.existsSync(articlesDir)) {
        console.error('Articles directory not found');
        process.exit(1);
    }

    const articles = fs.readdirSync(articlesDir)
        .filter(item => {
            const itemPath = path.join(articlesDir, item);
            return fs.statSync(itemPath).isDirectory();
        });

    console.log(`🔍 Auditing ${articles.length} articles...`);

    let totalScore = 0;
    let totalMaxScore = 0;
    let thinArticles = [];
    let lowScoreArticles = [];

    articles.forEach(articleName => {
        const articlePath = path.join(articlesDir, articleName);
        console.log(`\nAuditing: ${articleName}`);

        const result = auditArticle(articlePath);
        auditResults[articleName] = result;

        totalScore += result.score;
        totalMaxScore += result.maxScore;

        if (result.wordCount < 2000) {
            thinArticles.push({ name: articleName, wordCount: result.wordCount });
        }

        if (result.score < 10) {
            lowScoreArticles.push({ name: articleName, score: result.score, maxScore: result.maxScore });
        }

        console.log(`  Score: ${result.score}/${result.maxScore} (${Math.round(result.score/result.maxScore*100)}%)`);
        console.log(`  Words: ${result.wordCount}`);

        if (result.issues.length > 0) {
            console.log(`  Issues: ${result.issues.slice(0, 3).join(', ')}${result.issues.length > 3 ? '...' : ''}`);
        }
    });

    // Generate summary
    const avgScore = totalScore / articles.length;
    const avgPercentage = Math.round(avgScore / MAX_SCORE * 100);

    console.log(`\n📊 AUDIT SUMMARY`);
    console.log(`================`);
    console.log(`Articles audited: ${articles.length}`);
    console.log(`Average score: ${avgScore.toFixed(1)}/${MAX_SCORE} (${avgPercentage}%)`);
    console.log(`Thin articles (<2000 words): ${thinArticles.length}`);
    console.log(`Low score articles (<10/16): ${lowScoreArticles.length}`);

    if (thinArticles.length > 0) {
        console.log(`\n📏 THIN ARTICLES:`);
        thinArticles.forEach(article => {
            console.log(`  ${article.name}: ${article.wordCount} words`);
        });
    }

    if (lowScoreArticles.length > 0) {
        console.log(`\n⚠️  LOW SCORE ARTICLES:`);
        lowScoreArticles.forEach(article => {
            console.log(`  ${article.name}: ${article.score}/${article.maxScore}`);
        });
    }

    // Save detailed results
    const outputPath = './article-audit.json';
    fs.writeFileSync(outputPath, JSON.stringify({
        summary: {
            totalArticles: articles.length,
            averageScore: avgScore,
            averagePercentage: avgPercentage,
            thinArticles: thinArticles.length,
            lowScoreArticles: lowScoreArticles.length
        },
        criteria: AUDIT_CRITERIA,
        results: auditResults,
        thinArticles,
        lowScoreArticles
    }, null, 2));

    console.log(`\n💾 Detailed results saved to: ${outputPath}`);

    return {
        avgScore,
        avgPercentage,
        thinArticles,
        lowScoreArticles,
        auditResults
    };
}

if (require.main === module) {
    main();
}

module.exports = { auditArticle, main };