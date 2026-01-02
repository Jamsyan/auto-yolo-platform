function createWebSocket(url) {
    return new WebSocket(url);
}

// 封装连接管理器
class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0; // 计数器
        this.maxReconnectAttempts = 10;
    }

    // 建立链接
    connect() {
        this.socket = createWebSocket(this.url);

        // 连接成功检查
        this.socket.onopen = function() {
            if (this.reconnectAttempts !== 0) {
                this.reconnectAttempts = 0
            }
            this.isConnected = true;
            console.log('WebSocket连接成功');
        }.bind(this);

        // 异常检查
        this.socket.onerror = function(error) {
            console.error('WebSocket连接错误:', error);
        }.bind(this);

        // 连接丢失
        this.socket.onclose = function() {
            console.warn('WebSocket连接关闭');
            this.handleReconnect()
        }.bind(this);
        return this;
    }

    // 重连机制
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            // 计数器累加
            this.reconnectAttempts++;
            console.log(`尝试重连第${this.reconnectAttempts}次`);
            setTimeout(function() {
                if (this.socket) {
                    try {
                        console.warn('识别到socket实例存在,执行初始化')
                        this.socket.close();
                        this.socket.onclose = null;
                        this.socket.onerror = null;
                        this.socket.onmessage = null;
                        this.socket.onopen = null;
                    }
                    catch (error) {
                        console.error('socket实力存在但是关闭失败',error)
                    }
                }
                this.socket = null;
                this.connect();
            }.bind(this), 5000);
        } else {
            console.warn('达到最大重连次数，停止重连');
        }
    }

    // 发送消息
    send(message) {
        if (this.isConnected && this.socket) {
            try {
                // 将消息转换为 JSON 字符串
                const messageStr = typeof message === 'string' ? message : JSON.stringify(message);
                this.socket.send(messageStr);
                console.log('WebSocket消息发送成功:', messageStr);
                return true;
            } catch (error) {
                console.error('WebSocket消息发送失败:', error);
                return false;
            }
        } else {
            console.error('WebSocket未连接，无法发送消息');
            return false;
        }
    }

    // 接受消息
    onMessage(callback) {
        if (this.socket) {
            this.socket.onmessage = callback;
        }
    }

    // 连接关闭
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
// 发送socket消息
export function sendMessages(message) {
    wsManager.send(message);
}
// 接受socket消息
export function getMessages(handler) {
    wsManager.onMessage(handler);
}
// 初始化socket消息
export function initConnection() {
    wsManager.connect();
}