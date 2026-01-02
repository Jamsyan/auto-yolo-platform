# -*- coding: utf-8 -*-
import os

from ultralytics import YOLO

from autoconfig.auto_config import ModelTrainSetData, DefaultPathSet


class YoloTrain:
    def __init__(self,model='yolo11n.pt'):
        self.model_training_hub = DefaultPathSet.MODEL_TRAINING_HUB # 模型训练集
        self.model_hub = DefaultPathSet.MODEL_TRAINING_MODEL_HUB # 模型集
        self.config_hub = DefaultPathSet.MODEL_TRAINING_CONFIG # 模型配置集

        self.model = model

        self.config = ModelTrainSetData()

    def load_model(self):
        model_path = os.path.join(self.model_hub,self.model)
        return YOLO(model_path)

    def train(self,config_file=None,project=None):
        project = project if project else 'train_project'
        cfph = os.path.join(self.config_hub,config_file)
        if not os.path.exists(cfph):
            return '[错误]---模型配置文件不存在'
        model = self.load_model()  # 加载模型
        # 模型训练参数
        config = self.config
        config.batch = 0.7
        config.epochs = 50
        config.data = cfph
        config.save = True
        config.project = project
        config.plots = True
        config.save_period = 5
        config.device = 'cuda:0'
        config.rect = True
        model.train(**config.train_set())

    def predict(self):
        model = self.load_model()


    def val(self,model_name = None):
        config = self.config
        self.model = self.model if model_name is None else self.model # 模型名称
        model = self.load_model()
        model.val(**config.train_set())

if __name__ == '__main__':
    pass