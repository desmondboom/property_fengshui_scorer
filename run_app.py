#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动脚本 - 房屋布局评分系统 Web 应用
Launch script for House Layout Scoring System Web App
"""

import subprocess
import sys
import os

def main():
    """启动 Streamlit Web 应用"""
    print("🏠 启动房屋布局评分系统 Web 应用...")
    print("🏠 Starting House Layout Scoring System Web App...")
    
    # 检查是否在正确的环境中
    try:
        import streamlit
        import cv2
        import pytesseract
        print("✅ 依赖检查通过")
        print("✅ Dependencies check passed")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print(f"❌ Missing dependency: {e}")
        print("请先运行: conda activate listing-score-env")
        print("Please run: conda activate listing-score-env")
        sys.exit(1)
    
    # 启动 Streamlit 应用
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        print("👋 App stopped")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print(f"❌ Failed to start: {e}")

if __name__ == "__main__":
    main()
