from unittest.mock import patch, MagicMock
from servers.api.progressbar import ProgressBar


class TestProgressBar:
    def test_initialization(self):
        """测试ProgressBar类的初始化"""
        with patch('servers.api.progressbar.MessagesRepeat') as mock_mr:
            pb = ProgressBar()
            assert pb.index == {}
            assert pb.total == {}
            assert pb.task_id == {}
            assert pb.log is None
            assert pb.time_all == {}
            assert pb.time_left == {}
            assert pb.time_submit == {}
            assert pb.time_update == {}
            assert pb.task_list == []
            assert pb.update_list == []

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_submit(self, mock_mr):
        """测试submit方法"""
        # 设置mock返回值
        mock_mr_instance = MagicMock()
        mock_mr.return_value = mock_mr_instance
        
        pb = ProgressBar()
        
        # 调用submit方法
        task_id = 1
        task_name = "test_task"
        total = 100
        pb.submit(task_id, task_name, total)
        
        # 验证结果
        assert task_id in pb.total
        assert pb.total[task_id] == total
        
        assert task_id in pb.index
        assert pb.index[task_id] == 0
        
        assert task_id in pb.time_submit
        
        assert task_id in pb.task_id
        assert isinstance(pb.task_id[task_id], str)
        assert len(pb.task_id[task_id]) == 32  # MD5长度
        
        assert len(pb.task_list) == 1
        assert pb.task_list[0]["task_id"] == pb.task_id[task_id]
        assert pb.task_list[0]["task_name"] == task_name
        assert pb.task_list[0]["total"] == total
        
        # 验证调用
        mock_mr_instance.sendmessage.assert_called_once()

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_update(self, mock_mr):
        """测试update方法"""
        # 设置mock返回值
        mock_mr_instance = MagicMock()
        mock_mr.return_value = mock_mr_instance
        
        pb = ProgressBar()
        
        # 先调用submit方法
        task_id = 1
        task_name = "test_task"
        total = 100
        pb.submit(task_id, task_name, total)
        
        # 重置mock调用计数
        mock_mr_instance.sendmessage.reset_mock()
        
        # 调用update方法
        pb.update(task_id)
        
        # 验证结果
        assert pb.index[task_id] == 1
        assert task_id in pb.time_update
        assert task_id in pb.time_all
        assert task_id in pb.time_left
        
        assert len(pb.update_list) == 1
        assert pb.update_list[0]["task_id"] == pb.task_id[task_id]
        assert pb.update_list[0]["index"] == "1%"
        
        # 验证调用
        mock_mr_instance.sendmessage.assert_called_once()
        
        # 再次调用update方法，验证update_list的更新
        pb.update(task_id)
        assert pb.index[task_id] == 2
        assert pb.update_list[0]["index"] == "2%"

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_calculate_time_initial(self, mock_mr):
        """测试calculate_time方法在初始状态下的行为"""
        pb = ProgressBar()
        
        # 先调用submit方法
        task_id = 1
        task_name = "test_task"
        total = 100
        pb.submit(task_id, task_name, total)
        
        # 调用calculate_time方法
        pb.calculate_time(task_id)
        
        # 验证结果
        assert task_id in pb.time_all
        assert task_id in pb.time_left
        assert pb.time_all[task_id] == "00:00:00"
        assert pb.time_left[task_id] == "00:00:00"

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_calculate_time_with_progress(self, mock_mr):
        """测试calculate_time方法在有进度情况下的行为"""
        pb = ProgressBar()
        
        # 先调用submit方法
        task_id = 1
        task_name = "test_task"
        total = 100
        pb.submit(task_id, task_name, total)
        
        # 更新进度
        pb.index[task_id] = 50  # 50%进度
        
        # 设置时间值
        pb.time_submit[task_id] = 1000.0  # 提交时间
        pb.time_update[task_id] = 1005.0  # 更新时间（5秒后）
        
        # 调用calculate_time方法
        pb.calculate_time(task_id)
        
        # 验证结果
        assert task_id in pb.time_all
        assert task_id in pb.time_left
        
        # 预计总时间应该是10秒（5秒完成50%），剩余时间应该是5秒
        assert pb.time_all[task_id] == "00:00:10"  # 10秒
        assert pb.time_left[task_id] == "00:00:05"  # 5秒

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_calculate_time_near_completion(self, mock_mr):
        """测试calculate_time方法在接近完成情况下的行为"""
        pb = ProgressBar()
        
        # 先调用submit方法
        task_id = 1
        task_name = "test_task"
        total = 100
        pb.submit(task_id, task_name, total)
        
        # 更新进度到99%
        pb.index[task_id] = 99  # 99%进度
        
        # 设置时间值
        pb.time_submit[task_id] = 1000.0  # 提交时间
        pb.time_update[task_id] = 1009.9  # 更新时间（9.9秒后）
        
        # 调用calculate_time方法
        pb.calculate_time(task_id)
        
        # 验证结果
        assert task_id in pb.time_all
        assert task_id in pb.time_left
        
        # 预计总时间应该是10秒，剩余时间应该是0.1秒，四舍五入为0秒
        assert pb.time_all[task_id] == "00:00:10"  # 10秒
        assert pb.time_left[task_id] == "00:00:00"  # 0秒

    @patch('servers.api.progressbar.MessagesRepeat')
    def test_update_list_management(self, mock_mr):
        """测试update_list的管理"""
        # 设置mock返回值
        mock_mr_instance = MagicMock()
        mock_mr.return_value = mock_mr_instance
        
        pb = ProgressBar()
        
        # 提交两个任务
        task_id1 = 1
        task_name1 = "test_task_1"
        total1 = 100
        pb.submit(task_id1, task_name1, total1)
        
        task_id2 = 2
        task_name2 = "test_task_2"
        total2 = 200
        pb.submit(task_id2, task_name2, total2)
        
        # 重置mock调用计数
        mock_mr_instance.sendmessage.reset_mock()
        
        # 更新第一个任务
        pb.update(task_id1)
        assert len(pb.update_list) == 1
        assert pb.update_list[0]["task_id"] == pb.task_id[task_id1]
        assert pb.update_list[0]["index"] == "1%"
        
        # 更新第二个任务
        pb.update(task_id2)
        assert len(pb.update_list) == 2
        assert pb.update_list[1]["task_id"] == pb.task_id[task_id2]
        assert pb.update_list[1]["index"] == "1%"
        
        # 再次更新第一个任务
        pb.update(task_id1)
        assert len(pb.update_list) == 2  # 应该还是2个任务，只是更新其中一个
        assert pb.update_list[0]["index"] == "2%"
        assert pb.update_list[1]["index"] == "1%"