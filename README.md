# 基于YOLO模型的图像检测自动化训练与平台
### Automated training and platform for image detection based on YOLO model
## 项目结构

``` python
<项目根目录>
├── src/
│   ├── main.py               # 项目入口（基础配置）
│   ├── train.py              # YOLO模型训练与验证逻辑
│   ├── auto_config.py        # 路径与训练参数配置
│   ├── auto_annotation.py    # 视频帧提取、自动标注功能
│   └── ui/
│       ├── main.py           # UI启动入口（PySide6）
│       └── ui.qml            # QML界面布局
└── Library/                  # 数据与模型存储目录（自动生成）
    ├── Dataset/              # 数据集
    │   ├── core_set/         # 核心数据集
    │   ├── raw_data/         # 原始数据（图像/视频）
    │   └── train_set/        # 标注后训练集
    └── Model/                # 模型相关
        ├── annotation_model_hub/  # 标注用模型
        └── model_training_hub/    # 训练用模型、配置、日志
            ├── config/            # 训练配置文件
            ├── model_hub/         # 训练用模型文件
            └── training_log/      # 训练日志
```

## 安装依赖

确保已安装 Python 3.13 或更高版本，然后安装项目依赖：

```bash
pip install uv # 安装uv
uv init # 初始化项目
uv add pyproject.toml # 添加依赖
```
注意:ultralytics默认torch版本为cpu,不支持cuda,若需要使用cuda请先检查设备cuda版本,若可以使用执行一下操作
```bash
uv pip uninstall torch torchvision # 卸载torch torchvision
```
前往网站 https://pytorch.org/get-started/locally/

![img.png](img.png)
按照需求选择,获得链接后选择复制下方命令,从torch开始
```bash
执行 uv add install [你复制的命令部分]
```
## 使用方法
项目还在开发中，请耐心等待。
## 致谢
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