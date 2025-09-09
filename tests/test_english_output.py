#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
英文输出功能测试脚本
English Output Functionality Test Script
"""

from zhongxuan_scorer import score_layout


def test_english_output():
    """测试英文输出功能"""
    print("🇺🇸 English Output Functionality Test")
    print("=" * 60)

    # 测试数据
    test_data = {
        "house_facing": "S",
        "rooms": [
            {"norm_label": "entry", "palace9": "S", "center_xy": [0.5, 0.1]},
            {"norm_label": "master_bedroom", "palace9": "N", "center_xy": [0.5, 0.9]},
            {"norm_label": "kitchen", "palace9": "E", "center_xy": [0.8, 0.5]},
            {"norm_label": "bath", "palace9": "W", "center_xy": [0.2, 0.5]},
            {"norm_label": "bedroom", "palace9": "NE", "center_xy": [0.7, 0.3]},
        ],
    }

    print("📋 Test House Information:")
    print(f"   Orientation: {test_data['house_facing']}")
    print("   Room Distribution:")
    for room in test_data["rooms"]:
        print(f"     - {room['norm_label']}: {room['palace9']}")

    print("\n" + "=" * 60)

    # 北半球英文分析
    print("🌍 Northern Hemisphere English Analysis:")
    northern_en_result = score_layout(test_data, "northern", "en")
    print(f"   Total Score: {northern_en_result['total']} points")
    print(f"   Grade: {northern_en_result['grade']}")
    print(f"   House Gua: {northern_en_result['house_gua']}")

    print("\n   Detailed Scores:")
    for key, value in northern_en_result["breakdown"].items():
        print(f"     {key}: {value['score']} points - {value['why']}")

    print("\n   Optimization Advice:")
    for i, advice in enumerate(northern_en_result["advice"], 1):
        print(f"     {i}. {advice}")

    print("\n" + "=" * 60)

    # 南半球英文分析
    print("🌏 Southern Hemisphere English Analysis:")
    southern_en_result = score_layout(test_data, "southern", "en")
    print(f"   Total Score: {southern_en_result['total']} points")
    print(f"   Grade: {southern_en_result['grade']}")
    print(f"   House Gua: {southern_en_result['house_gua']}")

    print("\n   Detailed Scores:")
    for key, value in southern_en_result["breakdown"].items():
        print(f"     {key}: {value['score']} points - {value['why']}")

    print("\n   Optimization Advice:")
    for i, advice in enumerate(southern_en_result["advice"], 1):
        print(f"     {i}. {advice}")

    print("\n" + "=" * 60)

    # 对比分析
    print("🔄 Comparison Analysis:")
    print(
        f"   Northern Hemisphere: {northern_en_result['total']} points ({northern_en_result['grade']})"
    )
    print(
        f"   Southern Hemisphere: {southern_en_result['total']} points ({southern_en_result['grade']})"
    )

    score_diff = southern_en_result["total"] - northern_en_result["total"]
    if score_diff > 0:
        print(f"   📈 Southern Hemisphere scores {score_diff} points higher")
    elif score_diff < 0:
        print(f"   📉 Northern Hemisphere scores {abs(score_diff)} points higher")
    else:
        print(f"   ⚖️ Same score")

    print("\n✅ English output functionality test completed!")
    print("✅ 英文输出功能测试完成！")


def test_language_comparison():
    """测试中英文对比"""
    print("\n🔄 Chinese vs English Output Comparison")
    print("=" * 60)

    test_data = {
        "house_facing": "N",
        "rooms": [
            {"norm_label": "entry", "palace9": "N", "center_xy": [0.5, 0.1]},
            {"norm_label": "master_bedroom", "palace9": "S", "center_xy": [0.5, 0.9]},
        ],
    }

    # 中文输出
    zh_result = score_layout(test_data, "northern", "zh")
    print("🇨🇳 Chinese Output:")
    print(f"   House Gua: {zh_result['house_gua']}")
    print(f"   Main Door: {zh_result['breakdown']['main_door']['why']}")
    print(f"   Master Bed: {zh_result['breakdown']['master_bed']['why']}")

    # 英文输出
    en_result = score_layout(test_data, "northern", "en")
    print("\n🇺🇸 English Output:")
    print(f"   House Gua: {en_result['house_gua']}")
    print(f"   Main Door: {en_result['breakdown']['main_door']['why']}")
    print(f"   Master Bed: {en_result['breakdown']['master_bed']['why']}")

    print("\n✅ Language comparison test completed!")


if __name__ == "__main__":
    test_english_output()
    test_language_comparison()
