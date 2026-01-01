<div align="center">
  <img src="img/images.png" width="260" alt="项目Logo">

  <h1>叠层光电人工智能设计平台</h1>

  <p>
    <strong>堆叠式光电探测器人工智能设计平台</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Flask-3.0-green.svg" alt="Flask">
    <img src="https://img.shields.io/badge/AI-DeepSeek-purple.svg" alt="DeepSeek">
  </p>

  <p>
    AI深度推理 | 智能材料选择 | 渐进式设计 | RAG知识增强
  </p>
</div>

---

## 📖 简介

基于Flask和DeepSeek大语言模型的智能光电吸附设计系统。通过AI深度推理，根据用户输入的材料参数和应用需求，自动生成器件叠层结构设计、性能预测及优化建议。

## 📖 简介

基于 **Flask** 和 **DeepSeek** 大语言模型的智能光电探测器设计系统。通过 AI 深度推理，根据用户输入的材料参数和应用需求，自动生成器件叠层结构设计、性能预测及优化建议。

## ✨ 核心功能

- **智能材料选择**：支持量子点、单晶、多晶、二维材料等多种类别
- **双模式 AI 引擎**：深度思考模式 (R1) / 快速模式 (V3)
- **渐进式设计**：7 阶段思考流程，含自我评价与迭代优化
- **RAG 知识增强**：基于学术文献的检索增强生成
- **交互式可视化**：3D 层叠模型、性能曲线图
- **中英双语支持**：界面和 AI 输出均支持中英文切换

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
FLASK_SECRET_KEY=your-random-secret-key
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx  # RAG 功能需要
```

### 3. 启动应用

```bash
python app.py
```

访问 http://localhost:5000

## 📂 项目结构

```
├── app.py                 # Flask 主应用
├── deepseek_api.py        # DeepSeek API 封装
├── rag_service.py         # RAG 知识库服务
├── visualize.py           # 可视化生成
├── templates/             # 页面模板
├── static/                # 静态资源
├── data/                  # 学术文献 PDF
└── vector_db/             # 向量数据库
```

## 🛠️ 技术栈

- **后端**: Flask, DeepSeek API, LangChain, FAISS
- **前端**: Bootstrap 5, ECharts, CSS3
- **Embedding**: 阿里云 DashScope

## 📝 使用流程

1. **选择材料**：选择材料类别和具体材料
2. **配置参数**：设置禁带宽度、厚度范围、目标应用
3. **选择模式**：深度思考 / 快速模式，可启用渐进式设计
4. **生成设计**：AI 自动生成完整的器件结构
5. **查看结果**：层叠结构、性能参数、优化建议

## ⚠️ 注意事项

- 确保 API Key 有效且有足够额度
- 设计结果仅供参考，实际性能需实验验证
- 请勿将 API Key 提交到公开仓库

## 📄 许可证

MIT License


<div align="center">

Powered by **Flask** & **DeepSeek AI**

</div>



