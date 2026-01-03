import pytest
from unittest.mock import patch, MagicMock
from servers.message_server import app, message_queue, process_feedback_information


class TestMessageServer:
    def test_app_creation(self):
        """测试FastAPI应用的创建"""
        assert app is not None
        assert app.title == "FastAPI"

    @pytest.mark.asyncio
    async def test_message_queue(self):
        """测试消息队列的功能"""
        # 清空队列
        while not message_queue.empty():
            await message_queue.get()
        
        # 添加测试消息
        test_message = {"key": "value"}
        await message_queue.put(test_message)
        
        # 验证消息是否被正确添加
        assert not message_queue.empty()
        
        # 获取消息并验证
        received_message = await message_queue.get()
        assert received_message == test_message
        assert message_queue.empty()

    @pytest.mark.asyncio
    async def test_process_feedback_information(self):
        """测试process_feedback_information函数"""
        with patch('servers.message_server.OpenFileDialog') as mock_open_file_dialog:
            # 创建mock对象
            mock_instance = MagicMock()
            mock_open_file_dialog.return_value = mock_instance
            
            # 测试file.open类型
            test_data = {
                "type": "file.open",
                "data": {"test": "data"}
            }
            await process_feedback_information(test_data)
            
            # 验证调用
            mock_open_file_dialog.response_execution.assert_called_once_with({"test": "data"})