# 叠层光电探测器 AI 设计平台 (Stacked Photodetector AI Design Platform)

这是一个基于 Flask 框架和 DeepSeek 大模型构建的智能化叠层光电探测器设计系统。平台能够根据用户输入的材料参数和应用需求，利用 AI 进行深度推理，自动生成器件的叠层结构设计、性能预测及优化建议，并提供可视化的结构展示。

## 🌟 核心功能

*   **智能参数输入**：支持从多级分类（量子点、单晶、多晶、二维材料）中选择材料，并自定义禁带宽度、厚度范围及目标应用场景。
*   **双模式 AI 引擎**：
    *   **深度思考模式 (Deep Thinking)**：使用 DeepSeek Reasoner 模型，进行复杂的物理机制推理，适合高精度设计。
    *   **快速模式 (Fast Mode)**：使用 DeepSeek Chat 模型，快速生成设计方案，适合敏捷迭代。
*   **自动化结构设计**：AI 自动生成包含顶电极、电子传输层 (ETL)、光吸收层 (Absorber)、空穴传输层 (HTL) 及底电极的完整叠层结构。
*   **复合吸收层设计**：特别针对光吸收层进行优化，支持量子阱、超晶格、异质结等复合结构设计。
*   **可视化展示**：自动生成器件的层状结构示意图，直观展示各层材料、厚度及功能。
*   **实时思考过程**：展示 AI 的推理步骤，让设计过程透明化。

## 🛠️ 技术栈

*   **后端框架**: Python 3.13 + Flask 3.0
*   **AI 模型**: DeepSeek API (Reasoner / Chat)
*   **数据可视化**: Matplotlib
*   **前端界面**: HTML5, Bootstrap 5, JavaScript
*   **依赖管理**: pip (requirements.txt)

## 📂 项目结构

```text
DetectorDesign/
├── app.py              # Flask 主应用程序，处理路由和业务逻辑
├── deepseek_api.py     # DeepSeek API 调用封装，支持流式输出
├── visualize.py        # 结构可视化生成逻辑
├── utils.py            # 工具函数 (如 JSON 提取)
├── templates/          # HTML 模板文件
│   ├── index.html      # 参数输入页
│   ├── thinking.html   # AI 思考过程页
│   ├── result.html     # 设计结果展示页
│   └── navbar.html     # 导航栏组件
├── static/             # 静态资源 (CSS, JS, Images)
├── .env                # 环境变量配置文件
└── requirements.txt    # 项目依赖列表
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.8 或更高版本 (推荐 Python 3.13)。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

在项目根目录下创建或修改 `.env` 文件，填入你的 DeepSeek API Key 和 Flask Secret Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

### 4. 运行应用

**Windows:**
可以直接运行批处理文件：
```bash
run.bat
```
或者手动运行：
```bash
python app.py
```

**Linux/Mac:**
```bash
python app.py
```

启动后，访问浏览器打开 `http://localhost:5000` 即可使用平台。

## 📝 使用说明

1.  **选择材料**：在首页选择材料大类（如量子点），然后从下拉列表或手动输入具体材料。
2.  **设定参数**：输入期望的禁带宽度范围 (eV) 和厚度范围 (nm)。
3.  **选择应用**：选择目标应用场景（如太阳能电池、光通信等）。
4.  **选择模式**：根据需求选择"深度思考模式"或"快速模式"。
5.  **生成设计**：点击"开始设计"，系统将进入思考页面，实时展示 AI 的设计进度。
6.  **查看结果**：设计完成后，系统将展示详细的层叠结构表、性能预测数据、优化建议以及结构示意图。

## ⚙️ 工作原理

1.  **Prompt 构建**：系统将用户输入的参数封装为结构化的 Prompt，强制要求 AI 以 JSON 格式输出，并特别规定了光吸收层的复合结构要求。
2.  **LLM 推理**：调用 DeepSeek API，模型根据物理学知识和材料特性进行推理设计。
3.  **流式处理**：通过 Server-Sent Events (类似机制) 或流式响应，将 AI 的思考步骤实时反馈给前端。
4.  **数据解析与可视化**：后端解析 AI 返回的 JSON 数据，利用 Matplotlib 绘制结构图，并渲染最终结果页面。
5.  **结果缓存**：设计结果会暂时缓存在内存中（默认 24 小时），并通过定时任务自动清理过期数据。

## ⚠️ 注意事项

*   请确保 `.env` 文件中的 API Key 有效且有足够的额度。
*   生成的图像文件存储在 `static/images` 目录下，系统会自动定期清理。

---
Powered by Flask & DeepSeek AI
