# YOLO Project

这是一个基于 Ultralytics YOLO11 的目标检测项目。

## 项目结构

```
.
├── Library/
│   └── Model/
│       ├── annotation_model_hub/
│       └── model_training_hub/
│           ├── config/
│           └── training_log/
├── src/
│   ├── auto_annotation.py
│   ├── auto_config.py
│   ├── main.py
│   └── train.py
└── pyproject.toml
```

## 安装依赖

确保已安装 Python 3.13 或更高版本，然后安装项目依赖：

```bash
pip install -e .
```

或使用 pip 安装指定依赖：

```bash
pip install opencv-python pyside6 rich tensorboard ultralytics
```

## 使用方法

### 训练模型

要训练模型，请运行 [train.py](file:///E:/Project/YOLO/src/train.py) 脚本：

```bash
cd src
python train.py
```

训练配置可以在 [Library/Model/model_training_hub/config](file:///E:/Project/YOLO/Library/Model/model_training_hub/config) 目录中进行设置。

### 配置说明

模型训练的主要配置在 [src/auto_config.py](file:///E:/Project/YOLO/src/auto_config.py) 中定义，包括训练轮数、批次大小、图像尺寸等参数。

## 引用

如果您在研究中使用了此项目，请引用以下文献：

```bibtex
@software{yolo11_ultralytics,
  author = {Glenn Jocher and Jing Qiu},
  title = {Ultralytics YOLO11},
  version = {11.0.0},
  year = {2024},
  url = {https://github.com/ultralytics/ultralytics},
  orcid = {0000-0001-5950-6979, 0000-0003-3783-7069},
  license = {AGPL-3.0}
}
```

## 许可证

本项目根据 AGPL-3.0 许可证授权，详情请见 LICENSE 文件。