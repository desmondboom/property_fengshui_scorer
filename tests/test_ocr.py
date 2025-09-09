#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 OCR 功能
Test OCR functionality
"""

import numpy as np
from fp2layout import ocr_lines, preprocess_image

def test_ocr_availability():
    """测试 OCR 引擎可用性"""
    print("Testing OCR engine availability...")
    
    # 创建一个简单的测试图像
    test_img = np.ones((100, 300, 3), dtype=np.uint8) * 255
    test_img = preprocess_image(test_img)
    
    try:
        results = ocr_lines(test_img)
        print(f"✅ OCR engine is working! Found {len(results)} text regions")
        return True
    except Exception as e:
        print(f"❌ OCR engine failed: {e}")
        return False

if __name__ == "__main__":
    test_ocr_availability()
