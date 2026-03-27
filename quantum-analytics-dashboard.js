/**
 * QUANTUM ANALYTICS DASHBOARD
 * Real-time ecosystem monitoring with advanced visualizations
 * ML-driven insights and predictive analytics
 */

class QuantumAnalyticsDashboard {
    constructor(containerId = 'quantum-dashboard') {
        this.containerId = containerId;
        this.charts = new Map();
        this.metrics = new Map();
        this.realTimeData = new Map();
        this.updateInterval = 1000; // 1 second updates

        console.log('[QUANTUM DASHBOARD] Initializing real-time analytics dashboard');

        this.initialize();
    }

    async initialize() {
        await this.createDashboardContainer();
        await this.initializeCharts();
        await this.connectToDataStreams();
        await this.startRealTimeUpdates();

        console.log('[QUANTUM DASHBOARD] Real-time analytics dashboard active');
    }

    async createDashboardContainer() {
        const container = document.getElementById(this.containerId) || document.body;

        container.innerHTML = `
            <div class="quantum-dashboard">
                <header class="dashboard-header">
                    <h1 class="dashboard-title">
                        <span class="quantum-icon">⚛️</span>
                        Quantum Ecosystem Analytics
                    </h1>
                    <div class="dashboard-status">
                        <span class="status-indicator active"></span>
                        <span class="status-text">Real-time monitoring active</span>
                    </div>
                </header>

                <div class="dashboard-grid">
                    <!-- Performance Overview -->
                    <div class="dashboard-card performance-overview">
                        <h3>Performance Overview</h3>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <div class="metric-value" id="response-time">--</div>
                                <div class="metric-label">Avg Response Time</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value" id="throughput">--</div>
                                <div class="metric-label">Throughput</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value" id="error-rate">--</div>
                                <div class="metric-label">Error Rate</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value" id="cache-hit-rate">--</div>
                                <div class="metric-label">Cache Hit Rate</div>
                            </div>
                        </div>
                        <canvas id="performance-chart" width="400" height="200"></canvas>
                    </div>

                    <!-- User Behavior Analytics -->
                    <div class="dashboard-card user-analytics">
                        <h3>User Behavior Analytics</h3>
                        <div class="behavior-metrics">
                            <div class="metric-row">
                                <span>Active Users:</span>
                                <span id="active-users">--</span>
                            </div>
                            <div class="metric-row">
                                <span>Session Duration:</span>
                                <span id="session-duration">--</span>
                            </div>
                            <div class="metric-row">
                                <span>Tools Used:</span>
                                <span id="tools-used">--</span>
                            </div>
                        </div>
                        <canvas id="user-behavior-chart" width="400" height="200"></canvas>
                    </div>

                    <!-- Integration Health -->
                    <div class="dashboard-card integration-health">
                        <h3>Integration Health Matrix</h3>
                        <div id="integration-matrix" class="integration-grid"></div>
                    </div>

                    <!-- Real-time Tool Usage -->
                    <div class="dashboard-card tool-usage">
                        <h3>Real-time Tool Usage</h3>
                        <div id="tool-usage-heatmap" class="heatmap-container"></div>
                    </div>

                    <!-- Predictive Analytics -->
                    <div class="dashboard-card predictive-analytics">
                        <h3>Predictive Analytics</h3>
                        <div class="prediction-container">
                            <div class="prediction-item">
                                <h4>Next Tool Prediction</h4>
                                <div id="next-tool-prediction" class="prediction-value">--</div>
                            </div>
                            <div class="prediction-item">
                                <h4>Performance Trend</h4>
                                <div id="performance-trend" class="prediction-value">--</div>
                            </div>
                        </div>
                        <canvas id="prediction-chart" width="400" height="150"></canvas>
                    </div>

                    <!-- System Health -->
                    <div class="dashboard-card system-health">
                        <h3>System Health</h3>
                        <div class="health-indicators">
                            <div class="health-item">
                                <div class="health-circle" id="cpu-health"></div>
                                <span>CPU</span>
                            </div>
                            <div class="health-item">
                                <div class="health-circle" id="memory-health"></div>
                                <span>Memory</span>
                            </div>
                            <div class="health-item">
                                <div class="health-circle" id="network-health"></div>
                                <span>Network</span>
                            </div>
                            <div class="health-item">
                                <div class="health-circle" id="cache-health"></div>
                                <span>Cache</span>
                            </div>
                        </div>
                    </div>

                    <!-- ML Insights -->
                    <div class="dashboard-card ml-insights">
                        <h3>ML-Driven Insights</h3>
                        <div id="ml-insights-container" class="insights-container">
                            <div class="insight-loading">Analyzing patterns...</div>
                        </div>
                    </div>

                    <!-- Real-time Logs -->
                    <div class="dashboard-card real-time-logs">
                        <h3>Real-time Event Stream</h3>
                        <div id="log-container" class="log-stream"></div>
                    </div>
                </div>
            </div>
        `;

        this.attachDashboardStyles();
    }

    attachDashboardStyles() {
        if (document.getElementById('quantum-dashboard-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'quantum-dashboard-styles';
        styles.textContent = `
            .quantum-dashboard {
                background: #0a0a0f;
                color: #e0e0e8;
                font-family: 'Inter', sans-serif;
                padding: 20px;
                min-height: 100vh;
            }

            .dashboard-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #1e1e2e;
            }

            .dashboard-title {
                color: #00ff88;
                font-size: 2rem;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .quantum-icon {
                animation: quantum-pulse 2s infinite;
            }

            @keyframes quantum-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.1); }
            }

            .dashboard-status {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .status-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #ff4444;
            }

            .status-indicator.active {
                background: #00ff88;
                animation: pulse 1s infinite;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
                100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
            }

            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 24px;
            }

            .dashboard-card {
                background: linear-gradient(135deg, rgba(18, 18, 26, 0.9) 0%, rgba(30, 30, 46, 0.9) 100%);
                border: 1px solid #1e1e2e;
                border-radius: 16px;
                padding: 24px;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }

            .dashboard-card:hover {
                border-color: #00ff88;
                box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
            }

            .dashboard-card h3 {
                color: #00ccff;
                margin: 0 0 20px 0;
                font-size: 1.2rem;
                font-weight: 600;
            }

            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-bottom: 20px;
            }

            .metric-item {
                background: rgba(0, 255, 136, 0.05);
                border: 1px solid rgba(0, 255, 136, 0.1);
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            }

            .metric-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #00ff88;
                margin-bottom: 4px;
            }

            .metric-label {
                font-size: 0.8rem;
                color: #a0a0b0;
            }

            .health-indicators {
                display: flex;
                justify-content: space-around;
                align-items: center;
                padding: 20px 0;
            }

            .health-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
            }

            .health-circle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: 3px solid #1e1e2e;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .health-circle.excellent {
                background: radial-gradient(circle, #00ff88, #00cc66);
                border-color: #00ff88;
            }

            .health-circle.good {
                background: radial-gradient(circle, #ffaa00, #ff9900);
                border-color: #ffaa00;
            }

            .health-circle.warning {
                background: radial-gradient(circle, #ff6600, #ff4400);
                border-color: #ff6600;
            }

            .health-circle.critical {
                background: radial-gradient(circle, #ff4444, #ff2222);
                border-color: #ff4444;
            }

            .log-stream {
                height: 200px;
                overflow-y: auto;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 12px;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 0.85rem;
                line-height: 1.4;
            }

            .log-entry {
                margin-bottom: 8px;
                padding: 4px 8px;
                border-radius: 4px;
                border-left: 3px solid;
            }

            .log-entry.info { border-left-color: #00ccff; }
            .log-entry.success { border-left-color: #00ff88; }
            .log-entry.warning { border-left-color: #ffaa00; }
            .log-entry.error { border-left-color: #ff4444; }

            .prediction-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin-bottom: 20px;
            }

            .prediction-item {
                background: rgba(0, 204, 255, 0.05);
                border: 1px solid rgba(0, 204, 255, 0.1);
                border-radius: 8px;
                padding: 12px;
            }

            .prediction-item h4 {
                margin: 0 0 8px 0;
                font-size: 0.9rem;
                color: #00ccff;
            }

            .prediction-value {
                font-size: 1.1rem;
                font-weight: 600;
                color: #e0e0e8;
            }

            .insights-container {
                max-height: 200px;
                overflow-y: auto;
            }

            .insight-item {
                background: rgba(108, 92, 231, 0.1);
                border: 1px solid rgba(108, 92, 231, 0.2);
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
            }

            .insight-title {
                font-weight: 600;
                color: #6C5CE7;
                margin-bottom: 4px;
            }

            .insight-description {
                font-size: 0.9rem;
                color: #b0b0b8;
            }

            .insight-loading {
                text-align: center;
                padding: 40px;
                color: #a0a0b0;
                font-style: italic;
            }

            .integration-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                gap: 8px;
            }

            .integration-item {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                padding: 8px;
                text-align: center;
                font-size: 0.8rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .integration-item.healthy {
                border-color: #00ff88;
                background: rgba(0, 255, 136, 0.1);
            }

            .integration-item.warning {
                border-color: #ffaa00;
                background: rgba(255, 170, 0, 0.1);
            }

            .integration-item.error {
                border-color: #ff4444;
                background: rgba(255, 68, 68, 0.1);
            }

            @media (max-width: 768px) {
                .dashboard-grid {
                    grid-template-columns: 1fr;
                }

                .metrics-grid {
                    grid-template-columns: 1fr;
                }

                .prediction-container {
                    grid-template-columns: 1fr;
                }
            }
        `;

        document.head.appendChild(styles);
    }

    async initializeCharts() {
        // Initialize Chart.js charts for real-time data
        this.setupPerformanceChart();
        this.setupUserBehaviorChart();
        this.setupPredictionChart();
    }

    setupPerformanceChart() {
        const ctx = document.getElementById('performance-chart').getContext('2d');

        this.charts.set('performance', new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Response Time (ms)',
                    data: [],
                    borderColor: '#00ff88',
                    backgroundColor: 'rgba(0, 255, 136, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Throughput (req/s)',
                    data: [],
                    borderColor: '#00ccff',
                    backgroundColor: 'rgba(0, 204, 255, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#a0a0b0' }
                    },
                    y: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#a0a0b0' }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#e0e0e8' }
                    }
                },
                animation: false
            }
        }));
    }

    async connectToDataStreams() {
        // Connect to quantum ecosystem for real-time data
        if (window.quantumEcosystem) {
            this.quantumConnection = window.quantumEcosystem;
        }

        // Setup WebSocket connection for real-time updates
        this.setupWebSocketConnection();

        // Setup EventSource for server-sent events
        this.setupEventSource();
    }

    setupWebSocketConnection() {
        try {
            this.websocket = new WebSocket('ws://localhost:8080/api/quantum/analytics/stream');

            this.websocket.onopen = () => {
                console.log('[DASHBOARD] WebSocket connected');
                this.updateConnectionStatus(true);
            };

            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleRealtimeData(data);
            };

            this.websocket.onerror = (error) => {
                console.warn('[DASHBOARD] WebSocket error:', error);
                this.updateConnectionStatus(false);
            };

            this.websocket.onclose = () => {
                console.log('[DASHBOARD] WebSocket disconnected');
                this.updateConnectionStatus(false);
                // Attempt reconnection
                setTimeout(() => this.setupWebSocketConnection(), 5000);
            };

        } catch (error) {
            console.warn('[DASHBOARD] WebSocket not available, using polling fallback');
            this.setupPollingFallback();
        }
    }

    startRealTimeUpdates() {
        this.updateTimer = setInterval(() => {
            this.updateDashboard();
        }, this.updateInterval);

        console.log('[DASHBOARD] Real-time updates started');
    }

    async updateDashboard() {
        try {
            // Get latest metrics from quantum ecosystem
            const data = await this.getLatestMetrics();

            // Update performance metrics
            this.updatePerformanceMetrics(data.performance);

            // Update user behavior analytics
            this.updateUserBehaviorMetrics(data.userBehavior);

            // Update integration health
            this.updateIntegrationHealth(data.integrationHealth);

            // Update system health indicators
            this.updateSystemHealth(data.systemHealth);

            // Update predictive analytics
            this.updatePredictiveAnalytics(data.predictions);

            // Update ML insights
            this.updateMLInsights(data.mlInsights);

            // Add log entry
            this.addLogEntry('info', 'Dashboard updated successfully');

        } catch (error) {
            console.error('[DASHBOARD] Update failed:', error);
            this.addLogEntry('error', `Update failed: ${error.message}`);
        }
    }

    async getLatestMetrics() {
        if (this.quantumConnection) {
            return await this.quantumConnection.getQuantumDashboardData();
        }

        // Fallback to mock data for demonstration
        return this.generateMockData();
    }

    generateMockData() {
        const now = Date.now();
        return {
            performance: {
                responseTime: 50 + Math.random() * 100,
                throughput: 100 + Math.random() * 50,
                errorRate: Math.random() * 0.05,
                cacheHitRate: 0.85 + Math.random() * 0.1
            },
            userBehavior: {
                activeUsers: Math.floor(10 + Math.random() * 50),
                sessionDuration: 300 + Math.random() * 600,
                toolsUsed: Math.floor(5 + Math.random() * 10)
            },
            integrationHealth: {
                healthy: Math.floor(15 + Math.random() * 10),
                warning: Math.floor(Math.random() * 3),
                error: Math.floor(Math.random() * 2)
            },
            systemHealth: {
                cpu: 0.3 + Math.random() * 0.4,
                memory: 0.4 + Math.random() * 0.3,
                network: 0.2 + Math.random() * 0.2,
                cache: 0.1 + Math.random() * 0.2
            },
            predictions: {
                nextTool: 'calculator-' + Math.floor(Math.random() * 100),
                performanceTrend: Math.random() > 0.5 ? 'improving' : 'stable'
            },
            mlInsights: this.generateMockInsights()
        };
    }

    updatePerformanceMetrics(data) {
        document.getElementById('response-time').textContent = `${data.responseTime.toFixed(1)}ms`;
        document.getElementById('throughput').textContent = `${data.throughput.toFixed(1)}/s`;
        document.getElementById('error-rate').textContent = `${(data.errorRate * 100).toFixed(2)}%`;
        document.getElementById('cache-hit-rate').textContent = `${(data.cacheHitRate * 100).toFixed(1)}%`;

        // Update performance chart
        const chart = this.charts.get('performance');
        if (chart) {
            const time = new Date().toLocaleTimeString();
            chart.data.labels.push(time);
            chart.data.datasets[0].data.push(data.responseTime);
            chart.data.datasets[1].data.push(data.throughput);

            // Keep only last 20 data points
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => dataset.data.shift());
            }

            chart.update('none');
        }
    }

    updateSystemHealth(data) {
        this.updateHealthCircle('cpu-health', data.cpu);
        this.updateHealthCircle('memory-health', data.memory);
        this.updateHealthCircle('network-health', data.network);
        this.updateHealthCircle('cache-health', data.cache);
    }

    updateHealthCircle(elementId, value) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const percentage = Math.round(value * 100);
        element.textContent = `${percentage}%`;

        // Update health status based on value
        element.className = 'health-circle';
        if (value < 0.3) element.classList.add('excellent');
        else if (value < 0.6) element.classList.add('good');
        else if (value < 0.8) element.classList.add('warning');
        else element.classList.add('critical');
    }

    addLogEntry(type, message) {
        const logContainer = document.getElementById('log-container');
        if (!logContainer) return;

        const timestamp = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.innerHTML = `
            <span class="log-timestamp">[${timestamp}]</span>
            <span class="log-message">${message}</span>
        `;

        logContainer.appendChild(entry);

        // Keep only last 50 entries
        while (logContainer.children.length > 50) {
            logContainer.removeChild(logContainer.firstChild);
        }

        // Auto-scroll to bottom
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    updateConnectionStatus(connected) {
        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');

        if (statusIndicator && statusText) {
            if (connected) {
                statusIndicator.classList.add('active');
                statusText.textContent = 'Real-time monitoring active';
            } else {
                statusIndicator.classList.remove('active');
                statusText.textContent = 'Connection lost - attempting reconnect';
            }
        }
    }

    destroy() {
        console.log('[DASHBOARD] Shutting down analytics dashboard');

        if (this.updateTimer) clearInterval(this.updateTimer);
        if (this.websocket) this.websocket.close();

        // Clean up charts
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
    }
}

// Initialize dashboard when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.quantumDashboard = new QuantumAnalyticsDashboard();
    });
} else {
    window.quantumDashboard = new QuantumAnalyticsDashboard();
}

// Chart.js fallback if not loaded
if (typeof Chart === 'undefined') {
    console.warn('[DASHBOARD] Chart.js not available, using fallback visualization');
    window.Chart = {
        register: () => {},
        // Minimal fallback implementation
    };
}

console.log('[QUANTUM DASHBOARD] Analytics Dashboard Module Loaded');