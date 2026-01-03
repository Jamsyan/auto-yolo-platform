import time
import json
import hashlib
from ..manage_repeat import MessagesRepeat

class ProgressBar:
    def __init__(self):
        self.index = {}
        self.total = {}
        self.task_id = {}
        self.log = None
        self.time_all = {}  # 按任务ID存储
        self.time_left = {}  # 按任务ID存储
        self.time_submit = {}
        self.time_update = {}
        self.task_list = []
        self.update_list = []
        self.th = MessagesRepeat()

    def submit(self, task_id,task_name,total):
        self.total[task_id] = total
        self.index[task_id] = 0
        self.time_submit[task_id] = time.time()
        hs = hashlib.md5()
        hs.update(str(task_id).encode('utf-8'))
        hs.update(task_name.encode('utf-8'))
        id = hs.hexdigest()
        self.task_id[task_id] = id
        self.task_list.append({
            "task_id": self.task_id[task_id],
            "task_name": task_name,
            "total": total,
        })
        self.th.sendmessage(json.dumps(
            {
                "type": f"{self.__class__.__name__}.{self.submit.__name__}",
                "task_list": self.task_list,
            }
        ))

    def update(self, task_id):
        self.index[task_id] += 1
        self.time_update[task_id] = time.time()
        self.calculate_time(task_id)
        index = min(100, int((self.index[task_id] / self.total[task_id]) * 100))
        data = {
            "task_id": self.task_id[task_id],
            "time_all": self.time_all[task_id],  # 使用特定任务的时间
            "time_left": self.time_left[task_id],  # 使用特定任务的时间
            "index": f'{index}%',
        }
        found = False
        for i,item in enumerate(self.update_list):
            if item["task_id"] == self.task_id[task_id]:
                self.update_list[i] = data
                found = True  # 修复：找到匹配项后设置found为True
                break  # 修复：找到后退出循环
        if not found:
            self.update_list.append(data)
        self.th.sendmessage(json.dumps(
            {
                "type": f"{self.__class__.__name__}.{self.update.__name__}",
                "update_list": self.update_list,
            }
        ))

    def calculate_time(self, task_id):
        time_submit = self.time_submit[task_id]
        time_update = self.time_update[task_id]
        
        # 计算已完成部分的平均执行时间
        current_progress = self.index[task_id]
        if current_progress > 0:
            elapsed_time = time_update - time_submit  # 已用时间
            avg_time_per_unit = elapsed_time / current_progress  # 每个单位的平均耗时
            total_time = avg_time_per_unit * self.total[task_id]  # 预计总时间
            left_time = total_time - elapsed_time  # 剩余时间
        else:
            # 如果还没有进度，则估算一个值
            total_time = 0
            left_time = 0

        def format_t(t):
            """
            时间格式化为 HH:MM:SS 格式
            """
            # 将总秒数转换为时、分、秒
            if t < 0:
                t = 0  # 避免负数时间
            total_seconds = int(t)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_all[task_id] = format_t(total_time)  # 按任务ID存储
        self.time_left[task_id] = format_t(left_time)  # 按任务ID存储