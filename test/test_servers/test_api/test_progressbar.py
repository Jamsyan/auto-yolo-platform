import pytest
from unittest.mock import patch, MagicMock
from src.servers.api.progressbar import ProgressBar

class TestProgressBar:
    def setup_method(self):
        """在每个测试方法前创建ProgressBar实例"""
        self.progress_bar = ProgressBar()
    
    def test_initialization(self):
        """测试初始化是否正确设置属性"""
        assert hasattr(self.progress_bar, 'index')
        assert hasattr(self.progress_bar, 'total')
        assert hasattr(self.progress_bar, 'task_id')
        assert hasattr(self.progress_bar, 'log')
        assert hasattr(self.progress_bar, 'time_all')
        assert hasattr(self.progress_bar, 'time_left')
        assert hasattr(self.progress_bar, 'time_submit')
        assert hasattr(self.progress_bar, 'time_update')
        assert hasattr(self.progress_bar, 'task_list')
        assert hasattr(self.progress_bar, 'update_list')
        assert hasattr(self.progress_bar, 'th')
        
        # 验证初始值
        assert isinstance(self.progress_bar.index, dict)
        assert isinstance(self.progress_bar.total, dict)
        assert isinstance(self.progress_bar.task_id, dict)
        assert self.progress_bar.log is None
        assert isinstance(self.progress_bar.time_all, dict)
        assert isinstance(self.progress_bar.time_left, dict)
        assert isinstance(self.progress_bar.time_submit, dict)
        assert isinstance(self.progress_bar.time_update, dict)
        assert isinstance(self.progress_bar.task_list, list)
        assert isinstance(self.progress_bar.update_list, list)
        assert len(self.progress_bar.task_list) == 0
        assert len(self.progress_bar.update_list) == 0
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_submit_method(self, mock_sendmessage):
        """测试submit()方法"""
        # 执行测试
        task_id = 1
        task_name = 'test_task'
        total = 100
        self.progress_bar.submit(task_id, task_name, total)
        
        # 验证
        assert task_id in self.progress_bar.index
        assert task_id in self.progress_bar.total
        assert task_id in self.progress_bar.time_submit
        assert task_id in self.progress_bar.task_id
        assert len(self.progress_bar.task_list) == 1
        
        # 验证task_list中的内容
        task = self.progress_bar.task_list[0]
        assert 'task_id' in task
        assert task['task_name'] == task_name
        assert task['total'] == total
        
        # 验证sendmessage被调用
        mock_sendmessage.assert_called_once()
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_submit_method_multiple_tasks(self, mock_sendmessage):
        """测试submit()方法提交多个任务"""
        # 执行测试
        tasks = [
            (1, 'task1', 100),
            (2, 'task2', 200),
            (3, 'task3', 300)
        ]
        
        for task_id, task_name, total in tasks:
            self.progress_bar.submit(task_id, task_name, total)
        
        # 验证
        assert len(self.progress_bar.task_list) == 3
        assert len(self.progress_bar.index) == 3
        assert len(self.progress_bar.total) == 3
        assert len(self.progress_bar.task_id) == 3
        
        # 验证sendmessage被调用了3次
        assert mock_sendmessage.call_count == 3
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_update_method(self, mock_sendmessage):
        """测试update()方法"""
        # 先提交一个任务
        task_id = 1
        task_name = 'test_task'
        total = 100
        self.progress_bar.submit(task_id, task_name, total)
        
        # 执行测试
        self.progress_bar.update(task_id)
        
        # 验证
        assert self.progress_bar.index[task_id] == 1
        assert task_id in self.progress_bar.time_update
        assert task_id in self.progress_bar.time_all
        assert task_id in self.progress_bar.time_left
        assert len(self.progress_bar.update_list) == 1
        
        # 验证update_list中的内容
        update = self.progress_bar.update_list[0]
        assert 'task_id' in update
        assert 'time_all' in update
        assert 'time_left' in update
        assert 'index' in update
        assert update['index'] == '1%'
        
        # 验证sendmessage被调用（第二次调用，第一次是submit）
        assert mock_sendmessage.call_count == 2
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_update_method_multiple_times(self, mock_sendmessage):
        """测试update()方法多次调用"""
        # 先提交一个任务
        task_id = 1
        task_name = 'test_task'
        total = 100
        self.progress_bar.submit(task_id, task_name, total)
        
        # 执行测试：更新5次
        for i in range(5):
            self.progress_bar.update(task_id)
        
        # 验证
        assert self.progress_bar.index[task_id] == 5
        assert len(self.progress_bar.update_list) == 1  # 应该只包含一个任务的更新
        
        # 验证update_list中的内容
        update = self.progress_bar.update_list[0]
        assert update['index'] == '5%'
        
        # 验证sendmessage被调用了6次（1次submit + 5次update）
        assert mock_sendmessage.call_count == 6
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_update_method_multiple_tasks(self, mock_sendmessage):
        """测试update()方法处理多个任务"""
        # 先提交两个任务
        task1_id = 1
        task1_name = 'task1'
        task1_total = 100
        self.progress_bar.submit(task1_id, task1_name, task1_total)
        
        task2_id = 2
        task2_name = 'task2'
        task2_total = 200
        self.progress_bar.submit(task2_id, task2_name, task2_total)
        
        # 执行测试：分别更新两个任务
        self.progress_bar.update(task1_id)
        self.progress_bar.update(task2_id)
        self.progress_bar.update(task1_id)
        
        # 验证
        assert self.progress_bar.index[task1_id] == 2
        assert self.progress_bar.index[task2_id] == 1
        assert len(self.progress_bar.update_list) == 2  # 应该包含两个任务的更新
        
        # 验证sendmessage被调用了5次（2次submit + 3次update）
        assert mock_sendmessage.call_count == 5
    
    def test_calculate_time_method(self):
        """测试calculate_time()方法"""
        # 先设置必要的属性
        task_id = 1
        self.progress_bar.time_submit[task_id] = 1234567890.0
        self.progress_bar.time_update[task_id] = 1234567895.0
        self.progress_bar.index[task_id] = 5
        self.progress_bar.total[task_id] = 100
        
        # 执行测试
        self.progress_bar.calculate_time(task_id)
        
        # 验证
        assert task_id in self.progress_bar.time_all
        assert task_id in self.progress_bar.time_left
        
        # 验证时间格式（HH:MM:SS）
        time_all = self.progress_bar.time_all[task_id]
        time_left = self.progress_bar.time_left[task_id]
        
        assert isinstance(time_all, str)
        assert len(time_all.split(':')) == 3
        assert isinstance(time_left, str)
        assert len(time_left.split(':')) == 3
    
    def test_calculate_time_method_no_progress(self):
        """测试calculate_time()方法处理无进度情况"""
        # 先设置必要的属性
        task_id = 1
        self.progress_bar.time_submit[task_id] = 1234567890.0
        self.progress_bar.time_update[task_id] = 1234567895.0
        self.progress_bar.index[task_id] = 0  # 无进度
        self.progress_bar.total[task_id] = 100
        
        # 执行测试
        self.progress_bar.calculate_time(task_id)
        
        # 验证
        assert task_id in self.progress_bar.time_all
        assert task_id in self.progress_bar.time_left
        
        # 验证时间为00:00:00
        assert self.progress_bar.time_all[task_id] == '00:00:00'
        assert self.progress_bar.time_left[task_id] == '00:00:00'
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_update_method_100_percent(self, mock_sendmessage):
        """测试update()方法处理100%进度"""
        # 先提交一个任务
        task_id = 1
        task_name = 'test_task'
        total = 5
        self.progress_bar.submit(task_id, task_name, total)
        
        # 执行测试：更新5次，达到100%
        for i in range(5):
            self.progress_bar.update(task_id)
        
        # 验证
        assert self.progress_bar.index[task_id] == 5
        
        # 验证update_list中的内容
        update = self.progress_bar.update_list[0]
        assert update['index'] == '100%'
        
        # 验证sendmessage被调用了6次（1次submit + 5次update）
        assert mock_sendmessage.call_count == 6
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_update_method_over_100_percent(self, mock_sendmessage):
        """测试update()方法处理超过100%进度"""
        # 先提交一个任务
        task_id = 1
        task_name = 'test_task'
        total = 5
        self.progress_bar.submit(task_id, task_name, total)
        
        # 执行测试：更新6次，超过100%
        for i in range(6):
            self.progress_bar.update(task_id)
        
        # 验证
        assert self.progress_bar.index[task_id] == 6
        
        # 验证update_list中的内容，应该被限制在100%
        update = self.progress_bar.update_list[0]
        assert update['index'] == '100%'
        
        # 验证sendmessage被调用了7次（1次submit + 6次update）
        assert mock_sendmessage.call_count == 7
    
    @patch('src.servers.api.progressbar.MessagesRepeat.sendmessage')
    def test_task_id_generation(self, mock_sendmessage):
        """测试任务ID生成机制"""
        # 执行测试：提交两个相同任务ID但不同名称的任务
        task_id = 1
        self.progress_bar.submit(task_id, 'task1', 100)
        self.progress_bar.submit(task_id, 'task2', 200)
        
        # 验证：应该生成不同的任务ID
        task1_hash = self.progress_bar.task_id[task_id]
        
        # 提交另一个任务
        task_id2 = 2
        self.progress_bar.submit(task_id2, 'task1', 100)
        task2_hash = self.progress_bar.task_id[task_id2]
        
        # 验证
        assert task1_hash != task2_hash
        
        # 验证sendmessage被调用了3次
        assert mock_sendmessage.call_count == 3
    
    def test_progress_bar_integration(self):
        """测试进度条完整流程"""
        # 执行完整流程：提交任务 -> 更新进度 -> 完成任务
        task_id = 1
        task_name = 'integration_test'
        total = 3
        
        # 提交任务
        self.progress_bar.submit(task_id, task_name, total)
        assert len(self.progress_bar.task_list) == 1
        
        # 第一次更新
        self.progress_bar.update(task_id)
        assert self.progress_bar.index[task_id] == 1
        assert self.progress_bar.update_list[0]['index'] == '33%'
        
        # 第二次更新
        self.progress_bar.update(task_id)
        assert self.progress_bar.index[task_id] == 2
        assert self.progress_bar.update_list[0]['index'] == '66%'
        
        # 第三次更新（完成）
        self.progress_bar.update(task_id)
        assert self.progress_bar.index[task_id] == 3
        assert self.progress_bar.update_list[0]['index'] == '100%'
        
        # 验证所有属性都已设置
        assert task_id in self.progress_bar.index
        assert task_id in self.progress_bar.total
        assert task_id in self.progress_bar.task_id
        assert task_id in self.progress_bar.time_submit
        assert task_id in self.progress_bar.time_update
        assert task_id in self.progress_bar.time_all
        assert task_id in self.progress_bar.time_left
