/**
 * Universal Tool Navigation System
 * Expansion Agent 5 - Unified User Experience
 * Advanced navigation with search, keyboard shortcuts, and AI-powered suggestions
 */

class UniversalToolNavigation {
    constructor() {
        this.tools = this.loadAllTools();
        this.searchIndex = this.buildSearchIndex();
        this.shortcuts = this.initializeShortcuts();
        this.recentSearches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
        this.quickAccess = JSON.parse(localStorage.getItem('quickAccessTools') || '[]');

        this.init();
    }

    loadAllTools() {
        const toolCategories = window.toolIntegration?.toolCategories || {};
        const allTools = {};

        Object.entries(toolCategories).forEach(([categoryId, categoryData]) => {
            if (categoryData.tools) {
                categoryData.tools.forEach(toolId => {
                    allTools[toolId] = {
                        id: toolId,
                        name: this.getToolDisplayName(toolId),
                        category: categoryId,
                        categoryName: categoryData.name,
                        icon: categoryData.icon,
                        url: `/free-tools/${toolId}/`,
                        keywords: this.generateKeywords(toolId),
                        popularity: this.getToolPopularity(toolId),
                        description: this.getToolDescription(toolId)
                    };
                });
            }
        });

        return allTools;
    }

    buildSearchIndex() {
        const index = {};

        Object.entries(this.tools).forEach(([toolId, tool]) => {
            const searchTerms = [
                tool.name.toLowerCase(),
                tool.category.toLowerCase(),
                tool.categoryName.toLowerCase(),
                ...tool.keywords.map(k => k.toLowerCase())
            ];

            searchTerms.forEach(term => {
                const words = term.split(/\s+/);
                words.forEach(word => {
                    if (word.length > 2) {
                        if (!index[word]) index[word] = [];
                        if (!index[word].includes(toolId)) {
                            index[word].push(toolId);
                        }
                    }
                });
            });
        });

        return index;
    }

    initializeShortcuts() {
        return {
            'ctrl+k': () => this.openSearch(),
            'ctrl+shift+f': () => this.openFavorites(),
            'ctrl+h': () => this.showHistory(),
            'escape': () => this.closeSearch(),
            '/': () => this.focusSearch()
        };
    }

    init() {
        this.createNavigationUI();
        this.bindEvents();
        this.loadQuickAccess();
    }

    createNavigationUI() {
        // Create search overlay
        const searchOverlay = document.createElement('div');
        searchOverlay.id = 'universal-search-overlay';
        searchOverlay.className = 'search-overlay';
        searchOverlay.innerHTML = `
            <div class="search-container">
                <div class="search-header">
                    <div class="search-input-container">
                        <input type="text" id="universal-search-input" placeholder="Search tools... (Press / or Ctrl+K)" autocomplete="off">
                        <div class="search-shortcut">⌘K</div>
                    </div>
                    <button class="search-close" onclick="universalNav.closeSearch()">✕</button>
                </div>

                <div class="search-filters">
                    <button class="filter-btn active" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="calculators">Calculators</button>
                    <button class="filter-btn" data-filter="converters">Converters</button>
                    <button class="filter-btn" data-filter="recent">Recent</button>
                    <button class="filter-btn" data-filter="favorites">Favorites</button>
                </div>

                <div class="search-results" id="search-results"></div>

                <div class="search-footer">
                    <div class="search-tips">
                        <span>💡 Tips: Use keywords, category names, or tool types</span>
                    </div>
                    <div class="search-shortcuts">
                        <span>↑↓ Navigate</span>
                        <span>Enter Open</span>
                        <span>Esc Close</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(searchOverlay);

        // Create quick navigation bar
        this.createQuickNavBar();

        // Attach styles
        this.attachStyles();
    }

    createQuickNavBar() {
        const quickNav = document.createElement('div');
        quickNav.id = 'quick-nav-bar';
        quickNav.className = 'quick-nav-bar';
        quickNav.innerHTML = `
            <div class="quick-nav-content">
                <button class="quick-nav-btn search-trigger" onclick="universalNav.openSearch()" title="Search Tools (Ctrl+K)">
                    🔍 Search
                </button>

                <div class="quick-access-tools" id="quick-access-tools">
                    <!-- Quick access tools will be populated here -->
                </div>

                <div class="nav-actions">
                    <button class="quick-nav-btn" onclick="universalNav.openFavorites()" title="Favorites">
                        ⭐
                    </button>
                    <button class="quick-nav-btn" onclick="universalNav.showHistory()" title="History">
                        🕒
                    </button>
                    <button class="quick-nav-btn" onclick="universalNav.showCategories()" title="Categories">
                        📂
                    </button>
                    <button class="quick-nav-btn analytics-trigger" onclick="universalNav.showAnalytics()" title="Analytics">
                        📊
                    </button>
                </div>
            </div>
        `;

        // Insert at the top of the page
        document.body.insertBefore(quickNav, document.body.firstChild);
    }

    bindEvents() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            const shortcut = this.getShortcutKey(e);
            if (this.shortcuts[shortcut]) {
                e.preventDefault();
                this.shortcuts[shortcut]();
            }
        });

        // Search input events
        const searchInput = document.getElementById('universal-search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.performSearch(e.target.value));
            searchInput.addEventListener('keydown', (e) => this.handleSearchKeydown(e));
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.applyFilter(e.target.dataset.filter));
        });

        // Click outside to close
        document.getElementById('universal-search-overlay').addEventListener('click', (e) => {
            if (e.target.id === 'universal-search-overlay') {
                this.closeSearch();
            }
        });
    }

    getShortcutKey(e) {
        let key = '';
        if (e.ctrlKey || e.metaKey) key += 'ctrl+';
        if (e.shiftKey) key += 'shift+';
        if (e.altKey) key += 'alt+';

        if (e.key === '/') return '/';
        if (e.key === 'Escape') return 'escape';

        key += e.key.toLowerCase();
        return key;
    }

    openSearch() {
        const overlay = document.getElementById('universal-search-overlay');
        const input = document.getElementById('universal-search-input');

        overlay.style.display = 'flex';
        setTimeout(() => {
            input.focus();
            this.showDefaultResults();
        }, 100);

        // Track search opening
        this.trackEvent('search_opened');
    }

    closeSearch() {
        document.getElementById('universal-search-overlay').style.display = 'none';
    }

    focusSearch() {
        if (document.getElementById('universal-search-overlay').style.display !== 'flex') {
            this.openSearch();
        } else {
            document.getElementById('universal-search-input').focus();
        }
    }

    performSearch(query) {
        const resultsContainer = document.getElementById('search-results');

        if (!query.trim()) {
            this.showDefaultResults();
            return;
        }

        const results = this.searchTools(query);
        this.renderSearchResults(results);

        // Track search
        this.trackSearch(query);
    }

    searchTools(query) {
        const queryWords = query.toLowerCase().split(/\s+/);
        const matches = new Map();

        queryWords.forEach(word => {
            if (word.length < 2) return;

            // Exact matches
            if (this.searchIndex[word]) {
                this.searchIndex[word].forEach(toolId => {
                    matches.set(toolId, (matches.get(toolId) || 0) + 10);
                });
            }

            // Partial matches
            Object.keys(this.searchIndex).forEach(indexWord => {
                if (indexWord.includes(word)) {
                    this.searchIndex[indexWord].forEach(toolId => {
                        matches.set(toolId, (matches.get(toolId) || 0) + 5);
                    });
                }
            });
        });

        // Convert to array and sort by relevance
        const results = Array.from(matches.entries())
            .map(([toolId, score]) => ({
                ...this.tools[toolId],
                relevanceScore: score
            }))
            .sort((a, b) => b.relevanceScore - a.relevanceScore)
            .slice(0, 10);

        return results;
    }

    renderSearchResults(results) {
        const container = document.getElementById('search-results');

        if (results.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <div class="no-results-text">No tools found</div>
                    <div class="no-results-suggestion">Try different keywords or browse categories</div>
                </div>
            `;
            return;
        }

        container.innerHTML = results.map((tool, index) => `
            <div class="search-result-item ${index === 0 ? 'selected' : ''}" data-tool-id="${tool.id}" data-index="${index}">
                <div class="result-icon">${tool.icon}</div>
                <div class="result-content">
                    <div class="result-title">${tool.name}</div>
                    <div class="result-category">${tool.categoryName}</div>
                    <div class="result-description">${tool.description}</div>
                </div>
                <div class="result-actions">
                    <button class="quick-action" onclick="universalNav.openTool('${tool.id}')" title="Open Tool">
                        →
                    </button>
                    <button class="quick-action" onclick="universalNav.toggleFavorite('${tool.id}')" title="Add to Favorites">
                        ⭐
                    </button>
                </div>
            </div>
        `).join('');
    }

    showDefaultResults() {
        const favorites = this.getFavoriteTools();
        const recent = this.getRecentTools();
        const popular = this.getPopularTools();

        const container = document.getElementById('search-results');
        container.innerHTML = `
            <div class="default-results">
                ${favorites.length > 0 ? `
                    <div class="result-section">
                        <h3>⭐ Your Favorites</h3>
                        <div class="tool-chips">
                            ${favorites.slice(0, 5).map(tool => `
                                <div class="tool-chip" onclick="universalNav.openTool('${tool.id}')">
                                    ${tool.icon} ${tool.name}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                ${recent.length > 0 ? `
                    <div class="result-section">
                        <h3>🕒 Recently Used</h3>
                        <div class="tool-chips">
                            ${recent.slice(0, 5).map(tool => `
                                <div class="tool-chip" onclick="universalNav.openTool('${tool.id}')">
                                    ${tool.icon} ${tool.name}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                <div class="result-section">
                    <h3>🔥 Popular Tools</h3>
                    <div class="tool-chips">
                        ${popular.slice(0, 8).map(tool => `
                            <div class="tool-chip" onclick="universalNav.openTool('${tool.id}')">
                                ${tool.icon} ${tool.name}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    handleSearchKeydown(e) {
        const results = document.querySelectorAll('.search-result-item');
        if (results.length === 0) return;

        let selectedIndex = -1;
        const selected = document.querySelector('.search-result-item.selected');
        if (selected) {
            selectedIndex = parseInt(selected.dataset.index);
        }

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.selectResult(Math.min(selectedIndex + 1, results.length - 1));
                break;

            case 'ArrowUp':
                e.preventDefault();
                this.selectResult(Math.max(selectedIndex - 1, 0));
                break;

            case 'Enter':
                e.preventDefault();
                if (selected) {
                    this.openTool(selected.dataset.toolId);
                }
                break;
        }
    }

    selectResult(index) {
        document.querySelectorAll('.search-result-item').forEach((item, i) => {
            item.classList.toggle('selected', i === index);
        });
    }

    openTool(toolId) {
        const tool = this.tools[toolId];
        if (tool) {
            // Track usage
            window.toolIntegration?.trackToolUsage(toolId);

            // Add to recent searches
            this.addToRecentSearches(tool);

            // Navigate
            window.location.href = tool.url;
        }
        this.closeSearch();
    }

    addToRecentSearches(tool) {
        this.recentSearches = this.recentSearches.filter(t => t.id !== tool.id);
        this.recentSearches.unshift(tool);
        this.recentSearches = this.recentSearches.slice(0, 10);

        localStorage.setItem('recentSearches', JSON.stringify(this.recentSearches));
    }

    loadQuickAccess() {
        const container = document.getElementById('quick-access-tools');
        if (!container) return;

        const quickTools = this.getQuickAccessTools();

        container.innerHTML = quickTools.map(tool => `
            <button class="quick-tool-btn" onclick="universalNav.openTool('${tool.id}')" title="${tool.name}">
                ${tool.icon}
            </button>
        `).join('');
    }

    getQuickAccessTools() {
        const favorites = this.getFavoriteTools();
        const recent = this.getRecentTools();

        // Combine favorites and recent, prioritize favorites
        const combined = [...favorites.slice(0, 3), ...recent.slice(0, 2)];
        const unique = combined.filter((tool, index, array) =>
            array.findIndex(t => t.id === tool.id) === index
        );

        return unique.slice(0, 4);
    }

    getFavoriteTools() {
        const favorites = JSON.parse(localStorage.getItem('favoriteTools') || '[]');
        return favorites.map(toolId => this.tools[toolId]).filter(Boolean);
    }

    getRecentTools() {
        return this.recentSearches;
    }

    getPopularTools() {
        const analytics = JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}');

        return Object.entries(this.tools)
            .map(([toolId, tool]) => ({
                ...tool,
                usage: analytics[toolId] || 0
            }))
            .sort((a, b) => b.usage - a.usage)
            .slice(0, 10);
    }

    showAnalytics() {
        // Create analytics modal
        const modal = document.createElement('div');
        modal.className = 'analytics-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>📊 Your Analytics Dashboard</h2>
                    <button class="modal-close" onclick="this.closest('.analytics-modal').remove()">✕</button>
                </div>
                <div id="analytics-dashboard"></div>
            </div>
        `;

        document.body.appendChild(modal);

        // Initialize analytics dashboard
        if (window.toolAnalytics) {
            window.toolAnalytics.renderDashboard('analytics-dashboard');
        }

        modal.style.display = 'flex';
    }

    trackEvent(eventType, data = {}) {
        const events = JSON.parse(localStorage.getItem('navigationEvents') || '[]');
        events.push({
            type: eventType,
            timestamp: new Date().toISOString(),
            data
        });

        // Keep only last 100 events
        if (events.length > 100) {
            events.splice(0, events.length - 100);
        }

        localStorage.setItem('navigationEvents', JSON.stringify(events));
    }

    trackSearch(query) {
        this.trackEvent('search', { query });

        const searches = JSON.parse(localStorage.getItem('searchHistory') || '[]');
        searches.unshift({
            query,
            timestamp: new Date().toISOString()
        });

        localStorage.setItem('searchHistory', JSON.stringify(searches.slice(0, 50)));
    }

    getToolDisplayName(toolId) {
        return toolId
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    generateKeywords(toolId) {
        const keywordMap = {
            'xml-formatter': ['xml', 'format', 'beautify', 'validate', 'developer'],
            'yen-to-usd-converter': ['currency', 'exchange', 'japan', 'dollar', 'money'],
            '401k-calculator': ['retirement', 'savings', 'tax', 'finance', 'planning'],
            'a1c-calculator': ['diabetes', 'glucose', 'blood', 'health', 'medical'],
            '1-rep-max-calculator': ['fitness', 'strength', 'workout', 'gym', 'exercise']
        };

        return keywordMap[toolId] || toolId.split('-');
    }

    getToolDescription(toolId) {
        const descriptions = {
            'xml-formatter': 'Format and validate XML with syntax highlighting',
            'yen-to-usd-converter': 'Real-time Japanese Yen to US Dollar conversion',
            '401k-calculator': 'Comprehensive retirement savings calculator',
            'a1c-calculator': 'Convert A1C to average blood glucose levels',
            '1-rep-max-calculator': 'Estimate your one-rep max for strength training'
        };

        return descriptions[toolId] || `Professional ${this.getToolDisplayName(toolId).toLowerCase()}`;
    }

    getToolPopularity(toolId) {
        const analytics = JSON.parse(localStorage.getItem('toolUsageAnalytics') || '{}');
        return analytics[toolId] || 0;
    }

    attachStyles() {
        if (document.getElementById('universal-nav-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'universal-nav-styles';
        styles.textContent = `
            .quick-nav-bar {
                position: fixed;
                top: 60px;
                right: 20px;
                z-index: 999;
                background: rgba(18, 18, 26, 0.95);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 8px;
                display: flex;
                gap: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }

            .quick-nav-btn {
                background: transparent;
                border: none;
                color: #e0e0e8;
                padding: 8px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.85rem;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 4px;
            }

            .quick-nav-btn:hover {
                background: rgba(0,255,136,0.1);
                color: #00ff88;
            }

            .search-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(8px);
                display: none;
                align-items: flex-start;
                justify-content: center;
                padding-top: 100px;
                z-index: 2000;
            }

            .search-container {
                background: #12121a;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 16px;
                width: 90%;
                max-width: 600px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                overflow: hidden;
            }

            .search-header {
                display: flex;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }

            .search-input-container {
                flex: 1;
                position: relative;
            }

            .search-input-container input {
                width: 100%;
                background: transparent;
                border: none;
                color: #e0e0e8;
                font-size: 1.1rem;
                padding: 0;
                outline: none;
            }

            .search-shortcut {
                position: absolute;
                right: 8px;
                top: 50%;
                transform: translateY(-50%);
                color: #888;
                font-size: 0.75rem;
                background: rgba(255,255,255,0.05);
                padding: 2px 6px;
                border-radius: 4px;
            }

            .search-close {
                background: none;
                border: none;
                color: #888;
                font-size: 1.2rem;
                cursor: pointer;
                padding: 4px;
                margin-left: 16px;
            }

            .search-filters {
                display: flex;
                gap: 8px;
                padding: 16px 20px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }

            .filter-btn {
                background: transparent;
                border: 1px solid rgba(255,255,255,0.1);
                color: #888;
                padding: 6px 12px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.85rem;
                transition: all 0.2s;
            }

            .filter-btn:hover,
            .filter-btn.active {
                background: rgba(0,255,136,0.1);
                border-color: #00ff88;
                color: #00ff88;
            }

            .search-results {
                max-height: 400px;
                overflow-y: auto;
                padding: 8px;
            }

            .search-result-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                margin-bottom: 4px;
            }

            .search-result-item:hover,
            .search-result-item.selected {
                background: rgba(0,255,136,0.05);
            }

            .result-icon {
                font-size: 1.2rem;
                width: 24px;
                text-align: center;
            }

            .result-content {
                flex: 1;
                min-width: 0;
            }

            .result-title {
                color: #e0e0e8;
                font-weight: 500;
                font-size: 0.95rem;
            }

            .result-category {
                color: #888;
                font-size: 0.8rem;
            }

            .result-description {
                color: #b0b0b8;
                font-size: 0.85rem;
                margin-top: 2px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .result-actions {
                display: flex;
                gap: 4px;
            }

            .quick-action {
                background: transparent;
                border: 1px solid rgba(255,255,255,0.1);
                color: #888;
                width: 28px;
                height: 28px;
                border-radius: 6px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }

            .quick-action:hover {
                border-color: #00ff88;
                color: #00ff88;
            }

            .search-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 20px;
                border-top: 1px solid rgba(255,255,255,0.06);
                background: rgba(255,255,255,0.02);
            }

            .search-tips {
                color: #888;
                font-size: 0.8rem;
            }

            .search-shortcuts {
                display: flex;
                gap: 12px;
                color: #666;
                font-size: 0.75rem;
            }

            .default-results .result-section {
                margin-bottom: 20px;
            }

            .default-results h3 {
                color: #e0e0e8;
                font-size: 0.9rem;
                margin-bottom: 8px;
                padding-left: 4px;
            }

            .tool-chips {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }

            .tool-chip {
                background: rgba(0,255,136,0.1);
                color: #00ff88;
                border: 1px solid rgba(0,255,136,0.3);
                padding: 6px 10px;
                border-radius: 16px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 4px;
            }

            .tool-chip:hover {
                background: rgba(0,255,136,0.2);
                transform: translateY(-1px);
            }

            .no-results {
                text-align: center;
                padding: 40px 20px;
                color: #888;
            }

            .no-results-icon {
                font-size: 3rem;
                margin-bottom: 16px;
                opacity: 0.5;
            }

            .no-results-text {
                font-size: 1.1rem;
                margin-bottom: 8px;
            }

            .no-results-suggestion {
                font-size: 0.9rem;
                opacity: 0.7;
            }

            .analytics-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(8px);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 2000;
                padding: 20px;
            }

            .analytics-modal .modal-content {
                background: #12121a;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 16px;
                width: 90%;
                max-width: 1000px;
                max-height: 90vh;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }

            .analytics-modal .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 24px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }

            .analytics-modal .modal-header h2 {
                margin: 0;
                color: #00ff88;
            }

            .analytics-modal .modal-close {
                background: none;
                border: none;
                color: #888;
                font-size: 1.5rem;
                cursor: pointer;
            }

            .analytics-modal #analytics-dashboard {
                flex: 1;
                overflow-y: auto;
                padding: 0;
                margin: 0;
                background: transparent;
                border: none;
            }

            @media (max-width: 768px) {
                .quick-nav-bar {
                    right: 10px;
                    top: 10px;
                }

                .search-container {
                    width: 95%;
                    margin-top: -20px;
                }

                .search-filters {
                    flex-wrap: wrap;
                }

                .search-shortcuts {
                    flex-direction: column;
                    gap: 4px;
                    text-align: right;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

// Initialize universal navigation
window.universalNav = new UniversalToolNavigation();