#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整英文输出测试脚本
Complete English Output Test Script
"""

from zhongxuan_scorer import score_layout

def test_complete_english_output():
    """测试完整的英文输出，确保没有中文字符"""
    print("🇺🇸 Complete English Output Test")
    print("=" * 60)
    
    # 测试数据 - 包含各种房间类型
    test_data = {
        "house_facing": "S",
        "rooms": [
            {"norm_label": "entry", "palace9": "S", "center_xy": [0.5, 0.1]},
            {"norm_label": "master_bedroom", "palace9": "N", "center_xy": [0.5, 0.9]},
            {"norm_label": "kitchen", "palace9": "C", "center_xy": [0.5, 0.5]},  # 中宫
            {"norm_label": "bath", "palace9": "W", "center_xy": [0.2, 0.5]},
            {"norm_label": "ensuite", "palace9": "E", "center_xy": [0.8, 0.3]},
            {"norm_label": "bedroom", "palace9": "NE", "center_xy": [0.7, 0.3]},
            {"norm_label": "bedroom_2", "palace9": "SW", "center_xy": [0.3, 0.7]},
            {"norm_label": "garage", "palace9": "NW", "center_xy": [0.2, 0.2]},
            {"norm_label": "alfresco", "palace9": "S", "center_xy": [0.5, 0.05]},
        ],
    }
    
    print("📋 Test House Information:")
    print(f"   Orientation: {test_data['house_facing']}")
    print("   Room Distribution:")
    for room in test_data["rooms"]:
        print(f"     - {room['norm_label']}: {room['palace9']}")
    
    print("\n" + "=" * 60)
    
    # 南半球英文分析
    print("🌏 Southern Hemisphere English Analysis:")
    result = score_layout(test_data, "southern", "en")
    
    print(f"   Total Score: {result['total']} points")
    print(f"   Grade: {result['grade']}")
    print(f"   House Gua: {result['house_gua']}")
    
    print("\n   Detailed Scores:")
    for key, value in result["breakdown"].items():
        print(f"     {key}: {value['score']} points - {value['why']}")
    
    print("\n   Optimization Advice:")
    for i, advice in enumerate(result["advice"], 1):
        print(f"     {i}. {advice}")
    
    print("\n" + "=" * 60)
    
    # 检查是否还有中文字符
    print("🔍 Checking for Chinese characters in English output:")
    chinese_found = False
    
    # 检查宅卦标签
    if any('\u4e00' <= char <= '\u9fff' for char in result['house_gua']):
        print(f"   ❌ House Gua contains Chinese: {result['house_gua']}")
        chinese_found = True
    else:
        print(f"   ✅ House Gua is fully English: {result['house_gua']}")
    
    # 检查评分说明
    for key, value in result["breakdown"].items():
        if any('\u4e00' <= char <= '\u9fff' for char in value['why']):
            print(f"   ❌ {key} explanation contains Chinese: {value['why']}")
            chinese_found = True
        else:
            print(f"   ✅ {key} explanation is fully English: {value['why']}")
    
    # 检查建议
    for i, advice in enumerate(result["advice"], 1):
        if any('\u4e00' <= char <= '\u9fff' for char in advice):
            print(f"   ❌ Advice {i} contains Chinese: {advice}")
            chinese_found = True
        else:
            print(f"   ✅ Advice {i} is fully English: {advice}")
    
    if chinese_found:
        print("\n❌ Chinese characters found in English output!")
    else:
        print("\n✅ All English output is completely in English!")
    
    print("\n✅ Complete English output test completed!")

def test_edge_cases():
    """测试边缘情况"""
    print("\n🧪 Testing Edge Cases")
    print("=" * 60)
    
    # 测试没有检测到房间的情况
    test_data_minimal = {
        "house_facing": "N",
        "rooms": []
    }
    
    print("Testing minimal data (no rooms detected):")
    result = score_layout(test_data_minimal, "northern", "en")
    
    print(f"   House Gua: {result['house_gua']}")
    print("   Breakdown explanations:")
    for key, value in result["breakdown"].items():
        print(f"     {key}: {value['why']}")
    
    # 检查是否有中文字符
    chinese_found = False
    for key, value in result["breakdown"].items():
        if any('\u4e00' <= char <= '\u9fff' for char in value['why']):
            print(f"   ❌ {key} contains Chinese: {value['why']}")
            chinese_found = True
    
    if not chinese_found:
        print("   ✅ All explanations are in English even with minimal data")

if __name__ == "__main__":
    test_complete_english_output()
    test_edge_cases()
