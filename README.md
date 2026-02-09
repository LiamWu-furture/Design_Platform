<div align="center">
  <img src="img/images.png" width="560" alt="项目Logo">

  <h1>叠层光电探测器 AI 设计平台</h1>

  <p>
    <strong>基于大语言模型与 RAG 技术的智能光电探测器设计系统</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Flask-3.0-green.svg" alt="Flask">
    <img src="https://img.shields.io/badge/AI-DeepSeek-purple.svg" alt="DeepSeek">
    <img src="https://img.shields.io/badge/RAG-FAISS%20%2B%20LangChain-orange.svg" alt="RAG">
    <img src="https://img.shields.io/badge/Embedding-DashScope-red.svg" alt="DashScope">
  </p>

  <p>
    AI 深度推理 | 智能材料选择 | 渐进式设计 | RAG 知识增强 | 交互式可视化
  </p>
</div>

---

## 📖 简介

基于 **Flask** 和 **DeepSeek** 大语言模型的智能光电探测器设计系统。通过 AI 深度推理与 RAG（检索增强生成）技术，结合学术文献知识库，根据用户输入的材料参数和应用需求，自动生成器件叠层结构设计、性能预测及优化建议。

系统支持 **深度思考模式 (DeepSeek-R1)** 和 **快速模式 (DeepSeek-V3)** 两种推理引擎，并通过流式输出实时展示 AI 的推理过程，为科研人员和工程师提供专业的器件设计辅助工具。

## ✨ 核心功能

- **智能材料选择** - 支持量子点、单晶、多晶、二维材料等多种类别
- **双模式 AI 引擎** - 深度思考模式 (DeepSeek-R1) / 快速模式 (DeepSeek-V3)
- **RAG 知识增强** - 基于 30+ 篇学术文献的检索增强生成，设计方案有据可依
- **流式推理输出** - 实时展示 AI 推理过程，包含进度追踪与日志
- **交互式可视化** - 基于 PyECharts 的层叠结构图与光谱响应曲线
- **完整器件设计** - 自动生成包含电极、传输层、吸收层的完整叠层结构
- **备选材料推荐** - 每层提供 2-3 种备选材料及优缺点分析
- **优化建议生成** - 基于文献和 AI 分析提供器件性能优化方向

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制模板并填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx       # DeepSeek API 密钥（必需）
FLASK_SECRET_KEY=your-random-secret-key     # Flask 会话密钥（推荐修改）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx       # 阿里云 DashScope API 密钥（RAG 功能需要）
```

### 5. 构建向量数据库（首次使用）

将学术文献 PDF 放入 `data/` 目录，然后运行：

```bash
python scripts/vector_database_save.py
```

后续新增文献可放入 `data_new/` 目录，运行增量更新：

```bash
python scripts/vector_database_add.py
```

### 6. 启动应用

```bash
# 开发模式
python app.py

# 生产模式（使用 Gunicorn）
gunicorn -c gunicorn_config.py wsgi:app

# Windows 一键启动
run.bat
```

访问 http://localhost:5000

## 📂 项目结构

```
├── app.py                     # Flask 主应用，路由与业务逻辑
├── deepseek_api.py            # DeepSeek API 封装（流式/非流式调用 + RAG 集成）
├── rag_service.py             # RAG 知识库服务（FAISS 向量检索）
├── visualize.py               # PyECharts 可视化生成（结构图 + 性能曲线）
├── utils.py                   # 工具函数（JSON 解析等）
├── wsgi.py                    # WSGI 入口（Gunicorn 部署用）
├── gunicorn_config.py         # Gunicorn 生产配置
├── run.bat                    # Windows 一键启动脚本
├── requirements.txt           # Python 依赖列表
├── .env.example               # 环境变量模板（复制为 .env 后填入密钥）
│
├── templates/                 # Jinja2 页面模板
│   ├── index.html             #   参数输入页面
│   ├── thinking.html          #   AI 推理过程页面
│   ├── result.html            #   设计结果展示页面
│   └── navbar.html            #   导航栏组件
│
├── static/                    # 静态资源
│   ├── css/style.css          #   全局样式
│   ├── js/result.js           #   结果页交互逻辑
│   └── images/                #   运行时生成的可视化图表
│
├── scripts/                   # 工具脚本
│   ├── vector_database_save.py    # 向量数据库创建脚本
│   ├── vector_database_add.py     # 向量数据库增量更新脚本
│   ├── vector_database_use.py     # 向量数据库问答测试
│   └── RAG_test.py                # RAG 功能独立测试
│
├── data/                      # 学术文献 PDF（30+ 篇论文）
├── vector_db/                 # FAISS 向量数据库（运行时生成，已 gitignore）
│
├── docs/                      # 项目文档与笔记
│   ├── 创新点总结和建议.txt
│   ├── 向量数据库的创建.txt
│   └── 论文.docx
│
└── img/                       # 项目图片资源
    └── images.png             # 项目 Logo
```

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| **后端框架** | Flask 3.0, Gunicorn, Gevent |
| **AI 推理** | DeepSeek API (R1 / V3) |
| **RAG 引擎** | LangChain + FAISS 向量数据库 |
| **文本嵌入** | 阿里云 DashScope (text-embedding-v4) |
| **数据可视化** | PyECharts 2.0 |
| **前端** | Bootstrap 5, Font Awesome, CSS3 |
| **API 客户端** | OpenAI Python SDK, HTTPX |

## 📝 使用流程

1. **选择材料** - 在首页选择材料类别（量子点、单晶、多晶、二维材料等）
2. **配置参数** - 设置禁带宽度范围、厚度范围、目标应用及额外要求
3. **选择模式** - 深度思考 (R1) / 快速模式 (V3)
4. **AI 推理** - 系统检索相关文献，结合 RAG 知识增强进行设计推理
5. **查看结果** - 完整的叠层结构设计、交互式可视化图表、性能预测及优化建议

## 🔧 API 说明

系统设计输出的 JSON 结构包含：

- **layers** - 各层详细信息（材料、厚度、禁带宽度、功能、制备工艺、备选材料）
- **performance** - 性能参数（波长范围、响应度曲线、量子效率、暗电流）
- **optimization_suggestions** - 优化建议列表
- **explanation** - 设计说明（含文献引用）

## ⚠️ 注意事项

- 确保 DeepSeek API Key 和 DashScope API Key 有效且有足够额度
- 首次使用需运行 `python scripts/vector_database_save.py` 构建向量数据库
- 设计结果基于 AI 推理和文献参考，仅供科研参考，实际性能需实验验证
- 请勿将 `.env` 文件中的 API Key 提交到公开仓库
- 过期的设计结果会在 24 小时后自动清理

## 📄 许可证

MIT License


<div align="center">

Powered by **Flask** & **DeepSeek AI** & **LangChain RAG**

</div>

