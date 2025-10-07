#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify Quiz Chat 启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import jinja2
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  未找到.env文件")
        print("请复制env.example为.env并配置Dify API密钥")
        return False
    
    # 检查必要的环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DIFY_API_KEY")
    if not api_key or api_key == "your_dify_api_key_here":
        print("❌ 请配置DIFY_API_KEY环境变量")
        return False
    
    global app_port, app_host
    app_port = os.getenv("APP_PORT")
    if not app_port :
        app_port == "8000"

    app_host = os.getenv("APP_HOST")
    if not app_host :
        app_host == "0.0.0.0"


    print("✅ 环境变量配置正确")
    return True

def create_directories():
    """创建必要的目录"""
    directories = ["static", "templates", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ 目录结构检查完成")

def start_app():
    """启动应用"""
    print("🚀 启动Dify Quiz Chat应用...")
    
    try:
        # 使用uvicorn启动应用
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", app_host, 
            "--port", app_port, 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("🎯 Dify Quiz Chat 启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 检查环境变量
    if not check_env_file():
        print("\n💡 配置说明：")
        print("1. 复制 env.example 为 .env")
        print("2. 在Dify平台创建应用并获取API Key")
        print("3. 在.env文件中配置DIFY_API_KEY")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 启动应用
    start_app()

if __name__ == "__main__":
    main()
