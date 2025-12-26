import time

class ProgressBar:
    def __init__(self):
        self.index = 0
        self.task = []
        self.task_ID = None
        self.total = None
        self.log = None
        self.time_all = None
        self.time_left = None
        self.time_submit = {}
        self.time_update = {}

    def submit(self, task_id,task_name,total):
        self.task_ID = task_id
        self.total = total
        self.time_submit[task_id] = time.time()
        self.task.append({
            "task_id": task_id,
            "task_name": task_name,
            "total": total,
        })
        data = {
            "type": f"{self.__class__.__name__}.{self.submit.__name__}",
            "task": self.task,
        }
        post_msg(data)

    def update(self, task_id):
        self.index += 1
        self.time_update[task_id] = time.time()
        self.calculate_time(task_id)
        index = min(100, int((self.index / self.total) * 100))
        data = {
            "type": f"{self.__class__.__name__}.{self.update.__name__}",
            task_id: {
                "time_all": self.time_all,
                "time_left": self.time_left,
                "text_log": self.log,
                "index": f'{index}%'
            }
        }
        post_msg(data)

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
            return f"{hours}:{mins:.2f}:{secs:.2f}"
        self.time_all = format_t(total_time)
        self.time_left = format_t(left_time)