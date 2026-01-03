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

        self.default = ""
        self.filter_list = self._get_filter_list()
        self.msgsend = MessagesRepeat()

    def data(self):
        return {
            'name': self.name,
            'path': self.path,
            'is_dir': self.is_dir,
            'size': self.size,
            'modfied': self.modified,
            'ext': self.ext
        }

    def _get_filter_list(self, filter:str = None):
        filter_list = [
            '.jpg',
            '.jpeg',
            '.png',
            '.mp4',
        ]
        if filter and filter not in filter_list:
            filter_list.append(filter)
        return filter_list

    def get_drive_letter(self):
        # 获取驱动器列表
        drive_list = []
        for i in range(26):
            drive = fr'{chr(ord('A')+i)}:\\'
            mask = win32file.GetDriveType(drive)
            if mask == 3:
                self.name = drive.split(':')[0]
                self.path = str(Path(drive).resolve())
                self.is_dir = True
                drive_list.append(self.data())
        self.send('file.open', drive_list)
        return drive_list

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
                self.name = item.name
                self.path = str(Path(item).resolve())
                self.is_dir = True
                dir_list.append(self.data())
        self.send('file.open.dir_list',dir_list)
        return dir_list

    def get_file_list(self,path):
        """
        获取目标目录文件列表
        :return:
        """
        file = Path(path)
        file_list = []
        if file.is_dir():
            for item in file.iterdir():
                if item.is_file():
                    self.name = item.name
                    self.path = str(item.resolve())
                    self.is_dir = False
                    self.size = item.stat().st_size
                    self.modified = item.stat().st_mtime
                    self.ext = item.suffix
                    file_list.append(self.data())
            self.send('file.open.file_list',self.read_file_filter(file_list))
        return file_list

    def read_file_filter(self,filelist:list):
        re_data = []
        if filelist:
            for item in filelist:
                ext = item['ext']
                if ext in self.filter_list:
                    re_data.append(item)
        return re_data

    def send(self,types,message):
        """
        发送文件数据信息
        :return:
        """
        data = {
            "type": types,
            "data": message
        }
        self.msgsend.sendmessage(data)

    def go_back(self):
        pass

    def search(self):
        pass

    def response_execution(self,message:dict):
        """
        前端返回信息执行器
        :return:
        """
        types = message['type']
        control_actuator = {
            'file.open':self.get_drive_letter,
            'file.open.dir_list':self.get_dir_list,
            'file.open.file_list':self.get_file_list,
            'file.back':self.go_back,
            'file.search':self.search,
            'file.filter':self._get_filter_list,
        }
        if types in control_actuator:
            control_actuator[types]()


def test():
    openfile = OpenFileDialog()
    drive = openfile.get_drive_letter()
    dir_list = openfile.get_dir_list(drive[2]['path'])
    file_list = openfile.get_file_list(dir_list[14]['path'])
    for i in file_list:
        print(i)


if __name__ == "__main__":
    test()