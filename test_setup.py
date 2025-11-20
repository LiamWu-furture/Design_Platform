"""
项目环境测试脚本
检查所有依赖和配置是否正确
"""

import sys
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  建议使用Python 3.8或更高版本")
        return False
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = {
        'flask': 'Flask',
        'requests': 'requests',
        'matplotlib': 'matplotlib',
        'dotenv': 'python-dotenv',
        'numpy': 'numpy'
    }
    
    all_installed = True
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            all_installed = False
    
    return all_installed

def check_env_file():
    """检查.env文件"""
    if not os.path.exists('.env'):
        print("✗ .env文件不存在")
        return False
    
    print("✓ .env文件存在")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    secret_key = os.getenv('FLASK_SECRET_KEY')
    
    if not api_key:
        print("  ⚠️  DEEPSEEK_API_KEY未配置")
        return False
    else:
        print(f"  ✓ DEEPSEEK_API_KEY已配置 (长度: {len(api_key)})")
    
    if not secret_key:
        print("  ⚠️  FLASK_SECRET_KEY未配置")
    else:
        print(f"  ✓ FLASK_SECRET_KEY已配置")
    
    return True

def check_directories():
    """检查目录结构"""
    required_dirs = [
        'templates',
        'static',
        'static/images'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/ 目录存在")
        else:
            print(f"✗ {dir_path}/ 目录不存在")
            all_exist = False
    
    return all_exist

def check_files():
    """检查必需文件"""
    required_files = [
        'app.py',
        'deepseek_api.py',
        'visualize.py',
        'requirements.txt',
        'templates/index.html',
        'templates/result.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 50)
    print("叠层光电探测器设计系统 - 环境检查")
    print("=" * 50)
    print()
    
    print("[1/5] 检查Python版本...")
    python_ok = check_python_version()
    print()
    
    print("[2/5] 检查依赖包...")
    deps_ok = check_dependencies()
    print()
    
    print("[3/5] 检查环境变量...")
    env_ok = check_env_file()
    print()
    
    print("[4/5] 检查目录结构...")
    dirs_ok = check_directories()
    print()
    
    print("[5/5] 检查必需文件...")
    files_ok = check_files()
    print()
    
    print("=" * 50)
    if all([python_ok, deps_ok, env_ok, dirs_ok, files_ok]):
        print("✅ 所有检查通过！项目可以运行。")
        print()
        print("启动命令:")
        print("  python app.py")
        print()
        print("或使用快速启动脚本:")
        print("  run.bat")
    else:
        print("❌ 部分检查未通过，请修复上述问题。")
        print()
        if not deps_ok:
            print("安装依赖:")
            print("  pip install -r requirements.txt")
    print("=" * 50)

if __name__ == '__main__':
    main()
