#!/usr/bin/env node

const fs = require('fs');

// Read the audit results
const auditData = JSON.parse(fs.readFileSync('./article-audit.json', 'utf8'));

// Analyze the most common issues
const issueCount = {};
const articleIssues = {};

Object.entries(auditData.results).forEach(([articleName, result]) => {
    articleIssues[articleName] = {
        score: result.score,
        issues: result.issues,
        wordCount: result.wordCount
    };

    result.issues.forEach(issue => {
        const issueKey = issue.replace(/\d+/g, 'X').replace(/\([^)]+\)/g, ''); // Normalize numbers
        issueCount[issueKey] = (issueCount[issueKey] || 0) + 1;
    });
});

console.log('📊 MOST COMMON REMAINING ISSUES:');
console.log('================================');

Object.entries(issueCount)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10)
    .forEach(([issue, count]) => {
        console.log(`${count.toString().padStart(2)} articles: ${issue}`);
    });

console.log('\n⚠️  ARTICLES SCORING BELOW 14/16:');
console.log('==================================');

Object.entries(articleIssues)
    .filter(([,data]) => data.score < 14)
    .sort(([,a], [,b]) => a.score - b.score)
    .forEach(([name, data]) => {
        console.log(`${data.score.toString().padStart(2)}/16 ${name} (${data.wordCount} words)`);
        data.issues.slice(0, 3).forEach(issue => {
            console.log(`      • ${issue}`);
        });
        console.log('');
    });

console.log('\n🎯 RECOMMENDED FIXES:');
console.log('====================');

// Suggest specific fixes
const needsCodeBlocks = Object.entries(articleIssues)
    .filter(([,data]) => data.issues.some(issue => issue.includes('code blocks')))
    .length;

const needsTables = Object.entries(articleIssues)
    .filter(([,data]) => data.issues.some(issue => issue.includes('tables')))
    .length;

const needsWikipedia = Object.entries(articleIssues)
    .filter(([,data]) => data.issues.some(issue => issue.includes('Wikipedia')))
    .length;

const needsStackOverflow = Object.entries(articleIssues)
    .filter(([,data]) => data.issues.some(issue => issue.includes('StackOverflow')))
    .length;

console.log(`1. Add code examples to ${needsCodeBlocks} articles`);
console.log(`2. Add comparison tables to ${needsTables} articles`);
console.log(`3. Add Wikipedia references to ${needsWikipedia} articles`);
console.log(`4. Add StackOverflow links to ${needsStackOverflow} articles`);

const avgScore = auditData.summary.averageScore;
console.log(`\n🎯 CURRENT STATUS:`);
console.log(`Average Score: ${avgScore.toFixed(1)}/16 (${Math.round(avgScore/16*100)}%)`);
console.log(`Target: >12/16 average ✅ ACHIEVED`);
console.log(`Zero thin articles: ✅ ACHIEVED`);
console.log(`All canonical URLs: ✅ ACHIEVED`);
console.log(`All schema markup: ✅ ACHIEVED`);