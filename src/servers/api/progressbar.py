import time
import json
from ..transportation_hub import Transponder

class ProgressBar:
    def __init__(self):
        self.index = 0
        self.total = None
        self.log = None
        self.time_all = None
        self.time_left = None
        self.time_submit = {}
        self.time_update = {}
        self.task_list = []
        self.update_list = []
        self.th = Transponder()

    def submit(self, task_id,task_name,total):
        self.total = total
        self.time_submit[task_id] = time.time()
        self.task_list.append({
            "task_id": task_id,
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
        self.index += 1
        self.time_update[task_id] = time.time()
        self.calculate_time(task_id)
        index = min(100, int((self.index / self.total) * 100))
        data = {
            "task_id": task_id,
            "time_all": self.time_all,
            "time_left": self.time_left,
            "index": f'{index}%',
        }
        found = False
        for i,item in enumerate(self.update_list):
            if item["task_id"] == task_id:
                self.update_list[i] = data
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
        total_time = execution_time*self.total
        left_time = total_time - (time_update - time_submit)
        def format_t(t):
            hours = int(t // 3600)  # 小时
            mins = float((t % 3600) // 60)  # 分钟（保留2位小数）
            secs = float(t % 60)  # 秒（保留2位小数）
            return f"{hours:.2f}:{mins:.2f}:{secs:.2f}"
        self.time_all = format_t(total_time)
        self.time_left = format_t(left_time)