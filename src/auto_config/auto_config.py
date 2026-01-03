from typing import Optional, Dict, Any


class ModelTrainSetData:
    def __init__(self):
        self.model:Optional[str] = None # 模型名称
        self.data:Optional[str] = None # 数据集名称
        self.epochs:Optional[int] = 50 # 训练轮数
        self.time:Optional[float] = None # 训练时长
        self.patience:Optional[int] = 100 # 训练中断检测
        self.batch:Optional[int|float] = 16 # 训练批次
        self.imgsz:Optional[int] = 640 # 训练图片尺寸
        self.save:Optional[bool] = True # 模型保存
        self.save_period:Optional[int] = -1 # 模型保存间隔
        self.cache:Optional[bool] = True # 缓存数据集
        self.device:Optional[int|str|list] = None # 训练设备
        self.workers:Optional[int] = 8 # 训练线程数
        self.project:Optional[str] = None # 模型保存目录
        self.name:Optional[str] = None # 模型保存名称
        self.exist_ok:Optional[bool] = False # 覆盖模式
        self.pretrained:Optional[bool|str] = True # 模型预训练
        self.optimizer:Optional[str] = 'auto' # 优化器
        self.seed:Optional[int] = 0 # 随机数种子
        self.deterministic:Optional[bool] = True # 固定随机数
        self.single_cls:Optional[bool] = False # 单类别模式
        self.classes:Optional[list[int]] = None # 类别
        self.rect:Optional[bool] = False
        self.multi_scale:Optional[bool] = False
        self.cos_lr:Optional[bool] = False
        self.close_mosaic:Optional[int] = 10
        self.resume:Optional[bool] = False
        self.amp:Optional[bool] = True
        self.fraction:Optional[float] = 1.0
        self.profile:Optional[bool] = False
        self.freeze:Optional[int|list] = None
        self.lr0:Optional[float] = 0.01
        self.lrf:Optional[float] = 0.01
        self.momentum:Optional[float] = 0.937
        self.weight_decay:Optional[float] = 0.0005
        self.warmup_epochs:Optional[float] = 3.0
        self.warmup_momentum:Optional[float] = 0.8
        self.warmup_bias_lr:Optional[float] = 0.1
        self.box:Optional[float] = 7.5
        self.cls:Optional[float] = 0.5
        self.dfl:Optional[float] = 1.5
        self.pose:Optional[float] = 12.0
        self.kobj:Optional[float] = 2.0
        self.nbs:Optional[int] = 64
        self.overlap_mask:Optional[bool] = True
        self.mask_ratio:Optional[int] = 4
        self.dropout:Optional[float] = 0.0
        self.val:Optional[bool] = True
        self.plots:Optional[bool] = False
        self.compile:Optional[bool|str] = False

    def train_set(self) -> Dict[str, Any]:
        data = {
            'Model': self.model,
            'data': self.data,
            'epochs': self.epochs,
            'time': self.time,
            'patience': self.patience,
            'batch': self.batch,
            'imgsz': self.imgsz,
            'save': self.save,
            'save_period': self.save_period,
            'cache': self.cache,
            'device': self.device,
            'workers': self.workers,
            'project': self.project,
            'name': self.name,
            'exist_ok': self.exist_ok,
            'pretrained': self.pretrained,
            'optimizer': self.optimizer,
            'seed': self.seed,
            'deterministic': self.deterministic,
            'single_cls': self.single_cls,
            'classes': self.classes,
            'rect': self.rect,
            'multi_scale': self.multi_scale,
            'cos_lr': self.cos_lr,
            'close_mosaic': self.close_mosaic,
            'resume': self.resume,
            'amp': self.amp,
            'fraction': self.fraction,
            'profile': self.profile,
            'lr0': self.lr0,
            'lrf': self.lrf,
            'momentum': self.momentum,
            'weight_decay': self.weight_decay,
            'warmup_epochs': self.warmup_epochs,
            'warmup_momentum': self.warmup_momentum,
            'warmup_bias_lr': self.warmup_bias_lr,
            'box': self.box,
            'cls': self.cls,
            'dfl': self.dfl,
            'pose': self.pose,
            'kobj': self.kobj,
            'nbs': self.nbs,
            'overlap_mask': self.overlap_mask,
            'mask_ratio': self.mask_ratio,
            'dropout': self.dropout,
            'val': self.val,
            'plots': self.plots,
            'compile': self.compile,
            'freeze': self.freeze,
        }
        return data

class DefaultPathSet:
    LIBRARY = '../../Library'
    FULL_DATASET = '../../Library/Dataset' # 数据集目录
    FULL_DATASET_CORE_SET = '../../Library/Dataset/core_set' # 核心数据集目录
    FULL_DATASET_RAW_DATA = '../../Library/Dataset/raw_data' # 原始数据集目录
    FULL_DATASET_RAW_DATA_IMAGE = '../../Library/Dataset/raw_data/image' # 原始数据集图片目录
    FULL_DATASET_RAW_DATA_VIDEO = '../../Library/Dataset/raw_data/video' # 原始数据集视频目录
    FULL_DATASET_TRAIN_SET = '../../Library/Dataset/train_set' # 训练数据集目录
    MODEL = '../../Library/Model' # 模型目录
    MODEL_ANNOTATION_MODEL_HUB = '../../Library/Model/annotation_model_hub' # 标注模型库
    MODEL_TRAINING_HUB = '../../Library/Model/model_training_hub' # 模型训练库
    MODEL_TRAINING_CONFIG = '../../Library/Model/model_training_hub/config' # 模型训练配置目录
    MODEL_TRAINING_MODEL_HUB = '../../Library/Model/model_training_hub/model_hub' # 模型训练模型目录
    MODEL_TRAINING_HUB_TRAINING_LOG = '../../Library/Model/model_training_hub/training_log' # 模型训练记录目录


class AutoConfig:...