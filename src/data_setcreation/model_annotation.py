# -*- coding: utf-8 -*-
import os
import random

from ultralytics import YOLO

from auto_config.auto_config import DefaultPathSet


class FaceAnnotation:
    def __init__(self):
        self.annotation_model_hub = DefaultPathSet.MODEL_ANNOTATION_MODEL_HUB  # 模型库
        self.out_dataset_dir = DefaultPathSet.FULL_DATASET_TRAIN_SET  # 输出数据集目录
        self.ready_annotation_dir = DefaultPathSet.FULL_DATASET_RAW_DATA_IMAGE  # 需要标注的数据集目录

        self.annotation_model = 'yolo11m.pt'  # 模型名称
        self.image_batch_size_num = 30  # 单批次标注照片数量，不要设置太大，除非显卡性能足够
        self.dataset_obj = None  # 验证集/训练集类型
        self.obj_tag = None  # 参数默认为空,如果存在则已内容命名并创建路径存入全部标注数据
        self.val_value = None  # 验证集比例
        self.model = None  # 模型
        self.annotation_config()  # 模型参数配置

    def load_model(self, model_hub=None, model_name=None):
        model = self.annotation_model if model_name is None else model_name  # 模型名称
        model_hub = self.annotation_model_hub if model_hub is None else model_hub  # 模型库
        model_path = os.path.join(model_hub, model)
        self.model = YOLO(model_path)  # 加载模型
        return self.model

    def annotation_config(self):
        self.source = None
        self.save_txt = False
        self.save = False
        self.verbose = False
        self.batch = 0.7
        self.device = 'cuda:0'
        self.stream = True

    def face_annotation(self, annotation_data, out_dataset_dir=None):
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
        pkg_name, path_list = annotation_data
        pkg_name = pkg_name if self.obj_tag is None else self.obj_tag
        result = self.model.predict(
            source=path_list if path_list else self.source,
            save_txt=self.save_txt,
            save=self.save,
            verbose=self.verbose,
            batch=self.batch,
            device=self.device,
            stream=self.stream,
        )
        for command, image_path in zip(result, path_list):
            file_name = os.path.basename(image_path).split('.')[0]  # 获取文件名称
            for i in ['images', 'labels']:  # 文件路径检查
                path = os.path.join(out_dataset_dir, pkg_name, i, dataset_obj)
                os.makedirs(name=path, exist_ok=True)
            # 图片文件保存
            sec_path = 'images'
            path = os.path.join(out_dataset_dir, pkg_name, sec_path, dataset_obj, f'{file_name}.jpg')
            command.save(str(path), labels=False, conf=False)
            # 表述文件保存
            sec_path = 'labels'
            path = os.path.join(out_dataset_dir, pkg_name, sec_path, dataset_obj, f'{file_name}.txt')
            command.save_txt(str(path))

    def get_image_path(self, path=None):
        """
        获取图片列表,创建待处理数据队列字典
        :param path:
        :return:
        """
        ready_path = self.ready_annotation_dir if path is None else path
        result: dict[str, list] = {}
        pkg_name_list = os.listdir(ready_path)
        for pkg_name in pkg_name_list:  # 获取包名称
            image_path_list = []
            pkg_dir_path = os.path.join(ready_path, pkg_name)
            image_name_list = os.listdir(pkg_dir_path)
            for image_name in image_name_list:
                image_path = os.path.join(pkg_dir_path, image_name)
                image_path_list.append(image_path)
            result[pkg_name] = image_path_list
        return result

    def execution_manager(self, data, batch_size=None):  # 数据集执行管理
        """
        数据集输出目标指向
        :param data:
        :param batch_size:
        :return:
        """
        key = list(data.keys())
        tag = '训练' if self.dataset_obj == 'train' else '验证'
        batch_size = self.image_batch_size_num if batch_size is None else batch_size
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

    def data_splitting(self, data, val_value=0.25):
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