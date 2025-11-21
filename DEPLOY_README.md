# 宝塔面板部署指南

本项目是一个基于Flask的Web应用，支持通过宝塔面板的"Python项目管理器"进行部署。

## 1. 准备工作

1. **上传文件**：
   将项目所有文件上传到服务器目录，例如 `/www/wwwroot/DetectorDesign`。
   确保包含以下关键文件：
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `static/`
   - `templates/`
   - `.env` (如果没有，请参考下文创建)

2. **配置环境变量**：
   在项目根目录下创建 `.env` 文件（如果未上传），并填入必要的配置：
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   FLASK_SECRET_KEY=your_random_secret_key
   ```

## 2. 宝塔Python项目管理器设置

1. 登录宝塔面板，进入 **软件商店**，搜索并安装 **Python项目管理器**。
2. 打开Python项目管理器，点击 **添加项目**。
3. 填写项目配置：
   - **项目名称**：DetectorDesign (或其他自定义名称)
   - **路径**：选择上传的项目目录 `/www/wwwroot/DetectorDesign`
   - **Python版本**：选择 Python 3.8+ (建议 3.10 或 3.11)
   - **框架**：Flask
   - **启动方式**：Gunicorn
   - **启动文件**：`wsgi.py`
   - **应用变量**：`app`
   - **端口**：输入想要运行的端口，例如 `5000` (确保在安全组开放此端口)
   - **勾选**：安装依赖 (会自动读取 requirements.txt)

4. 点击 **确定** 开始部署。

## 3. 验证部署

1. 等待项目状态变为"运行中"。
2. 点击 **映射** 按钮，将项目映射到一个域名 (如果没有域名，可以直接用 IP:端口 访问)。
3. 访问 `http://你的IP:5000` 或映射的域名，检查应用是否正常运行。

## 4. 常见问题排查

- **依赖安装失败**：
  检查日志，如果提示缺少系统库，可能需要在终端手动安装，例如 `yum install mesa-libGL` (Matplotlib有时需要)。
  
- **启动失败**：
  查看项目日志。如果是 `ModuleNotFoundError`，尝试在项目管理器中点击"模块"手动添加缺失的包。

- **静态资源无法加载**：
  Flask自带静态文件服务，但建议在网站配置中(如果配置了Nginx映射)添加静态资源代理：
  ```nginx
  location /static {
      alias /www/wwwroot/DetectorDesign/static;
  }
  ```

## 5. 维护

- **清理缓存**：项目会自动清理24小时前的生成结果。
- **重启服务**：修改代码或配置后，需要在Python项目管理器中重启项目。
