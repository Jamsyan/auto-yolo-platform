import time
import json
import hashlib
from datetime import timedelta
from ..transportation_hub import Transponder

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
        self.th = Transponder()

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
        update_time_list = []
        time_submit = self.time_submit[task_id]
        time_update = self.time_update[task_id]
        update_time_list.append(time_update)
        execution_time = sum(update_time_list)/len(update_time_list)
        total_time = execution_time*self.total[task_id]
        left_time = total_time - (time_update - time_submit)

        def format_t(t):
            """
            更健壮的时间格式化
            支持: 毫秒精度、超过24小时、可读性强
            """
            td = timedelta(seconds=t)

            # 如果小于1小时，显示 MM:SS.fff
            if t < 3600:
                minutes = int(td.seconds // 60)
                seconds = (td.seconds % 60) + td.microseconds / 1_000_000
                return f"{minutes:02d}:{seconds:06.3f}"
            # 如果小于1天，显示 HH:MM:SS.fff
            elif t < 86400:
                hours = td.seconds // 3600
                minutes = (td.seconds % 3600) // 60
                seconds = (td.seconds % 60) + td.microseconds / 1_000_000
                return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
            # 超过1天，显示 X天 HH:MM:SS
            else:
                days = td.days
                hours = td.seconds // 3600
                minutes = (td.seconds % 3600) // 60
                seconds = td.seconds % 60
                return f"{days}天 {hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_all[task_id] = format_t(total_time)  # 按任务ID存储
        self.time_left[task_id] = format_t(left_time)  # 按任务ID存储