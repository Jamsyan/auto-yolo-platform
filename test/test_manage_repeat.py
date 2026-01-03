from unittest.mock import patch, MagicMock
from servers.manage_repeat import MessagesRepeat, DefaultInterfaceUrl


class TestDefaultInterfaceUrl:
    def test_default_interface_url(self):
        """测试DefaultInterfaceUrl类的默认值"""
        assert DefaultInterfaceUrl.LOCALHOST == 'localhost'
        assert DefaultInterfaceUrl.PORT == 8000
        assert DefaultInterfaceUrl.GETINTERFRACEIRL == "/api/inside/get/"
        assert DefaultInterfaceUrl.POSTINTERFRACEIRL == "/api/inside/post/"

class TestMessagesRepeat:
    def test_initialization(self):
        """测试MessagesRepeat类的初始化"""
        mr = MessagesRepeat()
        assert mr.localhost == 'localhost'
        assert mr.port == 8000
        assert mr.get == "/api/inside/get/"
        assert mr.post == "/api/inside/post/"
        assert mr.requests is not None

    @patch('servers.manage_repeat.requests.Session')
    def test_sendmessage_success(self, mock_session_class):
        """测试sendmessage方法在正常情况下的行为"""
        # 创建mock对象
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        # 实例化MessagesRepeat
        mr = MessagesRepeat()
        
        # 测试数据
        test_message = {'key': 'value'}
        
        # 调用sendmessage方法
        mr.sendmessage(test_message)
        
        # 验证调用
        expected_url = f"http://{mr.localhost}:{mr.port}/{mr.post}"
        mock_session.post.assert_called_once_with(expected_url, data=test_message)

    @patch('servers.manage_repeat.requests.Session')
    def test_sendmessage_connection_error(self, mock_session_class):
        """测试sendmessage方法在连接错误情况下的行为"""
        # 创建mock对象，模拟连接错误
        mock_session = MagicMock()
        mock_session.post.side_effect = ConnectionError("Connection refused")
        mock_session_class.return_value = mock_session
        
        # 实例化MessagesRepeat
        mr = MessagesRepeat()
        
        # 测试数据
        test_message = {'key': 'value'}
        
        # 调用sendmessage方法，应该不会引发异常
        mr.sendmessage(test_message)
        
        # 验证调用
        expected_url = f"http://{mr.localhost}:{mr.port}/{mr.post}"
        mock_session.post.assert_called_once_with(expected_url, data=test_message)

    @patch('servers.manage_repeat.requests.Session')
    def test_getmessage(self, mock_session_class):
        """测试getmessage方法"""
        # 创建mock对象和响应
        mock_response = MagicMock()
        mock_response.text = '{"result": "success"}'
        mock_response.status_code = 200
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # 实例化MessagesRepeat
        mr = MessagesRepeat()
        
        # 调用getmessage方法
        response = mr.getmessage()
        
        # 验证调用和返回值
        expected_url = f"http://{mr.localhost}:{mr.port}/{mr.get}"
        mock_session.get.assert_called_once_with(expected_url)
        assert response == mock_response