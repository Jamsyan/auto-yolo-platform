import time
from .main import MessageCount

class ProgressBar:
    def __init__(self):
        self.index = 0
        self.task_ID = None
        self.total = None
        self.task_log = None
        self.time_all = None
        self.time_left = None
        self.time_submit = None
        self.time_update = None

    def submit(self, task_id,total):
        self.task_ID = task_id
        self.total = total
        self.time_submit = time.time()
        data = {
            "type": f"{self.__name__}.{self.submit.__name__}",
            "task_ID": self.task_ID,
            "total": self.total,
        }
        MessageCount.managers.append(data)

    def update(self, task_log):
        self.task_log = task_log
        self.time_update = time.time()
        self.calculate_time()
        self.index += 1
        index = float(self.index / self.total)*100
        data = {
            "type": f"{self.__name__}.{self.submit.__name__}",
            "time_all": self.time_all,
            "time_left": self.time_left,
            "task_log": self.task_log,
            "index": index
        }
        MessageCount.managers.append(data)

    def calculate_time(self):
        elapsed_time = self.time_update - self.time_submit
        total_time = elapsed_time * self.total / self.index
        left_time = total_time - elapsed_time
        left_time = left_time if left_time >= 0 else 0
        def format_t(t):
            hours = int(t // 3600)  # 小时
            mins = float((t % 3600) // 60)  # 分钟（保留2位小数）
            secs = float(t % 60)  # 秒（保留2位小数）
            return f"{hours}:{mins:.2f}:{secs:.2f}"
        self.time_all = format_t(total_time)
        self.time_left = format_t(left_time)