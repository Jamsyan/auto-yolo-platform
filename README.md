# 基于YOLO模型的图像检测自动化训练与平台
### Automated training and platform for image detection based on YOLO model

本项目是一个基于YOLO模型的自动化图像检测训练平台，支持视频帧提取、自动标注、模型训练和验证等功能。项目提供了一个完整的图像检测训练流程，包括数据预处理、模型训练和结果可视化。

## 功能特性

- **视频帧提取**：从视频文件中自动提取图像帧，并支持多种数据增强技术（灰度图、高斯模糊、高曝光等）
- **自动标注**：使用YOLO模型对图像进行自动标注，支持训练集和验证集的自动划分
- **模型训练**：集成YOLO11模型，支持多种训练参数配置
- **进度监控**：提供实时训练进度监控和日志记录
- **Web API接口**：基于FastAPI的API接口，支持WebSocket实时通信
- **前端界面**：Vue.js前端界面，提供用户友好的操作体验

## 项目结构

```
<项目根目录>
├── app/                    # Vue.js前端应用
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── subcompoents/
│   │   │   └── ProgressBar.vue
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
├── src/                    # Python后端源码
│   ├── servers/            # 服务器相关模块
│   │   ├── api/
│   │   │   └── progressbar.py  # 进度条管理
│   │   ├── transportation_hub.py  # 传输中心
│   │   └── ws_server.py         # WebSocket服务器
│   ├── auto_annotation.py  # 视频帧提取、自动标注功能
│   ├── auto_config.py      # 路径与训练参数配置
│   ├── main.py             # 项目入口（FastAPI服务）
│   └── train.py            # YOLO模型训练与验证逻辑
├── Library/                # 数据与模型存储目录（自动生成）
│   ├── Dataset/            # 数据集
│   │   ├── core_set/       # 核心数据集
│   │   ├── raw_data/       # 原始数据（图像/视频）
│   │   └── train_set/      # 标注后训练集
│   └── Model/              # 模型相关
│       ├── annotation_model_hub/  # 标注用模型
│       └── model_training_hub/    # 训练用模型、配置、日志
│           ├── config/            # 训练配置文件
│           ├── model_hub/         # 训练用模型文件
│           └── training_log/      # 训练日志
├── README.md
└── pyproject.toml
```

## 安装依赖

确保已安装 Python 3.13 或更高版本，然后安装项目依赖：

```bash
pip install uv # 安装uv包管理器
uv venv # 创建虚拟环境
uv sync # 安装项目依赖
```

### CUDA支持

注意：ultralytics默认安装CPU版本的torch，如需使用CUDA，请先检查设备CUDA版本，如支持则执行以下操作：

```bash
uv pip uninstall torch torchvision -y # 卸载CPU版本
```

前往网站 https://pytorch.org/get-started/locally/ 按照需求选择CUDA版本，获得安装命令后执行：

```bash
uv pip install [你复制的torch安装命令]
```

## 使用方法

### 1. 启动后端服务

```bash
# 在项目根目录下运行
python src/main.py
```

### 2. 启动前端界面

```bash
# 进入app目录
cd app
npm install
npm run serve
```

### 3. 数据处理流程

1. 将原始视频数据放入 `Library/Dataset/raw_data/video` 目录
2. 运行视频帧提取功能，将视频转换为图像帧
3. 使用自动标注功能对图像进行标注
4. 配置训练参数并开始模型训练

### 4. 模型训练

```python
from train_model.train import YoloTrain

# 创建训练实例
trainer = YoloTrain(model='yolo11n.pt')

# 开始训练，指定配置文件
trainer.train(config_file='train_config.yaml', project='my_train_project')
```

## API接口

项目提供基于FastAPI的WebSocket接口，用于实时通信和进度监控：

- WebSocket端点：`ws://localhost:8000/api/`
- 实时传输训练进度和日志信息

## 项目配置

项目使用 [auto_config.py](file:///E:/Project/YOLO/src/auto_config.py) 进行配置管理，支持以下训练参数：

- 批次大小 (batch)
- 训练轮数 (epochs)
- 图像尺寸 (imgsz)
- 训练设备 (device)
- 学习率参数 (lr0, lrf)
- 以及其他YOLO训练所需的各种参数

## 技术栈

- **后端**: Python, FastAPI, Ultralytics YOLO
- **前端**: Vue.js 3
- **数据库**: 无（使用文件系统存储）
- **构建工具**: uv (Python), npm (JavaScript)
- **依赖管理**: pyproject.toml, package.json

## 系统架构

本项目采用前后端分离架构：

1. **后端服务**：使用FastAPI框架提供REST API和WebSocket接口，处理视频帧提取、自动标注和模型训练等核心功能
2. **前端界面**：使用Vue.js构建用户界面，提供数据收集、进度监控和系统概览等功能
3. **数据处理**：包含视频帧提取、数据增强、自动标注和模型训练等完整的数据处理流水线

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
```