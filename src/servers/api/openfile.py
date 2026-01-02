from pathlib import Path
from ..manage_repeat import MessagesRepeat
import win32file

class OpenFileDialog:
    """
    文件导入窗口后台执行支持
    """
    def __init__(self):
        self.default = ""
        self.drive = []
        self.dir_list = []
        self.msgsend = MessagesRepeat()

    def get_drive_letter(self):
        # 获取驱动器列表
        check_mask = [3]
        for i in range(26):
            drive = fr'{chr(ord('A')+i)}:\\'
            mask = win32file.GetDriveType(drive)
            if mask in check_mask:
                path = Path(drive).resolve()
                self.drive.append(path)
        self.data_send('dirve_list',self.drive)

    def get_dir_list(self,path):
        # 获取目录列表
        if path and Path(path).is_dir():
            for item in Path(path).iterdir():
                self.dir_list.append(item)
            self.data_send('file.dirlist',self.dir_list)
            self.dir_list = []
        elif path and Path(path).is_file():
            return
        elif not path:
            return

    def get_file_path(self):
        pass

    def get_file_list(self):
        pass

    def read_file_filter(self):
        pass

    def data_send(self,type,message):
        """
        发送文件数据信息
        :return:
        """
        data = {
            "type": type,
            "data": message
        }
        self.msgsend.post(data)

    def go_back(self):
        pass

    def search(self):
        pass

    def response_execution(self,message):
        """
        前端返回信息执行器
        :return:
        """
        type = message['type']
        if type == 'dir':
            pass
        elif type == 'file':
            pass


def test():
    OpenFileDialog().get_drive_letter()

if __name__ == "__main__":
    test()