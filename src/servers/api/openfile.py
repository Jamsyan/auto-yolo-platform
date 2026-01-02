from pathlib import Path
from ..manage_repeat import MessagesRepeat
import win32file

class OpenFileDialog:
    """
    文件导入窗口后台执行支持
    """
    def __init__(self):
        self.name:str|None = None
        self.path:str|None = None
        self.is_dir:bool|None = None
        self.size:int|None = 0
        self.modified:str|float|None = None
        self.ext:str|None = None

        self.data = {
            'name': self.name,
            'path': self.path,
            'is_dir': self.is_dir,
            'size': self.size,
            'modfied': self.modified,
            'ext': self.ext
        }

        self.default = ""
        self.msgsend = MessagesRepeat()

    def get_drive_letter(self):
        # 获取驱动器列表
        check_mask = [3]
        drive_list = []
        for i in range(26):
            drive = fr'{chr(ord('A')+i)}:\\'
            mask = win32file.GetDriveType(drive)
            if mask in check_mask:
                self.name = mask
                self.path = str(Path(drive).resolve())
                self.is_dir = True
                drive_list.append(self.data)
        self.send('file.open.dirve_list', drive_list)

    def get_dir_list(self,path):
        """
        获取目录列表
        :param path:
        :return:
        """
        file = Path(path)
        dir_list = []
        for item in file.iterdir():
            if item.is_dir():
                self.data['name'] = item.name
                self.data['path'] = str(Path(item).resolve())
                self.data['is_dir'] = True
                dir_list.append(self.data)
        self.send('file.open.dir_list',dir_list)


    def get_file_list(self,path):
        """
        获取目标目录文件列表
        :return:
        """
        file_list = []
        file = Path(path)
        if file.is_dir():
            for item in file.iterdir():
                if item.is_file():
                    self.name = item.name
                    self.path = str(item.resolve())
                    self.is_dir = False
                    self.size = item.stat().st_size
                    self.modified = item.stat().st_mtime
                    self.ext = item.suffix
                    file_list.append(self.data)
            self.send('file.open.file_list',file_list)

    def read_file_filter(self):
        pass

    def send(self,type,message):
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