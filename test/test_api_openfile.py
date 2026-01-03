from unittest.mock import patch, MagicMock
from servers.api.openfile import OpenFileDialog


class TestOpenFileDialog:
    def test_initialization(self):
        """测试OpenFileDialog类的初始化"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            assert ofd.name is None
            assert ofd.path is None
            assert ofd.is_dir is None
            assert ofd.size == 0
            assert ofd.modified is None
            assert ofd.ext is None
            assert ofd.default == ""
            assert ofd.filter_list is not None
            assert isinstance(ofd.filter_list, list)

    def test_data_method(self):
        """测试data方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            
            # 设置测试数据
            ofd.name = "test.txt"
            ofd.path = "C:/test/test.txt"
            ofd.is_dir = False
            ofd.size = 1024
            ofd.modified = 1234567890.0
            ofd.ext = ".txt"
            
            # 调用data方法
            data = ofd.data()
            
            # 验证结果
            assert data == {
                'name': "test.txt",
                'path': "C:/test/test.txt",
                'is_dir': False,
                'size': 1024,
                'modfied': 1234567890.0,
                'ext': ".txt"
            }

    def test_filter_list_default(self):
        """测试filter_list方法的默认情况"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            
            # 调用filter_list方法，不传递任何参数
            filter_list = ofd.filter_list()
            
            # 验证结果
            expected_list = ['.jpg', '.jpeg', '.png', '.mp4']
            assert filter_list == expected_list

    def test_filter_list_with_new_filter(self):
        """测试filter_list方法添加新过滤器的情况"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            
            # 调用filter_list方法，传递新过滤器
            new_filter = '.gif'
            filter_list = ofd.filter_list(new_filter)
            
            # 验证结果
            expected_list = ['.jpg', '.jpeg', '.png', '.mp4', '.gif']
            assert filter_list == expected_list

    @patch('servers.api.openfile.win32file')
    @patch('servers.api.openfile.Path')
    def test_get_drive_letter(self, mock_path, mock_win32file):
        """测试get_drive_letter方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            # 设置mock返回值
            mock_win32file.GetDriveType.side_effect = lambda x: 3 if x in ['C:\\', 'D:\\'] else 0
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.resolve.return_value = "C:/"
            
            ofd = OpenFileDialog()
            
            # 调用get_drive_letter方法
            drive_list = ofd.get_drive_letter()
            
            # 验证调用
            assert len(drive_list) == 2  # 假设只有C:和D:是本地磁盘
            assert all(isinstance(drive, dict) for drive in drive_list)
            assert all(drive['is_dir'] is True for drive in drive_list)

    @patch('servers.api.openfile.Path')
    def test_get_dir_list(self, mock_path):
        """测试get_dir_list方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            # 设置mock返回值
            mock_dir1 = MagicMock()
            mock_dir1.is_dir.return_value = True
            mock_dir1.name = "dir1"
            
            mock_dir2 = MagicMock()
            mock_dir2.is_dir.return_value = True
            mock_dir2.name = "dir2"
            
            mock_path_instance = MagicMock()
            mock_path_instance.iterdir.return_value = [mock_dir1, mock_dir2]
            mock_path.return_value = mock_path_instance
            
            mock_path_instance2 = MagicMock()
            mock_path_instance2.resolve.return_value = "C:/test/dir1"
            mock_path.return_value = mock_path_instance2
            
            ofd = OpenFileDialog()
            
            # 调用get_dir_list方法
            dir_list = ofd.get_dir_list("C:/test")
            
            # 验证结果
            assert len(dir_list) == 2
            assert all(drive['is_dir'] is True for drive in dir_list)

    @patch('servers.api.openfile.Path')
    def test_get_file_list(self, mock_path):
        """测试get_file_list方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            # 设置mock返回值
            mock_file1 = MagicMock()
            mock_file1.is_file.return_value = True
            mock_file1.is_dir.return_value = False
            mock_file1.name = "file1.jpg"
            mock_file1.suffix = ".jpg"
            
            mock_stat1 = MagicMock()
            mock_stat1.st_size = 1024
            mock_stat1.st_mtime = 1234567890.0
            mock_file1.stat.return_value = mock_stat1
            
            mock_file2 = MagicMock()
            mock_file2.is_file.return_value = True
            mock_file2.is_dir.return_value = False
            mock_file2.name = "file2.txt"
            mock_file2.suffix = ".txt"
            
            mock_stat2 = MagicMock()
            mock_stat2.st_size = 2048
            mock_stat2.st_mtime = 1234567891.0
            mock_file2.stat.return_value = mock_stat2
            
            mock_path_instance = MagicMock()
            mock_path_instance.is_dir.return_value = True
            mock_path_instance.iterdir.return_value = [mock_file1, mock_file2]
            mock_path.return_value = mock_path_instance
            
            ofd = OpenFileDialog()
            
            # 调用get_file_list方法
            file_list = ofd.get_file_list("C:/test")
            
            # 验证结果
            assert len(file_list) == 2
            assert all(drive['is_dir'] is False for drive in file_list)

    def test_read_file_filter(self):
        """测试read_file_filter方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            
            # 设置测试数据
            test_files = [
                {'name': 'file1.jpg', 'ext': '.jpg'},
                {'name': 'file2.txt', 'ext': '.txt'},
                {'name': 'file3.png', 'ext': '.png'},
                {'name': 'file4.mp4', 'ext': '.mp4'},
                {'name': 'file5.gif', 'ext': '.gif'}
            ]
            
            # 调用read_file_filter方法
            filtered_files = ofd.read_file_filter(test_files)
            
            # 验证结果
            # 默认过滤器是['.jpg', '.jpeg', '.png', '.mp4']，所以应该返回4个文件
            assert len(filtered_files) == 4
            assert all(file['ext'] in ['.jpg', '.png', '.mp4'] for file in filtered_files)

    def test_send_method(self):
        """测试send方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            # 设置mock返回值
            mock_mr_instance = MagicMock()
            mock_mr.return_value = mock_mr_instance
            
            ofd = OpenFileDialog()
            
            # 调用send方法
            test_type = "test_type"
            test_message = {"key": "value"}
            ofd.send(test_type, test_message)
            
            # 验证调用
            mock_mr_instance.sendmessage.assert_called_once()

    def test_response_execution(self):
        """测试response_execution方法"""
        with patch('servers.api.openfile.MessagesRepeat') as mock_mr:
            ofd = OpenFileDialog()
            
            # 测试file.open类型
            with patch.object(ofd, 'get_drive_letter') as mock_get_drive:
                test_data = {
                    'type': 'file.open',
                    'data': {}
                }
                ofd.response_execution(test_data)
                mock_get_drive.assert_called_once()
            
            # 测试file.open.dir_list类型
            with patch.object(ofd, 'get_dir_list') as mock_get_dir:
                test_data = {
                    'type': 'file.open.dir_list',
                    'data': {}
                }
                ofd.response_execution(test_data)
                mock_get_dir.assert_called_once()
            
            # 测试file.open.file_list类型
            with patch.object(ofd, 'get_file_list') as mock_get_file:
                test_data = {
                    'type': 'file.open.file_list',
                    'data': {}
                }
                ofd.response_execution(test_data)
                mock_get_file.assert_called_once()
            
            # 测试file.filter类型
            with patch.object(ofd, 'filter_list') as mock_filter_list:
                test_data = {
                    'type': 'file.filter',
                    'data': {}
                }
                ofd.response_execution(test_data)
                mock_filter_list.assert_called_once()