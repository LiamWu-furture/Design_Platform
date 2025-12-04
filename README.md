# 🔬 叠层光电探测器 AI 设计平台

<div align="center">

**Stacked Photodetector AI Design Platform**

*基于深度学习的智能化光电器件设计系统*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://www.deepseek.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 项目简介

这是一个基于 **Flask** 框架和 **DeepSeek** 大语言模型构建的智能化叠层光电探测器设计系统。平台通过 AI 深度推理，根据用户输入的材料参数和应用需求，自动生成完整的器件叠层结构设计、性能预测及优化建议，并提供交互式 3D 可视化展示。

### 🎯 设计目标

- **降低设计门槛**：无需深厚的半导体物理背景，即可快速获得专业的器件设计方案
- **加速研发迭代**：从传统的数周设计周期缩短至分钟级
- **提供决策支持**：为每层提供多个备选材料方案，帮助研究人员做出最优选择
- **知识传承**：通过 AI 推理过程展示，帮助学习者理解器件设计原理

---

## ✨ 核心功能

### 1️⃣ 智能材料选择系统
- **多级分类体系**：支持量子点、单晶、多晶、二维材料等多种材料类别
- **动态级联选择**：大类 → 子类 → 具体材料的三级联动
- **自定义输入**：支持手动输入未列出的新型材料
- **材料数据库**：内置常见光电材料的禁带宽度、特性参数

### 2️⃣ 双模式 AI 引擎
- **🧠 深度思考模式 (DeepSeek Reasoner)**
  - 进行复杂的物理机制推理
  - 考虑能带匹配、界面工程、载流子传输等多重因素
  - 适合高精度、高性能要求的设计场景
  
- **⚡ 快速模式 (DeepSeek Chat)**
  - 快速生成可行的设计方案
  - 适合概念验证和快速迭代
  - 响应时间更短，适合教学演示

### 3️⃣ 智能结构设计
- **完整层叠架构**：自动生成包含以下功能层的完整结构
  - 顶电极 (Top Electrode)
  - 电子传输层 (Electron Transport Layer, ETL)
  - 光吸收层 (Absorber Layer)
  - 空穴传输层 (Hole Transport Layer, HTL)
  - 底电极 (Bottom Electrode)
  - 必要的缓冲层和接触层

- **复合吸收层优化**：特别针对光吸收层进行优化
  - 支持量子阱结构
  - 支持超晶格结构
  - 支持异质结设计
  - 支持梯度带隙结构

### 4️⃣ 备选材料推荐 🆕
- **多方案对比**：为每一层提供 2-3 个备选材料
- **优缺点分析**：详细说明每个备选材料的优势和劣势
- **性能权衡**：帮助用户在成本、性能、工艺难度间做出平衡

### 5️⃣ 交互式可视化
- **3D 层叠模型**：可拖拽旋转的三维结构展示
- **层级信息标注**：点击层块查看详细参数
- **性能曲线图**：光谱响应度曲线的交互式展示
- **结构示意图**：清晰的二维层叠结构图

### 6️⃣ 实时推理过程
- **思考步骤可视化**：实时展示 AI 的设计推理过程
- **进度追踪**：显示设计进度和当前步骤
- **日志记录**：保存完整的推理日志供后续分析

---

## 🛠️ 技术栈

### 后端技术
- **核心框架**: Python 3.8+ / Flask 3.0
- **AI 引擎**: DeepSeek API (Reasoner R1 / Chat V3)
- **数据处理**: NumPy, Pandas
- **可视化**: Matplotlib, Plotly
- **环境管理**: python-dotenv

### 前端技术
- **UI 框架**: Bootstrap 5.3
- **图标库**: Font Awesome 6.4
- **交互脚本**: Vanilla JavaScript (ES6+)
- **样式**: CSS3 (含渐变、动画、3D 变换)

### 开发工具
- **依赖管理**: pip + requirements.txt
- **版本控制**: Git
- **API 调用**: OpenAI SDK (兼容 DeepSeek)

---

## 📂 项目结构

```text
DetectorDesign/
├── app.py                      # Flask 主应用，路由和业务逻辑
├── deepseek_api.py             # DeepSeek API 调用封装，支持流式输出
├── visualize.py                # 结构可视化生成（Matplotlib/Plotly）
├── utils.py                    # 工具函数（JSON 解析、数据处理）
├── rag_service.py              # RAG 知识库服务（可选）
│
├── templates/                  # Jinja2 模板文件
│   ├── index.html              # 参数输入页（材料选择、参数配置）
│   ├── thinking.html           # AI 思考过程页（实时推理展示）
│   ├── result.html             # 设计结果展示页（多选项卡布局）
│   └── navbar.html             # 导航栏组件
│
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css           # 全局样式表
│   ├── js/
│   │   ├── result.js           # 结果页交互逻辑（3D 模型、选项卡）
│   │   └── thinking.js         # 思考页动画和进度控制
│   └── images/                 # 生成的可视化图片（自动清理）
│
├── .env                        # 环境变量配置（API Key、密钥）
├── requirements.txt            # Python 依赖列表
├── run.bat                     # Windows 快速启动脚本
└── README.md                   # 项目文档
```

---

## 🚀 快速开始

### 前置要求

- **Python**: 3.8 或更高版本（推荐 3.10+）
- **DeepSeek API Key**: 从 [DeepSeek 官网](https://www.deepseek.com/) 获取
- **操作系统**: Windows / Linux / macOS

### 安装步骤

#### 1️⃣ 克隆项目

```bash
git clone <repository-url>
cd DetectorDesign
```

#### 2️⃣ 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包括：
- `Flask==3.0.0` - Web 框架
- `openai` - DeepSeek API 客户端
- `python-dotenv` - 环境变量管理
- `matplotlib` - 数据可视化
- `plotly` - 交互式图表

#### 4️⃣ 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Flask 应用配置
FLASK_SECRET_KEY=your-random-secret-key-here

# 可选：RAG 知识库配置
# ENABLE_RAG=true
```

> 💡 **提示**: 可以使用 `python -c "import secrets; print(secrets.token_hex(32))"` 生成随机密钥

#### 5️⃣ 启动应用

**方式一：使用启动脚本（Windows）**
```bash
run.bat
```

**方式二：直接运行**
```bash
python app.py
```

**方式三：开发模式（支持热重载）**
```bash
flask --app app run --debug
```

#### 6️⃣ 访问应用

打开浏览器访问：
```
http://localhost:5000
```

---

## 📝 使用指南

### 基础工作流程

#### 步骤 1: 材料选择
1. 在首页选择**材料大类**（量子点、单晶、多晶、二维材料）
2. 选择**材料子类**（如 IV 族量子点、II-VI 族量子点等）
3. 从下拉列表选择**具体材料**，或手动输入新材料名称

**支持的材料类型**：
- **量子点**: 硅、锗、CdSe、InP、钙钛矿等
- **单晶材料**: Si、GaAs、InP、SiC 等
- **多晶材料**: 多晶硅、CIGS、CdTe 等
- **二维材料**: 石墨烯、MoS₂、WSe₂、黑磷等

#### 步骤 2: 参数配置
- **禁带宽度范围**: 输入期望的禁带宽度范围（单位：eV）
  - 示例：0.5 - 3.0 eV（覆盖红外到紫外波段）
  
- **厚度范围**: 输入各层的厚度范围（单位：nm）
  - 示例：10 - 500 nm
  
- **目标应用**: 选择器件的应用场景
  - 太阳能电池
  - 光通信探测器
  - 图像传感器
  - 紫外探测器
  - 红外探测器
  - 其他（可自定义）

- **额外要求**（可选）: 输入特殊需求
  - 示例："需要高量子效率"、"低暗电流"、"宽光谱响应"

#### 步骤 3: 选择 AI 模式
- **🧠 深度思考模式**: 
  - 使用 DeepSeek Reasoner (R1)
  - 推理时间：30-60 秒
  - 适合：正式设计、高精度需求
  
- **⚡ 快速模式**: 
  - 使用 DeepSeek Chat (V3)
  - 推理时间：10-20 秒
  - 适合：快速验证、教学演示

#### 步骤 4: 生成设计
1. 点击**"开始设计"**按钮
2. 系统跳转到思考页面，实时显示：
   - AI 推理进度
   - 当前处理步骤
   - 推理日志（深度思考模式）
3. 等待设计完成（进度条达到 100%）

#### 步骤 5: 查看结果
设计完成后，结果页面包含 5 个选项卡：

**📋 设计参数**
- 显示用户输入的所有参数
- 便于核对和记录

**🏗️ 层叠结构**
- **3D 交互模型**: 可拖拽旋转的三维结构
  - 鼠标拖动旋转视角
  - 点击层块查看详细信息
  - 控制按钮快速调整视角
  
- **层详细信息列表**: 
  - 层名称、材料、厚度、禁带宽度
  - 功能描述、制备工艺
  - **备选材料** 🆕: 点击展开查看 2-3 个备选方案

**📊 可视化**
- 层叠结构示意图（交互式）
- 光谱响应曲线（可缩放、悬停查看数值）

**⚡ 性能参数**
- 波长响应范围
- 量子效率（IQE/EQE）
- 暗电流
- 设计说明

**💡 优化建议**
- AI 提供的改进建议
- 性能提升方向
- 工艺优化要点

### 高级功能

#### 备选材料对比
每一层都提供备选材料，帮助您做出最优选择：
- **材料名称**: 备选材料的具体名称
- **禁带宽度**: 该材料的禁带宽度值
- **优点**: 使用该材料的优势
- **缺点**: 使用该材料的劣势

点击"备选材料"可展开/折叠详细信息。

#### 导出和分享
- 结果页面可通过浏览器打印功能导出为 PDF
- 可视化图表支持右键保存

---

## ⚙️ 工作原理

### 系统架构

```
用户输入 → Prompt 构建 → DeepSeek API → JSON 解析 → 可视化生成 → 结果展示
    ↓           ↓              ↓            ↓            ↓            ↓
  参数验证   模板渲染      流式推理     数据提取    Matplotlib    多选项卡UI
```

### 详细流程

#### 1. Prompt 工程
系统将用户输入转换为结构化的 Prompt：
- **参数封装**: 材料类型、禁带宽度、厚度、应用场景
- **约束条件**: 
  - 必须包含完整的功能层（电极、传输层、吸收层）
  - 禁止包含衬底层
  - 光吸收层必须是复合结构
- **输出格式**: 强制要求 JSON 格式，包含：
  - `layers`: 层结构数组（含备选材料）
  - `performance`: 性能参数
  - `optimization_suggestions`: 优化建议
  - `explanation`: 设计说明

#### 2. AI 推理
- **模型选择**: 根据用户选择调用 Reasoner 或 Chat 模型
- **知识运用**: AI 基于以下知识进行推理
  - 半导体物理（能带理论、载流子传输）
  - 材料特性（禁带宽度、迁移率、稳定性）
  - 器件工程（界面匹配、光学设计）
  - 制备工艺（薄膜沉积、退火处理）

#### 3. 流式处理
- **实时反馈**: 通过 Server-Sent Events 将推理过程传输到前端
- **进度追踪**: 
  - 步骤 1-2: 参数接收和 Prompt 构建
  - 步骤 3: RAG 知识库检索（可选）
  - 步骤 4: AI 推理（显示推理内容）
  - 步骤 5: JSON 解析
  - 步骤 6: 可视化生成
  - 步骤 7: 完成

#### 4. 数据处理
- **JSON 提取**: 从 AI 响应中提取有效的 JSON 数据
- **数据验证**: 检查必需字段、数据类型
- **视觉属性计算**: 为 3D 模型计算层的位置、高度、颜色

#### 5. 可视化生成
- **结构图**: 使用 Matplotlib 绘制层叠示意图
- **性能曲线**: 使用 Plotly 生成交互式光谱响应图
- **3D 模型**: 前端 CSS3 渲染三维层叠结构

#### 6. 结果缓存
- **内存缓存**: 设计结果存储在服务器内存（24 小时）
- **自动清理**: 后台线程定期清理过期数据和图片文件
- **Session 管理**: 使用 Flask Session 追踪用户设计任务

---

## 🎨 设计示例

### 示例 1: 硅基红外探测器
**输入参数**:
- 材料: 硅量子点
- 禁带宽度: 0.5 - 1.2 eV
- 厚度: 50 - 300 nm
- 应用: 红外探测器

**输出结果**:
- 5 层结构（ITO/ZnO/Si-QDs/MoO₃/Au）
- 响应波长: 800 - 1600 nm
- 量子效率: ~75%
- 备选材料: TiO₂、SnO₂（ETL）；NiO、PEDOT:PSS（HTL）

### 示例 2: 钙钛矿太阳能电池
**输入参数**:
- 材料: CH₃NH₃PbI₃ 量子点
- 禁带宽度: 1.5 - 1.6 eV
- 厚度: 100 - 500 nm
- 应用: 太阳能电池

**输出结果**:
- 多层异质结结构
- 光谱响应: 400 - 800 nm
- 预期效率: >20%
- 优化建议: 界面钝化、封装保护

---

## 🔧 开发指南

### 添加新材料
编辑 `templates/index.html` 中的材料数据库：

```javascript
const materials = {
    "量子点": {
        "IV族量子点": ["硅量子点", "锗量子点", "您的新材料"],
        // ...
    }
};
```

### 自定义 Prompt
修改 `app.py` 中的 Prompt 模板：

```python
prompt = f"""请设计一个叠层光电探测器，参数如下：
材料类型: {material_type}
# 添加您的自定义要求
"""
```

### 扩展可视化
在 `visualize.py` 中添加新的绘图函数：

```python
def generate_custom_plot(design_data):
    # 您的可视化逻辑
    pass
```

---

## ❓ 常见问题

### Q1: API 调用失败怎么办？
**A**: 检查以下几点：
- `.env` 文件中的 API Key 是否正确
- DeepSeek 账户是否有足够余额
- 网络连接是否正常
- 查看控制台错误日志

### Q2: 设计结果不理想？
**A**: 尝试以下方法：
- 使用"深度思考模式"获得更精确的设计
- 在"额外要求"中添加更具体的需求
- 调整禁带宽度和厚度范围
- 多次生成并对比结果

### Q3: 如何保存设计结果？
**A**: 
- 使用浏览器的打印功能导出为 PDF
- 右键保存可视化图表
- 复制文本内容到文档

### Q4: 支持批量设计吗？
**A**: 当前版本不支持批量设计，但您可以：
- 多次运行单次设计
- 修改代码添加批处理功能

### Q5: 可以离线使用吗？
**A**: 不可以，系统需要调用 DeepSeek API。但您可以：
- 保存设计结果供离线查看
- 考虑部署本地大模型（需要修改代码）

---

## 📊 性能优化

- **缓存机制**: 设计结果缓存 24 小时，避免重复计算
- **异步处理**: 使用流式响应，提升用户体验
- **资源清理**: 自动清理过期图片和缓存数据
- **CDN 加速**: 静态资源使用 CDN 加载

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **DeepSeek AI**: 提供强大的推理能力
- **Flask**: 优雅的 Web 框架
- **Bootstrap**: 美观的 UI 组件
- **开源社区**: 各种优秀的 Python 库

---

## 📧 联系方式

- **问题反馈**: 请在 GitHub Issues 中提交
- **功能建议**: 欢迎在 Discussions 中讨论

---

## ⚠️ 注意事项

- 请确保 `.env` 文件中的 API Key 有效且有足够的额度
- 生成的图像文件存储在 `static/images` 目录下，系统会自动定期清理
- 设计结果仅供参考，实际器件性能需要实验验证
- 请勿将 API Key 提交到公开仓库

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个 Star！⭐**

Powered by **Flask** & **DeepSeek AI**

*让 AI 加速光电器件研发*

</div>
