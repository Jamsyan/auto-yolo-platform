from pathlib import Path

import win32file


class OpenFileDialog:
    def __init__(self):
        self.default = ""
        self.drive = []
        self.dir_list = []

    def get_drive_letter(self):
        # 获取驱动器列表
        check_mask = [3]
        for i in range(26):
            drive = fr'{chr(ord('A')+i)}:\\'
            mask = win32file.GetDriveType(drive)
            if mask in check_mask:
                path = Path(drive).resolve()
                self.drive.append(path)
            else:
                return

    def get_dir_list(self,path):
        # 获取目录列表
        if path and Path(path).is_dir():
            for item in Path(path).iterdir():
                self.dir_list.append(item)
            return
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

    def data_send(self):
        pass

    def go_back(self):
        pass

    def search(self):
        pass

    def response_execution(self):
        pass

def test():
    OpenFileDialog().get_drive_letter()

if __name__ == "__main__":
    test()