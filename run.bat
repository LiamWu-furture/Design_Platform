@echo off
echo ========================================
echo 叠层光电探测器设计系统
echo ========================================
echo.

REM 检查虚拟环境
if exist .venv\Scripts\activate.bat (
    echo [1/3] 激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo [警告] 未找到虚拟环境，使用系统Python
)

REM 检查依赖
echo [2/3] 检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖包...
    pip install -r requirements.txt
) else (
    echo [OK] 依赖包已安装
)

REM 启动应用
echo [3/3] 启动Flask应用...
echo.
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
python app.py

pause
