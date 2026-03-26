/**
 * Related Tools Widget - Embeddable component for cross-tool navigation
 * Expansion Agent 5 - Integration Enhancement System
 */

class RelatedToolsWidget {
    constructor(currentTool, containerId = 'related-tools-container') {
        this.currentTool = currentTool;
        this.containerId = containerId;
        this.integration = window.toolIntegration;
        this.init();
    }

    init() {
        this.createContainer();
        this.render();
        this.bindEvents();
    }

    createContainer() {
        let container = document.getElementById(this.containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = this.containerId;
            container.className = 'related-tools-widget';

            // Find best insertion point
            const mainContent = document.querySelector('main, .container, .content');
            if (mainContent) {
                mainContent.appendChild(container);
            } else {
                document.body.appendChild(container);
            }
        }
        this.container = container;
    }

    render() {
        const relatedTools = this.integration.getRelatedTools(this.currentTool);
        const recentlyUsed = this.integration.getRecentlyUsed(3);
        const favorites = this.integration.getFavorites().slice(0, 3);
        const category = this.integration.getToolCategory(this.currentTool);
        const categoryInfo = this.integration.toolCategories[category];

        this.container.innerHTML = `
            <div class="related-tools-content">
                <div class="tool-navigation-header">
                    <h3>🔗 Tool Navigation & Discovery</h3>
                    <div class="tool-actions">
                        <button class="favorite-btn ${favorites.some(f => f.id === this.currentTool) ? 'favorited' : ''}"
                                onclick="relatedToolsWidget.toggleFavorite()">
                            ⭐ ${favorites.some(f => f.id === this.currentTool) ? 'Favorited' : 'Add to Favorites'}
                        </button>
                        <button class="browse-all-btn" onclick="relatedToolsWidget.showAllTools()">
                            📂 Browse All Tools
                        </button>
                    </div>
                </div>

                ${categoryInfo ? `
                <div class="current-category">
                    <span class="category-badge">
                        ${categoryInfo.icon} ${categoryInfo.name}
                    </span>
                </div>
                ` : ''}

                <div class="tools-grid">
                    ${relatedTools.length > 0 ? `
                    <div class="tools-section">
                        <h4>🎯 Related Tools</h4>
                        <div class="tool-cards">
                            ${relatedTools.map(tool => this.createToolCard(tool, 'related')).join('')}
                        </div>
                    </div>
                    ` : ''}

                    ${recentlyUsed.length > 0 ? `
                    <div class="tools-section">
                        <h4>🕒 Recently Used</h4>
                        <div class="tool-cards">
                            ${recentlyUsed.map(tool => this.createToolCard(tool, 'recent')).join('')}
                        </div>
                    </div>
                    ` : ''}

                    ${favorites.length > 0 ? `
                    <div class="tools-section">
                        <h4>⭐ Your Favorites</h4>
                        <div class="tool-cards">
                            ${favorites.map(tool => this.createToolCard(tool, 'favorite')).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>

                <div class="quick-access">
                    <h4>🚀 Quick Access</h4>
                    <div class="category-links">
                        ${Object.entries(this.integration.toolCategories).map(([id, cat]) => `
                            <a href="#" onclick="relatedToolsWidget.showCategory('${id}')" class="category-link">
                                ${cat.icon} ${cat.name}
                            </a>
                        `).join('')}
                    </div>
                </div>

                <div class="tool-insights">
                    <div class="usage-stats">
                        <span>📊 Total Tools: ${this.integration.generateToolNavigation().totalTools}</span>
                        <span>🔥 Your Usage: ${Object.keys(this.integration.usageAnalytics).length} tools used</span>
                    </div>
                </div>
            </div>
        `;

        this.injectStyles();
    }

    createToolCard(tool, type) {
        const usageCount = this.integration.usageAnalytics[tool.id] || 0;
        const typeIcon = type === 'related' ? '🔗' : type === 'recent' ? '🕒' : '⭐';

        return `
            <div class="tool-card" data-tool-id="${tool.id}" onclick="relatedToolsWidget.navigateToTool('${tool.url}')">
                <div class="tool-card-header">
                    <span class="tool-type-icon">${typeIcon}</span>
                    <span class="tool-name">${tool.name}</span>
                </div>
                <div class="tool-card-meta">
                    ${tool.category ? `<span class="tool-category">${this.integration.toolCategories[tool.category]?.icon || '🔧'} ${this.integration.toolCategories[tool.category]?.name || tool.category}</span>` : ''}
                    ${usageCount > 0 ? `<span class="usage-count">Used ${usageCount}x</span>` : ''}
                </div>
            </div>
        `;
    }

    navigateToTool(url) {
        // Track the navigation
        const toolId = url.match(/\/free-tools\/([^\/]+)\//)?.[1];
        if (toolId) {
            this.integration.trackToolUsage(toolId);
        }
        window.location.href = url;
    }

    toggleFavorite() {
        const isFavorited = this.integration.toggleFavorite(this.currentTool);
        const btn = this.container.querySelector('.favorite-btn');
        if (btn) {
            btn.textContent = isFavorited ? '⭐ Favorited' : '⭐ Add to Favorites';
            btn.className = `favorite-btn ${isFavorited ? 'favorited' : ''}`;
        }
        this.render(); // Re-render to update favorites section
    }

    showAllTools() {
        const modal = this.createToolBrowserModal();
        document.body.appendChild(modal);
        modal.style.display = 'flex';
    }

    showCategory(categoryId) {
        const category = this.integration.toolCategories[categoryId];
        if (!category) return;

        const modal = this.createCategoryModal(categoryId, category);
        document.body.appendChild(modal);
        modal.style.display = 'flex';
    }

    createToolBrowserModal() {
        const navigation = this.integration.generateToolNavigation();

        const modal = document.createElement('div');
        modal.className = 'tool-browser-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🔧 All Tools Browser</h2>
                    <button class="modal-close" onclick="this.closest('.tool-browser-modal').remove()">✕</button>
                </div>
                <div class="modal-body">
                    ${navigation.categories.map(category => `
                        <div class="category-section">
                            <h3>${category.icon} ${category.name} (${category.tools.length})</h3>
                            <div class="tools-grid-modal">
                                ${category.tools.map(tool => `
                                    <div class="tool-card-modal" onclick="relatedToolsWidget.navigateToTool('${tool.url}')">
                                        <span class="tool-name">${tool.name}</span>
                                        <span class="tool-usage">${this.integration.usageAnalytics[tool.id] || 0} uses</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        return modal;
    }

    createCategoryModal(categoryId, category) {
        const modal = document.createElement('div');
        modal.className = 'tool-browser-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${category.icon} ${category.name}</h2>
                    <button class="modal-close" onclick="this.closest('.tool-browser-modal').remove()">✕</button>
                </div>
                <div class="modal-body">
                    <div class="tools-grid-modal">
                        ${category.tools.map(toolId => {
                            const toolName = this.integration.getToolDisplayName(toolId);
                            const usageCount = this.integration.usageAnalytics[toolId] || 0;
                            return `
                                <div class="tool-card-modal" onclick="relatedToolsWidget.navigateToTool('/free-tools/${toolId}/')">
                                    <span class="tool-name">${toolName}</span>
                                    <span class="tool-usage">${usageCount} uses</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            </div>
        `;
        return modal;
    }

    bindEvents() {
        // Close modals when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('tool-browser-modal')) {
                e.target.remove();
            }
        });
    }

    injectStyles() {
        if (document.getElementById('related-tools-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'related-tools-styles';
        styles.textContent = `
            .related-tools-widget {
                background: #12121a;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 24px;
                margin: 32px 0;
                backdrop-filter: blur(12px);
            }

            .tool-navigation-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                flex-wrap: wrap;
                gap: 12px;
            }

            .tool-navigation-header h3 {
                margin: 0;
                color: #00ff88;
                font-size: 1.4rem;
            }

            .tool-actions {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }

            .favorite-btn, .browse-all-btn {
                padding: 8px 16px;
                border: 1px solid #00ff88;
                background: transparent;
                color: #00ff88;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.2s;
            }

            .favorite-btn:hover, .browse-all-btn:hover {
                background: rgba(0,255,136,0.1);
            }

            .favorite-btn.favorited {
                background: #00ff88;
                color: #0a0a0f;
            }

            .current-category {
                margin-bottom: 20px;
            }

            .category-badge {
                display: inline-block;
                background: rgba(0,255,136,0.1);
                color: #00ff88;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.9rem;
            }

            .tools-grid {
                display: grid;
                gap: 20px;
            }

            .tools-section h4 {
                color: #e0e0e8;
                margin: 0 0 12px 0;
                font-size: 1.1rem;
            }

            .tool-cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 12px;
                margin-bottom: 16px;
            }

            .tool-card {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 8px;
                padding: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }

            .tool-card:hover {
                border-color: #00ff88;
                background: rgba(0,255,136,0.05);
            }

            .tool-card-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 6px;
            }

            .tool-type-icon {
                font-size: 0.9rem;
            }

            .tool-name {
                color: #e0e0e8;
                font-weight: 500;
                font-size: 0.95rem;
            }

            .tool-card-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.8rem;
                color: #888;
            }

            .tool-category, .usage-count {
                font-size: 0.75rem;
            }

            .quick-access h4 {
                color: #e0e0e8;
                margin: 24px 0 12px 0;
            }

            .category-links {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }

            .category-link {
                display: inline-block;
                padding: 6px 12px;
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                color: #00ccff;
                text-decoration: none;
                font-size: 0.85rem;
                transition: all 0.2s;
            }

            .category-link:hover {
                background: rgba(0,204,255,0.1);
                border-color: #00ccff;
            }

            .tool-insights {
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid rgba(255,255,255,0.06);
            }

            .usage-stats {
                display: flex;
                justify-content: space-between;
                font-size: 0.85rem;
                color: #888;
            }

            /* Modal Styles */
            .tool-browser-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }

            .modal-content {
                background: #12121a;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                max-width: 90vw;
                max-height: 90vh;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }

            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 24px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
            }

            .modal-header h2 {
                margin: 0;
                color: #00ff88;
            }

            .modal-close {
                background: none;
                border: none;
                color: #888;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 4px;
            }

            .modal-close:hover {
                color: #e0e0e8;
            }

            .modal-body {
                padding: 20px 24px;
                overflow-y: auto;
                flex: 1;
            }

            .category-section {
                margin-bottom: 24px;
            }

            .category-section h3 {
                color: #e0e0e8;
                margin: 0 0 12px 0;
            }

            .tools-grid-modal {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 8px;
            }

            .tool-card-modal {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 6px;
                padding: 12px;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .tool-card-modal:hover {
                border-color: #00ff88;
                background: rgba(0,255,136,0.05);
            }

            .tool-card-modal .tool-name {
                color: #e0e0e8;
                font-size: 0.9rem;
            }

            .tool-card-modal .tool-usage {
                color: #888;
                font-size: 0.75rem;
            }

            @media (max-width: 768px) {
                .tool-cards {
                    grid-template-columns: 1fr;
                }

                .tool-navigation-header {
                    flex-direction: column;
                    align-items: stretch;
                }

                .usage-stats {
                    flex-direction: column;
                    gap: 4px;
                }

                .modal-content {
                    max-width: 95vw;
                    max-height: 95vh;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

// Auto-initialize for current page
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const toolMatch = currentPath.match(/\/free-tools\/([^\/]+)\//);
    if (toolMatch && window.toolIntegration) {
        window.relatedToolsWidget = new RelatedToolsWidget(toolMatch[1]);
    }
});