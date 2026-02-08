<div align="center">
  <img src="img/images.png" width="200" alt="叠层光电探测器 AI 设计平台">

  <h1>叠层光电探测器 AI 设计平台</h1>

  <p>
    <strong>基于大语言模型与 RAG 知识增强的智能光电探测器结构设计系统</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
    <img src="https://img.shields.io/badge/DeepSeek-R1%20%2F%20V3-7C3AED?style=flat-square" alt="DeepSeek">
    <img src="https://img.shields.io/badge/FAISS-Vector%20DB-0467DF?style=flat-square&logo=meta&logoColor=white" alt="FAISS">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  </p>

  <p>
    <a href="#-快速开始">快速开始</a> · <a href="#-核心功能">核心功能</a> · <a href="#-技术架构">技术架构</a> · <a href="#-使用指南">使用指南</a>
  </p>
</div>

---

## 📖 简介

本项目是一个面向科研人员和工程师的 **智能光电探测器辅助设计平台**。系统将 DeepSeek 大语言模型的深度推理能力与基于学术文献的 RAG（检索增强生成）技术相结合，能够根据用户指定的材料参数与应用需求，自动生成完整的叠层器件结构方案，并提供性能预测、备选材料推荐及优化建议。

> **适用场景：** 光电探测器结构预研、材料方案快速筛选、器件设计方案对比参考。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **智能结构设计** | AI 自动生成包含顶/底电极、电子/空穴传输层、光吸收层等完整叠层结构 |
| **双模式 AI 引擎** | 深度思考模式（DeepSeek-R1）提供深度推理；快速模式（DeepSeek-V3）满足高效需求 |
| **RAG 知识增强** | 基于 30+ 篇学术文献构建向量数据库，检索相关文献辅助 AI 设计，方案更具学术依据 |
| **多材料体系支持** | 覆盖量子点、单晶、多晶、二维材料、钙钛矿等多种材料类别 |
| **备选材料推荐** | 每层提供 2-3 种备选材料方案，含禁带宽度、优缺点对比 |
| **交互式可视化** | 层叠结构条形图、光谱响应曲线图，支持缩放与交互 |
| **流式推理展示** | 实时展示 AI 推理过程，直观了解设计思路 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 1. 克隆项目

```bash
git clone <仓库地址>
cd <项目目录>
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# DeepSeek API 密钥（必需）
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# Flask 应用密钥（建议修改为随机字符串）
FLASK_SECRET_KEY=your-random-secret-key

# 阿里云 DashScope API 密钥（RAG 功能需要）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

> **获取 API 密钥：**
> - DeepSeek：[platform.deepseek.com](https://platform.deepseek.com/)
> - DashScope：[dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/)

### 4. 启动应用

**开发环境：**

```bash
python app.py
```

**生产环境（Gunicorn）：**

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

启动后访问 http://localhost:5000 即可使用。

---

## 📂 项目结构

```
├── app.py                     # Flask 主应用，路由与业务逻辑
├── deepseek_api.py            # DeepSeek API 封装，含流式/非流式调用
├── rag_service.py             # RAG 知识库服务，向量检索与文献增强
├── visualize.py               # 基于 pyecharts 的可视化图表生成
├── wsgi.py                    # WSGI 入口（生产部署用）
├── gunicorn_config.py         # Gunicorn 服务器配置
├── requirements.txt           # Python 依赖清单
├── .env                       # 环境变量配置（需自行创建）
│
├── templates/                 # Jinja2 页面模板
│   ├── index.html             #   输入页面 — 材料参数配置
│   ├── thinking.html          #   思考页面 — AI 推理过程展示
│   ├── result.html            #   结果页面 — 设计方案与可视化
│   └── navbar.html            #   导航栏组件
│
├── static/                    # 静态资源
│   ├── css/style.css          #   全局样式
│   ├── js/                    #   JavaScript 脚本
│   └── images/                #   生成的可视化图表（运行时产生）
│
├── data/                      # 学术文献 PDF（RAG 知识库来源）
├── vector_db/                 # FAISS 向量数据库（预构建）
│   ├── index.faiss            #   向量索引文件
│   └── index.pkl              #   元数据文件
│
├── vector_database_save.py    # 工具脚本 — 从 PDF 创建向量数据库
├── vector_database_add.py     # 工具脚本 — 向现有数据库追加文档
├── vector_database_use.py     # 工具脚本 — 向量数据库查询测试
└── RAG_test.py                # RAG 功能测试脚本
```

---

## 🛠️ 技术架构

```
┌─────────────────────────────────────────────────────┐
│                    用户浏览器                        │
│            Bootstrap 5 + ECharts 前端                │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / SSE
┌───────────────────────▼─────────────────────────────┐
│              Flask Web 应用 (app.py)                 │
│         路由管理 · Session · 流式响应                  │
├─────────────────┬───────────────────┬───────────────┤
│  DeepSeek API   │   RAG Service     │  Visualize    │
│  (deepseek_api) │  (rag_service)    │ (visualize)   │
│                 │                   │               │
│  · R1 深度推理   │  · 文献向量检索    │  · 结构图      │
│  · V3 快速生成   │  · 上下文增强      │  · 响应度曲线  │
│  · 流式输出      │  · Top-K 匹配     │  · pyecharts  │
├─────────────────┼───────────────────┤               │
│  DeepSeek Cloud │  FAISS + DashScope│               │
│  (外部 API)      │  (本地向量数据库)   │               │
└─────────────────┴───────────────────┴───────────────┘
```

**关键技术栈：**

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端 | Bootstrap 5, ECharts, Font Awesome | 响应式布局，交互式图表 |
| 后端 | Flask 3.0, Gunicorn + gevent | 支持流式响应的 Web 框架 |
| AI 模型 | DeepSeek R1 / V3 | 深度推理与快速生成双模式 |
| RAG | LangChain, FAISS, DashScope Embeddings | 基于学术文献的检索增强生成 |
| 可视化 | pyecharts | 层叠结构图、光谱响应曲线 |

---

## 📝 使用指南

### 设计流程

1. **配置材料参数** — 在输入页面选择材料类别，设置禁带宽度范围、薄膜厚度范围
2. **指定应用场景** — 选择目标应用（如紫外探测、近红外探测等），可填写额外需求
3. **选择 AI 模式** — 深度思考模式（推荐，推理更充分）或快速模式（响应更快）
4. **等待 AI 推理** — 系统实时展示推理进度与思考过程
5. **查看设计结果** — 包含完整叠层结构、各层材料参数、性能预测、备选方案及优化建议

### AI 输出内容

设计结果包含以下信息：

- **叠层结构**：从顶电极到底电极的完整层叠设计，每层包含材料、厚度、禁带宽度、功能描述及制备工艺
- **备选材料**：每层提供 2-3 种替代材料方案，包含优缺点对比
- **性能预测**：波长响应范围、响应度曲线数据、量子效率、暗电流等关键指标
- **优化建议**：针对当前设计的改进方向与策略

### 管理知识库

**创建向量数据库（首次使用）：**

```bash
# 将 PDF 论文放入 data/ 文件夹后运行
python vector_database_save.py
```

**追加新文献：**

```bash
# 将新 PDF 放入 data_new/ 文件夹后运行
python vector_database_add.py
```

---

## ⚙️ 部署说明

### 生产部署（Gunicorn）

项目内置了 `gunicorn_config.py` 配置，推荐使用 gevent 工作模式以支持流式响应：

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

主要配置参数：

| 参数 | 默认值 | 说明 |
|------|-------|------|
| `workers` | 4 | 工作进程数 |
| `worker_class` | gevent | 协程模式，支持流式响应 |
| `timeout` | 600s | 请求超时（AI 推理耗时较长） |
| `bind` | 0.0.0.0:8000 | 监听地址 |

### Windows 开发环境

```bash
# 使用项目内置的启动脚本
run.bat
```

---

## ⚠️ 注意事项

- 请确保 DeepSeek API Key 有效且有足够的调用额度
- RAG 功能需要配置阿里云 DashScope API Key
- 深度思考模式（R1）推理时间较长（通常 1-3 分钟），请耐心等待
- **设计结果仅供科研参考，实际器件性能需经实验验证**
- 请勿将 API Key 提交到公开代码仓库

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

---

<div align="center">
  <sub>Powered by <b>Flask</b> · <b>DeepSeek AI</b> · <b>LangChain</b> · <b>FAISS</b></sub>
</div>
