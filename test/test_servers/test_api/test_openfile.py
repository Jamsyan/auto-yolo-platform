import pytest
from unittest.mock import patch, MagicMock
from src.servers.api.openfile import OpenFileDialog

class TestOpenFileDialog:
    def setup_method(self):
        """在每个测试方法前创建OpenFileDialog实例"""
        self.open_file = OpenFileDialog()
    
    def test_initialization(self):
        """测试初始化是否正确设置属性"""
        assert hasattr(self.open_file, 'name')
        assert hasattr(self.open_file, 'path')
        assert hasattr(self.open_file, 'is_dir')
        assert hasattr(self.open_file, 'size')
        assert hasattr(self.open_file, 'modified')
        assert hasattr(self.open_file, 'ext')
        assert hasattr(self.open_file, 'filter_list')
        assert hasattr(self.open_file, 'msgsend')
        
        # 验证初始值
        assert self.open_file.name is None
        assert self.open_file.path is None
        assert self.open_file.is_dir is None
        assert self.open_file.size == 0
        assert self.open_file.modified is None
        assert self.open_file.ext is None
    
    def test_data_method(self):
        """测试data()方法返回正确的数据格式"""
        # 设置属性
        self.open_file.name = 'test_file'
        self.open_file.path = 'C:\\test\\test_file.txt'
        self.open_file.is_dir = False
        self.open_file.size = 1024
        self.open_file.modified = 1234567890.0
        self.open_file.ext = '.txt'
        
        # 执行测试
        result = self.open_file.data()
        
        # 验证
        expected = {
            'name': 'test_file',
            'path': 'C:\\test\\test_file.txt',
            'is_dir': False,
            'size': 1024,
            'modfied': 1234567890.0,
            'ext': '.txt'
        }
        assert result == expected
    
    def test_get_filter_list_default(self):
        """测试_get_filter_list()方法返回默认过滤列表"""
        # 执行测试
        result = self.open_file._get_filter_list()
        
        # 验证
        expected = ['.jpg', '.jpeg', '.png', '.mp4']
        assert result == expected
    
    def test_get_filter_list_with_new_filter(self):
        """测试_get_filter_list()方法添加新的过滤条件"""
        # 执行测试
        result = self.open_file._get_filter_list('.pdf')
        
        # 验证
        expected = ['.jpg', '.jpeg', '.png', '.mp4', '.pdf']
        assert result == expected
    
    def test_get_filter_list_with_existing_filter(self):
        """测试_get_filter_list()方法添加已存在的过滤条件"""
        # 执行测试
        result = self.open_file._get_filter_list('.jpg')
        
        # 验证
        expected = ['.jpg', '.jpeg', '.png', '.mp4']
        assert result == expected
    
    @patch('src.servers.api.openfile.win32file.GetDriveType')
    @patch('src.servers.api.openfile.OpenFileDialog.send')
    def test_get_drive_letter(self, mock_send, mock_get_drive):
        """测试get_drive_letter()方法"""
        # 配置mock
        mock_get_drive.return_value = 3  # DRIVE_FIXED
        
        # 执行测试
        result = self.open_file.get_drive_letter()
        
        # 验证
        assert isinstance(result, list)
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == 'file.open'
    
    @patch('src.servers.api.openfile.Path')
    @patch('src.servers.api.openfile.OpenFileDialog.send')
    def test_get_dir_list(self, mock_send, mock_path):
        """测试get_dir_list()方法"""
        # 配置mock
        mock_dir1 = MagicMock(is_dir=MagicMock(return_value=True))
        mock_dir1.name = 'dir1'
        mock_dir2 = MagicMock(is_dir=MagicMock(return_value=True))
        mock_dir2.name = 'dir2'
        mock_path_instance = mock_path.return_value
        mock_path_instance.iterdir.return_value = [mock_dir1, mock_dir2]
        
        # 执行测试
        result = self.open_file.get_dir_list('C:\\test')
        
        # 验证
        assert isinstance(result, list)
        assert len(result) == 2
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == 'file.open.dir_list'
    
    @patch('src.servers.api.openfile.Path')
    @patch('src.servers.api.openfile.OpenFileDialog.send')
    def test_get_file_list(self, mock_send, mock_path):
        """测试get_file_list()方法"""
        # 配置mock
        mock_file1 = MagicMock(is_file=MagicMock(return_value=True), is_dir=MagicMock(return_value=False))
        mock_file1.name = 'file1.jpg'
        mock_file1.resolve.return_value = 'C:\\test\\file1.jpg'
        mock_file1.stat.return_value.st_size = 1024
        mock_file1.stat.return_value.st_mtime = 1234567890.0
        mock_file1.suffix = '.jpg'
        
        mock_file2 = MagicMock(is_file=MagicMock(return_value=True), is_dir=MagicMock(return_value=False))
        mock_file2.name = 'file2.png'
        mock_file2.resolve.return_value = 'C:\\test\\file2.png'
        mock_file2.stat.return_value.st_size = 2048
        mock_file2.stat.return_value.st_mtime = 1234567891.0
        mock_file2.suffix = '.png'
        
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_dir.return_value = True
        mock_path_instance.iterdir.return_value = [mock_file1, mock_file2]
        
        # 执行测试
        result = self.open_file.get_file_list('C:\\test')
        
        # 验证
        assert isinstance(result, list)
        assert len(result) == 2
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == 'file.open.file_list'
    
    def test_read_file_filter(self):
        """测试read_file_filter()方法"""
        # 准备测试数据
        file_list = [
            {'ext': '.jpg'},
            {'ext': '.txt'},
            {'ext': '.png'},
            {'ext': '.pdf'},
            {'ext': '.mp4'}
        ]
        
        # 执行测试
        result = self.open_file.read_file_filter(file_list)
        
        # 验证
        assert isinstance(result, list)
        # 应该只包含.jpg, .png, .mp4
        assert len(result) == 3
        assert all(file['ext'] in ['.jpg', '.png', '.mp4'] for file in result)
    
    def test_read_file_filter_empty(self):
        """测试read_file_filter()方法处理空列表"""
        # 执行测试
        result = self.open_file.read_file_filter([])
        
        # 验证
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('src.servers.api.openfile.MessagesRepeat.sendmessage')
    def test_send_method(self, mock_sendmessage):
        """测试send()方法"""
        # 执行测试
        message_type = 'test.type'
        message_data = {'key': 'value'}
        self.open_file.send(message_type, message_data)
        
        # 验证
        expected = {
            "type": message_type,
            "data": message_data
        }
        mock_sendmessage.assert_called_once_with(expected)
    
    def test_go_back_method(self):
        """测试go_back()方法"""
        # 执行测试
        result = self.open_file.go_back()
        
        # 验证
        assert result is None
    
    def test_search_method(self):
        """测试search()方法"""
        # 执行测试
        result = self.open_file.search()
        
        # 验证
        assert result is None
    
    @patch('src.servers.api.openfile.OpenFileDialog.get_drive_letter')
    def test_response_execution_file_open(self, mock_get_drive):
        """测试response_execution()方法处理file.open类型"""
        # 执行测试
        message = {'type': 'file.open'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_get_drive.assert_called_once()
    
    @patch('src.servers.api.openfile.OpenFileDialog.get_dir_list')
    def test_response_execution_file_open_dir_list(self, mock_get_dir):
        """测试response_execution()方法处理file.open.dir_list类型"""
        # 执行测试
        message = {'type': 'file.open.dir_list'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_get_dir.assert_called_once()
    
    @patch('src.servers.api.openfile.OpenFileDialog.get_file_list')
    def test_response_execution_file_open_file_list(self, mock_get_file):
        """测试response_execution()方法处理file.open.file_list类型"""
        # 执行测试
        message = {'type': 'file.open.file_list'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_get_file.assert_called_once()
    
    @patch('src.servers.api.openfile.OpenFileDialog.go_back')
    def test_response_execution_file_back(self, mock_go_back):
        """测试response_execution()方法处理file.back类型"""
        # 执行测试
        message = {'type': 'file.back'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_go_back.assert_called_once()
    
    @patch('src.servers.api.openfile.OpenFileDialog.search')
    def test_response_execution_file_search(self, mock_search):
        """测试response_execution()方法处理file.search类型"""
        # 执行测试
        message = {'type': 'file.search'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_search.assert_called_once()
    
    @patch('src.servers.api.openfile.OpenFileDialog._get_filter_list')
    def test_response_execution_file_filter(self, mock_filter):
        """测试response_execution()方法处理file.filter类型"""
        # 执行测试
        message = {'type': 'file.filter'}
        self.open_file.response_execution(message)
        
        # 验证
        mock_filter.assert_called_once()
    
    def test_response_execution_invalid_type(self):
        """测试response_execution()方法处理无效类型"""
        # 执行测试，应该不会抛出异常
        message = {'type': 'invalid_type'}
        result = self.open_file.response_execution(message)
        
        # 验证
        assert result is None
