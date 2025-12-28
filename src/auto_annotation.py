# -*- coding: utf-8 -*-
import os
import cv2
import random
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from auto_config import DefaultPathSet
from servers.api.progressbar import ProgressBar

class VideoFrameExtractor:
    def __init__(self,video=None,out=None):
        self.video = video
        self.out = out
        self.skip_list = []
        self.pbar = ProgressBar()

    def extract_frame_with_image(self,variant=True):
        """
        从视频中提取出图像数据,并保存到输出路径
        :param variant: True|False 默认True 执行图片变体生成
        :return
        """
        cap = cv2.VideoCapture(self.video)
        if cap.isOpened():
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.pbar.submit(task_id=2,
                             task_name=f'从视频{self.video}中提取出图像数据',
                             total=frame_count)
            package_name = Path(self.video).stem
            path = Path(self.out).joinpath(package_name)
            path.mkdir(parents=True, exist_ok=True)
            for index in range(frame_count):
                ret, frame = cap.read()
                frame = cv2.resize(frame, (360, 640))  # 切割尺寸
                image_name = f'row_image_{index}.jpg'
                filename = str(path/image_name)
                cv2.imwrite(filename=filename, img=frame)  # 写出原始图片文件
                self.pbar.log = f'正在处理第{index}帧数据...'
                if variant: # 图片变体
                    self.extract_frame_with_variants(frame=frame,index=index) # 图片变体
        cap.release()

    def extract_frame_with_variants(self, frame,index=None):
        """
        实现图像数据变体,以用于数据增强
        :param frame: 输入的图片或帧数据对象
        :param index: 输入文件命名序列
        :return:
        """
        b, g, r = cv2.split(frame)
        zeros = np.zeros_like(frame[:, :, 0])
        # 原始图片变体
        red_only = cv2.merge([zeros, zeros, r])  # 去红通道
        green_only = cv2.merge([zeros, g, zeros])  # 去绿通道
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度图
        blur_frame = cv2.GaussianBlur(frame, (13, 43), 0)  # 高斯模糊
        bright_frame = cv2.convertScaleAbs(src=frame, alpha=1, beta=2)  # 高曝光
        # 命名编码集
        ch_frame_list = [gray_frame, blur_frame, bright_frame, red_only, green_only, ]
        ch_frame_list_name = ['change_gray', 'change_blur', 'change_bright',
                            'change_onlyred', 'change_onlygreen']
        # 输出
        package_name = Path(self.video).stem
        path = Path(self.out).joinpath(package_name)
        path.mkdir(parents=True, exist_ok=True)
        for name, image in zip(ch_frame_list_name, ch_frame_list):
            image_name = f'{name}_{index}.jpg'
            filename = str(path/image_name)
            cv2.imwrite(filename=filename,img=image)  # 输出变体文件
            self.pbar.log = f'正在处理第{index}帧数据{name}变体...'
        self.pbar.update(task_id=2)

    def pre_execution_check(self):
        """
        主流程执行前检查
        :return:
        """
        def check(_video):
            package_count = len([i for i in Path(self.out).iterdir()])
            if package_count == 0:
                return True
            cap = cv2.VideoCapture(_video)
            if cap.isOpened():
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                package_name = Path(_video).stem
                path = Path(self.out).joinpath(package_name)
                path.mkdir(parents=True, exist_ok=True)
                file_count = len([i for i in Path(path).iterdir()])
                cap.release()
                if file_count == frame_count or file_count == frame_count*6:
                    _text = f'[提示]---检测到视频{_video}对应数据集已存在,已自动跳过...'
                    print(_text)
                    return False
                else:
                    return True
            return None

        # 路径参数输入存在检查
        status = {'video':False,'out':False}
        if self.video is None: # 没有输入视频文件/目录
            self.video = str(Path(DefaultPathSet.FULL_DATASET_RAW_DATA_VIDEO).resolve())
            status['video'] = True
            text = f'[提示]---未找到视频文件/目录,已自动选择默认视频文件目录:{self.video}'
            print(text)
        if self.out is None: # 没有设置输出路径
            self.out = str(Path(DefaultPathSet.FULL_DATASET_RAW_DATA_IMAGE).resolve())
            status['out'] = True
            text = f'[提示]---未找到图片输出目录,已自动选择默认图片输出目录:{self.out}'
            print(text)
        else: # 是自定义输出路径
            if not Path(self.out).is_dir():
                Path(self.out).mkdir(parents=True, exist_ok=True)
                text = f'[提示]---检测到自定义输出路径不存在已自动创建图片输出目录:{self.out}'
                print(text)
                return True
        if status['video']: # 是默认视频目录路径
            video = [i for i in Path(self.video).iterdir()]
            if len(video) == 0:
                text = f'[错误]---未找到视频文件,请检查是否正确导入视频数据'
                print(text)
                return False
            for item in video:
                if check(item):
                    continue
                else:
                    self.skip_list.append(item)
                if len(video) <= len(self.skip_list):
                    return False
            return True
        else: # 自定义视频文件/目录路径
            if isinstance(self.video, str): # 是文件路径
                if Path(self.video).is_file():
                    return check(self.video)
                elif Path(self.video).is_dir(): # 是目录路径
                    video = [i for i in Path(self.video).iterdir()]
                    if len(video) == 0:
                        text = f'[错误]---未找到视频文件,请检查视频文件路径是否正确'
                        print(text)
                        return False
                    for item in video:
                        if check(item):
                            continue
                        else:
                            self.skip_list.append(item)
                    if len(video) <= len(self.skip_list):
                        return False
                    return True
            elif isinstance(self.video, list): # 是列表
                for item in self.video:
                    if Path(item).is_file(): # 是文件
                        if check(item):
                            continue
                        else:
                            self.skip_list.append(item)
                    elif Path(item).is_dir(): # 是目录
                        self.skip_list.append(item)
                if len(self.video) <= len(self.skip_list):
                    return False
                return True
            return None

    def execute(self):
        if self.pre_execution_check():
            if isinstance(self.video, str):
                if Path(self.video).is_file():
                    self.pbar.submit(task_id=1,task_name=f"处理文件{self.video}",total=1)
                    self.pbar.log=f"[提示]---检测到文件,已自动切换模式"
                    self.extract_frame_with_image()
                    self.pbar.log=f"处理文件{self.video}完成"
                    self.pbar.update(task_id=1)
                elif Path(self.video).is_dir():
                    total = len([i for i in Path(self.video).iterdir()])
                    self.pbar.submit(task_id=1, task_name=f"处理路径{self.video}", total=total)
                    self.pbar.log=f'[提示]---检测到路径,已自动切换模式'
                    temp = self.video
                    for item in Path(temp).iterdir():
                        if item in self.skip_list:
                            self.pbar.log=f"文件{item}已跳过"
                            self.pbar.update(task_id=1)
                            continue
                        self.video = item
                        self.extract_frame_with_image()
                        self.pbar.log="处理文件{item}"
                        self.pbar.update(task_id=1)
                    self.pbar.log=f"处理路径{self.video}完成"
                    self.pbar.update(task_id=1)
            elif isinstance(self.video, list):
                self.pbar.submit(task_id=1, task_name=f"处理批量数据{self.video}", total=len(self.video))
                self.pbar.log=f'[提示]---检测到批量数据,已自动切换模式'
                temp = self.video
                for item in temp:
                    if item in self.skip_list:
                        self.pbar.log=f"文件{item}已跳过"
                        continue
                    elif Path(item).is_file():
                        self.pbar.log=f"处理文件{item}"
                        self.video = item
                        self.extract_frame_with_image()
                        self.pbar.log=f"处理文件{item}完成"
                    else:
                        self.pbar.log=f'[错误]---批量数据{item}不是合法文件'
                        raise FileNotFoundError(self.pbar.log)
                    self.pbar.update(task_id=1)
            self.pbar.log = f'[提示]---数据处理完成'
            self.pbar.update(task_id=1)

class FaceAnnotation:
    def __init__(self):
        self.annotation_model_hub = DefaultPathSet.MODEL_ANNOTATION_MODEL_HUB # 模型库
        self.out_dataset_dir = DefaultPathSet.FULL_DATASET_TRAIN_SET  # 输出数据集目录
        self.ready_annotation_dir = DefaultPathSet.FULL_DATASET_RAW_DATA_IMAGE # 需要标注的数据集目录
        
        self.annotation_model = 'yolo11m.pt'  # 模型名称
        self.image_batch_size_num = 30 # 单批次标注照片数量，不要设置太大，除非显卡性能足够
        self.dataset_obj = None # 验证集/训练集类型
        self.obj_tag = None # 参数默认为空,如果存在则已内容命名并创建路径存入全部标注数据
        self.val_value = None # 验证集比例
        self.model = None # 模型
        self.annotation_config() # 模型参数配置

    def load_model(self, model_hub = None, model_name = None):
        model = self.annotation_model if model_name is None else model_name # 模型名称
        model_hub = self.annotation_model_hub if model_hub is None else model_hub # 模型库
        model_path = os.path.join(model_hub, model)
        self.model = YOLO(model_path) # 加载模型
        return self.model


    def annotation_config(self):
        self.source = None
        self.save_txt = False
        self.save = False
        self.verbose = False
        self.batch = 0.7
        self.device = 'cuda:0'
        self.stream = True

    def face_annotation(self, annotation_data, out_dataset_dir = None):
        """
        面部标注执行
        :param annotation_data:
        :param out_dataset_dir:
        :return:
        """
        out_dataset_dir = self.out_dataset_dir if out_dataset_dir is None else out_dataset_dir
        dataset_obj = self.dataset_obj
        if dataset_obj is None:
            raise ValueError('[错误]---类型地址dataset_obj不能为None')
        pkg_name,path_list = annotation_data
        pkg_name = pkg_name if self.obj_tag is None else self.obj_tag
        result = self.model.predict(
            source=path_list if path_list else self.source,
            save_txt=self.save_txt,
            save=self.save,
            verbose=self.verbose,
            batch = self.batch,
            device=self.device,
            stream=self.stream,
        )
        for command,image_path in zip(result,path_list):
            file_name = os.path.basename(image_path).split('.')[0] # 获取文件名称
            for i in ['images','labels']: # 文件路径检查
                path = os.path.join(out_dataset_dir, pkg_name, i, dataset_obj)
                os.makedirs(name=path, exist_ok=True)
            # 图片文件保存
            sec_path = 'images'
            path = os.path.join(out_dataset_dir, pkg_name, sec_path, dataset_obj, f'{file_name}.jpg')
            command.save(str(path),labels= False,conf=  False)
            # 表述文件保存
            sec_path = 'labels'
            path = os.path.join(out_dataset_dir, pkg_name, sec_path, dataset_obj, f'{file_name}.txt')
            command.save_txt(str(path))

    def get_image_path(self, path = None):
        """
        获取图片列表,创建待处理数据队列字典
        :param path:
        :return:
        """
        ready_path = self.ready_annotation_dir if path is None else path
        result:dict[str, list] = {}
        pkg_name_list = os.listdir(ready_path)
        for pkg_name in pkg_name_list: # 获取包名称
            image_path_list = []
            pkg_dir_path = os.path.join(ready_path,pkg_name)
            image_name_list = os.listdir(pkg_dir_path)
            for image_name in image_name_list:
                image_path = os.path.join(pkg_dir_path,image_name)
                image_path_list.append(image_path)
            result[pkg_name] = image_path_list
        return result

    def execution_manager(self, data, batch_size = None): # 数据集执行管理
        """
        数据集输出目标指向
        :param data:
        :param batch_size:
        :return:
        """
        key = list(data.keys())
        tag = '训练' if self.dataset_obj == 'train' else '验证'
        batch_size  = self.image_batch_size_num if batch_size is None else batch_size
        for pkg_name in key:
            cache = []
            path_list = data[pkg_name]
            if self.dataset_obj is None:
                raise ValueError('[错误]---类型地址dataset_obj不能为None')
            for image_path in path_list:
                cache.append(image_path)
                if len(cache) >= batch_size:
                    self.face_annotation(annotation_data=(pkg_name, cache))
                    cache = []
            if cache:
                self.face_annotation(annotation_data=(pkg_name, cache))

    def data_splitting(self,data, val_value = 0.25):
        """
        数据列表拆分
        :param data:
        :param val_value: 验证集数据占比
        :return:
        """
        val_value = val_value if self.val_value is None else self.val_value
        key = list(data.keys())
        train_data_list = {}
        val_data_list = {}
        for dir_name in key:
            if dir_name in os.listdir(self.out_dataset_dir):
                continue
            root_list = data[dir_name]
            random.shuffle(root_list)
            num_val = int(len(root_list) * val_value)
            train_data_list[dir_name] = root_list[num_val:]
            val_data_list[dir_name] = root_list[:num_val]
        return train_data_list, val_data_list

    def start_annotation(self):
        """
        标注主流程
        :return: None
        """
        self.load_model()
        data = self.get_image_path()
        train_data_list, val_data_list = self.data_splitting(data=data)
        # 数据集输出
        self.dataset_obj = 'train'
        self.execution_manager(data=train_data_list)
        self.dataset_obj = 'val'
        self.execution_manager(data=val_data_list)

def test(name):
    if name == 'video':
        frame = VideoFrameExtractor()
        frame.execute()

if __name__ == '__main__':
    test('video')