function createWebSocket(url) {
    return new WebSocket(url);
}

// 封装连接管理器
class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        this.socket = createWebSocket(this.url);

        this.socket.onopen = function() {
            this.isConnected = true;
            console.log('WebSocket连接成功');
        }.bind(this);

        this.socket.onerror = function(error) {
            console.error('WebSocket连接错误:', error);
            this.isConnected = false;
            this.handleReconnect();
        }.bind(this);

        this.socket.onclose = function() {
            console.log('WebSocket连接关闭');
            this.isConnected = false;
        }.bind(this);

        return this;
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`尝试重连第${this.reconnectAttempts}次`);

            setTimeout(function() {
                this.socket = null;
                this.connect();
            }.bind(this), 5000);
        } else {
            console.error('达到最大重连次数，停止重连');
        }
    }

    send(message) {
        if (this.isConnected && this.socket) {
            this.socket.send(message);
        } else {
            console.error('WebSocket未连接，无法发送消息');
        }
    }

    onMessage(callback) {
        if (this.socket) {
            this.socket.onmessage = callback;
        }
    }

    close() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// 创建实例
const wsManager = new WebSocketManager("ws://localhost:8000/api/");

// 导出实例和方法
export { wsManager };
export function sendMessages(message) {
    wsManager.send(message);
}
export function getMessages(handler) {
    wsManager.onMessage(handler);
}
export function initConnection() {
    wsManager.connect();
}