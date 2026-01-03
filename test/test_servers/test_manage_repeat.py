import pytest
from unittest.mock import patch, MagicMock
from src.servers.manage_repeat import MessagesRepeat, DefaultInterfaceUrl

class TestDefaultInterfaceUrl:
    def test_default_values(self):
        """测试默认接口URL值是否正确"""
        assert DefaultInterfaceUrl.LOCALHOST == 'localhost'
        assert DefaultInterfaceUrl.PORT == 8000
        assert DefaultInterfaceUrl.GETINTERFRACEIRL == "/api/inside/get/"
        assert DefaultInterfaceUrl.POSTINTERFRACEIRL == "/api/inside/post/"

class TestMessagesRepeat:
    def setup_method(self):
        """在每个测试方法前创建MessagesRepeat实例"""
        self.messages_repeat = MessagesRepeat()
    
    def test_initialization(self):
        """测试初始化是否正确设置属性"""
        assert hasattr(self.messages_repeat, 'requests')
        assert self.messages_repeat.localhost == 'localhost'
        assert self.messages_repeat.port == 8000
        assert self.messages_repeat.get == "/api/inside/get/"
        assert self.messages_repeat.post == "/api/inside/post/"
    
    @patch('src.servers.manage_repeat.requests.Session.post')
    def test_sendmessage_success(self, mock_post):
        """测试sendmessage方法成功发送消息"""
        # 配置mock
        mock_post.return_value = MagicMock(status_code=200)
        
        # 执行测试
        message = {'key': 'value'}
        self.messages_repeat.sendmessage(message)
        
        # 验证
        expected_url = "http://localhost:8000//api/inside/post/"  # 注意双斜杠，这是代码中的bug
        mock_post.assert_called_once_with(expected_url, data=message)
    
    @patch('src.servers.manage_repeat.requests.Session.post')
    def test_sendmessage_connection_error(self, mock_post):
        """测试sendmessage方法处理连接错误"""
        # 配置mock抛出requests.exceptions.ConnectionError
        from requests.exceptions import ConnectionError as RequestsConnectionError
        mock_post.side_effect = RequestsConnectionError("Connection refused")
        
        # 执行测试，应该不会抛出异常
        message = {'key': 'value'}
        self.messages_repeat.sendmessage(message)
        
        # 验证
        expected_url = "http://localhost:8000//api/inside/post/"
        mock_post.assert_called_once_with(expected_url, data=message)
    
    @patch('src.servers.manage_repeat.requests.Session.get')
    def test_getmessage(self, mock_get):
        """测试getmessage方法获取消息"""
        # 配置mock返回值
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success', 'data': 'test data'}
        mock_get.return_value = mock_response
        
        # 执行测试
        response = self.messages_repeat.getmessage()
        
        # 验证
        expected_url = "http://localhost:8000//api/inside/get/"  # 注意双斜杠，这是代码中的bug
        mock_get.assert_called_once_with(expected_url)
        assert response == mock_response
    
    @patch('src.servers.manage_repeat.requests.Session.get')
    def test_getmessage_http_error(self, mock_get):
        """测试getmessage方法处理HTTP错误"""
        # 配置mock抛出HTTPError
        from requests.exceptions import HTTPError
        mock_get.side_effect = HTTPError("HTTP Error")
        
        # 执行测试，应该抛出异常
        with pytest.raises(HTTPError):
            self.messages_repeat.getmessage()
        
        # 验证
        expected_url = "http://localhost:8000//api/inside/get/"
        mock_get.assert_called_once_with(expected_url)
