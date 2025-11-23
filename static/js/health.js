// Health monitoring and WebSocket connection
class HealthMonitor {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.updateInterval = null;
    }

    init() {
        this.connectWebSocket();
        this.startPolling();
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/system-stream`;
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.updateHealthDisplay(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            // Fall back to polling
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                console.log(`Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
                this.connectWebSocket();
            }, this.reconnectDelay);
        }
    }

    startPolling() {
        // Poll every 5 seconds as fallback
        this.updateInterval = setInterval(() => {
            this.fetchHealth();
        }, 5000);
        
        // Initial fetch
        this.fetchHealth();
    }

    async fetchHealth() {
        try {
            const response = await fetch('/api/v1/health');
            if (response.ok) {
                const data = await response.json();
                this.updateHealthDisplay(data);
            }
        } catch (error) {
            console.error('Error fetching health data:', error);
            this.showError();
        }
    }

    updateHealthDisplay(data) {
        // System info
        if (data.system) {
            document.getElementById('system-platform').textContent = 
                `${data.system.platform} ${data.system.platform_release}`;
            document.getElementById('system-hostname').textContent = data.system.hostname;
            document.getElementById('system-arch').textContent = data.system.architecture;
        }

        // CPU
        if (data.cpu) {
            const cpuUsage = data.cpu.usage_percent || 0;
            document.getElementById('cpu-usage').textContent = `${cpuUsage.toFixed(1)}%`;
            document.getElementById('cpu-freq').textContent = 
                data.cpu.frequency_mhz ? `${(data.cpu.frequency_mhz / 1000).toFixed(2)} GHz` : 'N/A';
            document.getElementById('cpu-cores').textContent = 
                data.cpu.count ? `${data.cpu.count} cores` : '';
            document.getElementById('cpu-progress').style.width = `${cpuUsage}%`;
        }

        // Memory
        if (data.memory) {
            const memPercent = data.memory.percent || 0;
            document.getElementById('memory-usage').textContent = `${memPercent.toFixed(1)}%`;
            document.getElementById('memory-used').textContent = `${data.memory.used_mb.toFixed(0)} MB`;
            document.getElementById('memory-total').textContent = `${data.memory.total_mb.toFixed(0)} MB`;
            document.getElementById('memory-progress').style.width = `${memPercent}%`;
        }

        // Temperature
        if (data.temperature) {
            const temp = data.temperature.celsius;
            if (temp !== null) {
                document.getElementById('temperature').textContent = `${temp.toFixed(1)}°C`;
                document.getElementById('temp-status').textContent = 
                    temp > 80 ? 'High' : temp > 60 ? 'Warm' : 'Normal';
            } else {
                document.getElementById('temperature').textContent = 'N/A';
                document.getElementById('temp-status').textContent = 'Unavailable';
            }
        }

        // Network
        if (data.network) {
            document.getElementById('network-up').textContent = 
                `${(data.network.mbps_sent / 1024).toFixed(2)} MB/s`;
            document.getElementById('network-down').textContent = 
                `${(data.network.mbps_recv / 1024).toFixed(2)} MB/s`;
        }

        // Disk
        if (data.disk && data.disk.root) {
            const diskPercent = data.disk.root.percent || 0;
            document.getElementById('disk-usage').textContent = `${diskPercent.toFixed(1)}%`;
            document.getElementById('disk-used').textContent = `${data.disk.root.used_gb.toFixed(1)} GB`;
            document.getElementById('disk-total').textContent = `${data.disk.root.total_gb.toFixed(1)} GB`;
            document.getElementById('disk-progress').style.width = `${diskPercent}%`;
        }

        // Voltage/Throttle
        if (data.voltage) {
            const status = data.voltage.status || 'N/A';
            document.getElementById('voltage-status').textContent = status;
            
            if (data.voltage.flags) {
                const flags = data.voltage.flags;
                const issues = [];
                if (flags.under_voltage) issues.push('Under Voltage');
                if (flags.throttled) issues.push('Throttled');
                if (flags.frequency_capped) issues.push('Frequency Capped');
                document.getElementById('throttle-info').textContent = 
                    issues.length > 0 ? issues.join(', ') : 'OK';
            } else {
                document.getElementById('throttle-info').textContent = 'N/A';
            }
        }

        // Update overall health status
        this.updateHealthStatus(data);
    }

    updateHealthStatus(data) {
        const statusDot = document.getElementById('health-status-dot');
        const statusText = document.getElementById('health-status-text');
        
        let status = 'healthy';
        let statusClass = 'healthy';
        
        // Determine overall health
        if (data.voltage && data.voltage.status === 'WARNING') {
            status = 'degraded';
            statusClass = 'degraded';
        }
        
        if (data.temperature && data.temperature.celsius > 80) {
            status = 'degraded';
            statusClass = 'degraded';
        }
        
        if (data.cpu && data.cpu.usage_percent > 95) {
            status = 'degraded';
            statusClass = 'degraded';
        }
        
        if (data.memory && data.memory.percent > 95) {
            status = 'degraded';
            statusClass = 'degraded';
        }

        statusDot.className = `status-dot ${statusClass}`;
        statusText.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }

    showError() {
        document.getElementById('health-status-text').textContent = 'Error';
        document.getElementById('health-status-dot').className = 'status-dot unhealthy';
    }

    destroy() {
        if (this.ws) {
            this.ws.close();
        }
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize health monitor
const healthMonitor = new HealthMonitor();

// Refresh function for manual refresh
function refreshHealth() {
    healthMonitor.fetchHealth();
}

