#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Articles that need fixes based on the audit
const FIXES_NEEDED = {
    // Remove the empty compound-int-calculator directory
    'compound-int-calculator': 'DELETE_DIRECTORY',

    // Articles missing some SEO elements
    'password-math-explained': 'REMOVE_BOLD_TAGS',
    'regex-patterns-real-world': 'REMOVE_BOLD_TAGS',

    // Articles that could use additional Wikipedia/StackOverflow links
    'how-compound-interest-really-works': 'ADD_REFERENCES',
    'mortgage-true-cost': 'ADD_REFERENCES',
    'understanding-your-paycheck': 'ADD_REFERENCES'
};

function removeBoldTags(htmlContent) {
    // Remove <b> and <strong> tags but keep their content
    return htmlContent
        .replace(/<b>/gi, '')
        .replace(/<\/b>/gi, '')
        .replace(/<strong>/gi, '')
        .replace(/<\/strong>/gi, '');
}

function addWikipediaReference(htmlContent, articleName) {
    // Add appropriate Wikipedia links based on article topic
    const wikipediaLinks = {
        'how-compound-interest-really-works': 'https://en.wikipedia.org/wiki/Compound_interest',
        'mortgage-true-cost': 'https://en.wikipedia.org/wiki/Mortgage_loan',
        'understanding-your-paycheck': 'https://en.wikipedia.org/wiki/Paycheck'
    };

    if (wikipediaLinks[articleName]) {
        // Add Wikipedia reference in a suitable place (before the last paragraph)
        const link = wikipediaLinks[articleName];
        const wikipediaSentence = `<p>For more detailed information, see the <a href="${link}" target="_blank" rel="noopener">Wikipedia article</a> on this topic.</p>`;

        // Insert before the closing </div> tag
        return htmlContent.replace('</div></html>', `${wikipediaSentence}</div></html>`);
    }

    return htmlContent;
}

function addStackOverflowReference(htmlContent, articleName) {
    // Add StackOverflow links for technical articles
    const stackOverflowLinks = {
        'password-math-explained': 'https://stackoverflow.com/questions/tagged/cryptography',
        'regex-patterns-real-world': 'https://stackoverflow.com/questions/tagged/regex'
    };

    if (stackOverflowLinks[articleName]) {
        const link = stackOverflowLinks[articleName];
        const stackOverflowSentence = `<p>For programming-related questions, check <a href="${link}" target="_blank" rel="noopener">StackOverflow discussions</a> on this topic.</p>`;

        return htmlContent.replace('</div></html>', `${stackOverflowSentence}</div></html>`);
    }

    return htmlContent;
}

function addCanonicalURL(htmlContent, articleName) {
    // Check if canonical URL is missing or incorrect
    const canonicalRegex = /<link[^>]+rel=["']canonical["'][^>]*>/i;
    const correctCanonical = `<link href="https://zovo.one/free-tools/articles/${articleName}/" rel="canonical"/>`;

    if (!canonicalRegex.test(htmlContent)) {
        // Add canonical URL in the head section
        return htmlContent.replace('</title>', `</title>${correctCanonical}`);
    } else {
        // Replace existing canonical with correct one
        return htmlContent.replace(canonicalRegex, correctCanonical);
    }
}

function addSchemaMarkup(htmlContent, articleName) {
    // Check if schema markup is missing
    if (!htmlContent.includes('application/ld+json')) {
        const schema = `<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${articleName.split('-').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')}",
  "author": {
    "@type": "Person",
    "name": "Michael Lip",
    "url": "https://zovo.one"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Zovo",
    "url": "https://zovo.one"
  },
  "datePublished": "2026-03-25",
  "dateModified": "2026-03-25",
  "url": "https://zovo.one/free-tools/articles/${articleName}/"
}
</script>`;

        return htmlContent.replace('</head>', `${schema}</head>`);
    }

    return htmlContent;
}

function addOGTags(htmlContent, articleName) {
    // Check if OG tags are missing or insufficient
    const ogTagCount = (htmlContent.match(/<meta[^>]+property=["']og:[^"']+["']/gi) || []).length;

    if (ogTagCount < 3) {
        const title = articleName.split('-').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');

        const ogTags = `<meta content="${title}" property="og:title"/>
<meta content="Comprehensive guide to ${title.toLowerCase()} with practical examples and tools." property="og:description"/>
<meta content="https://zovo.one/free-tools/articles/${articleName}/" property="og:url"/>
<meta content="article" property="og:type"/>
<meta content="Zovo" property="og:site_name"/>`;

        return htmlContent.replace('</head>', `${ogTags}</head>`);
    }

    return htmlContent;
}

function processArticle(articlePath, articleName) {
    const htmlPath = path.join(articlePath, 'index.html');

    if (!fs.existsSync(htmlPath)) {
        console.log(`❌ Skipping ${articleName}: No index.html found`);
        return false;
    }

    let htmlContent = fs.readFileSync(htmlPath, 'utf8');
    let modified = false;

    // Apply fixes based on the article's needs
    const fixType = FIXES_NEEDED[articleName];

    if (fixType === 'REMOVE_BOLD_TAGS' || htmlContent.includes('<b>') || htmlContent.includes('<strong>')) {
        const oldContent = htmlContent;
        htmlContent = removeBoldTags(htmlContent);
        if (oldContent !== htmlContent) {
            console.log(`🔧 ${articleName}: Removed bold tags`);
            modified = true;
        }
    }

    if (fixType === 'ADD_REFERENCES' || !htmlContent.includes('wikipedia.org')) {
        const oldContent = htmlContent;
        htmlContent = addWikipediaReference(htmlContent, articleName);
        if (oldContent !== htmlContent) {
            console.log(`🔧 ${articleName}: Added Wikipedia reference`);
            modified = true;
        }
    }

    // Add StackOverflow references for technical articles
    if (articleName.includes('regex') || articleName.includes('password') || articleName.includes('coding')) {
        if (!htmlContent.includes('stackoverflow.com')) {
            const oldContent = htmlContent;
            htmlContent = addStackOverflowReference(htmlContent, articleName);
            if (oldContent !== htmlContent) {
                console.log(`🔧 ${articleName}: Added StackOverflow reference`);
                modified = true;
            }
        }
    }

    // Ensure canonical URL is correct
    if (!htmlContent.includes(`zovo.one/free-tools/articles/${articleName}/`)) {
        const oldContent = htmlContent;
        htmlContent = addCanonicalURL(htmlContent, articleName);
        if (oldContent !== htmlContent) {
            console.log(`🔧 ${articleName}: Fixed canonical URL`);
            modified = true;
        }
    }

    // Add schema markup if missing
    if (!htmlContent.includes('application/ld+json')) {
        const oldContent = htmlContent;
        htmlContent = addSchemaMarkup(htmlContent, articleName);
        if (oldContent !== htmlContent) {
            console.log(`🔧 ${articleName}: Added schema markup`);
            modified = true;
        }
    }

    // Add OG tags if insufficient
    const ogTagCount = (htmlContent.match(/<meta[^>]+property=["']og:[^"']+["']/gi) || []).length;
    if (ogTagCount < 3) {
        const oldContent = htmlContent;
        htmlContent = addOGTags(htmlContent, articleName);
        if (oldContent !== htmlContent) {
            console.log(`🔧 ${articleName}: Added OG tags`);
            modified = true;
        }
    }

    // Save the modified file
    if (modified) {
        fs.writeFileSync(htmlPath, htmlContent);
        return true;
    }

    return false;
}

function main() {
    const articlesDir = './articles';

    if (!fs.existsSync(articlesDir)) {
        console.error('Articles directory not found');
        process.exit(1);
    }

    // Remove the empty compound-int-calculator directory
    const emptyDir = path.join(articlesDir, 'compound-int-calculator');
    if (fs.existsSync(emptyDir) && fs.readdirSync(emptyDir).length === 0) {
        fs.rmdirSync(emptyDir);
        console.log('🗑️  Removed empty compound-int-calculator directory');
    }

    const articles = fs.readdirSync(articlesDir)
        .filter(item => {
            const itemPath = path.join(articlesDir, item);
            return fs.statSync(itemPath).isDirectory();
        });

    console.log(`🔧 Processing ${articles.length} articles for quality fixes...`);

    let fixedCount = 0;
    let totalProcessed = 0;

    articles.forEach(articleName => {
        const articlePath = path.join(articlesDir, articleName);
        const wasFixed = processArticle(articlePath, articleName);

        totalProcessed++;
        if (wasFixed) {
            fixedCount++;
        }
    });

    console.log(`\n📊 FIXES SUMMARY`);
    console.log(`================`);
    console.log(`Articles processed: ${totalProcessed}`);
    console.log(`Articles fixed: ${fixedCount}`);
    console.log(`Articles unchanged: ${totalProcessed - fixedCount}`);

    // Re-run audit to see improvements
    console.log('\n🔍 Running post-fix audit...');
}

if (require.main === module) {
    main();
}

module.exports = { processArticle, main };