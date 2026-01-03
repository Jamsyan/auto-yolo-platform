import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.servers.message_server import app

class TestMessageServer:
    def setup_method(self):
        """在每个测试方法前创建测试客户端"""
        self.client = TestClient(app)
    
    def test_post_message(self):
        """测试POST接口接收消息"""
        # 执行测试
        message = {"test": "data"}
        response = self.client.post("/api/inside/post/", json=message)
        
        # 验证
        assert response.status_code == 200
        assert response.json() is None  # 接口没有返回值
    
    def test_post_message_empty(self):
        """测试POST接口接收空消息"""
        # 执行测试
        message = {}
        response = self.client.post("/api/inside/post/", json=message)
        
        # 验证
        assert response.status_code == 200
        assert response.json() is None
    
    def test_post_message_invalid_json(self):
        """测试POST接口接收无效JSON"""
        # 执行测试
        response = self.client.post("/api/inside/post/", data="invalid json")
        
        # 验证
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_websocket_endpoint(self):
        """测试WebSocket端点"""
        # 使用测试客户端的websocket方法
        with self.client.websocket_connect("/api/") as websocket:
            # 测试发送消息
            test_message = {"type": "test", "data": "test data"}
            websocket.send_json(test_message)
            
            # 关闭连接
            websocket.close()
    
    @patch('src.servers.message_server.OpenFileDialog')
    def test_process_feedback_information_file_open(self, mock_open_file):
        """测试process_feedback_information函数处理file.open类型"""
        from src.servers.message_server import process_feedback_information
        
        # 执行测试
        data = {"type": "file.open", "data": "test data"}
        import asyncio
        asyncio.run(process_feedback_information(data))
        
        # 验证：注意实际代码中是直接调用类方法，而不是实例方法
        # 所以我们验证response_execution被调用
        mock_open_file.response_execution.assert_called_once_with('test data')
    
    def test_app_instance(self):
        """测试FastAPI应用实例是否正确创建"""
        from src.servers.message_server import app
        
        # 验证
        assert app is not None
        assert hasattr(app, 'routes')
        
        # 验证路由存在
        route_paths = [route.path for route in app.routes]
        assert "/api/inside/post/" in route_paths
        assert "/api/" in route_paths
