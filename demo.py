#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
演示脚本 - 测试房屋布局评分系统
Demo script for testing the House Layout Scoring System
"""

import json
import os

from fp2layout import detect_layout
from zhongxuan_scorer import score_layout


def demo_analysis():
    """演示分析流程"""
    print("🏠 房屋布局评分系统演示")
    print("=" * 50)

    # 检查测试图片是否存在
    test_image = "data/test.png"
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return

    print(f"📁 使用测试图片: {test_image}")

    try:
        # 步骤1: 平面图解析
        print("\n🔍 步骤1: 解析平面图...")
        layout_data = detect_layout(test_image, north_deg=0.0, house_facing="S")

        print(f"✅ 检测到 {len(layout_data['rooms'])} 个房间")
        for room in layout_data["rooms"]:
            print(
                f"   - {room['norm_label']} ({room['raw_text']}) 位置: {room['palace9']}"
            )

        # 步骤2: 北半球风水评分
        print("\n📊 步骤2: 北半球风水评分...")
        score_data_northern = score_layout(layout_data, "northern")

        print(f"\n🌍 北半球评分结果:")
        print(f"   总分: {score_data_northern['total']}分")
        print(f"   等级: {score_data_northern['grade']}级")
        print(f"   宅卦: {score_data_northern['house_gua']}")

        # 步骤3: 南半球风水评分
        print("\n📊 步骤3: 南半球风水评分...")
        score_data_southern = score_layout(layout_data, "southern")

        print(f"\n🌏 南半球评分结果:")
        print(f"   总分: {score_data_southern['total']}分")
        print(f"   等级: {score_data_southern['grade']}级")
        print(f"   宅卦: {score_data_southern['house_gua']}")

        # 对比分析
        print(f"\n🔄 南北半球对比:")
        print(f"   北半球总分: {score_data_northern['total']}分 ({score_data_northern['grade']}级)")
        print(f"   南半球总分: {score_data_southern['total']}分 ({score_data_southern['grade']}级)")

        # 显示南半球详细评分
        print(f"\n📋 南半球详细评分:")
        for key, value in score_data_southern["breakdown"].items():
            print(f"   {key}: {value['score']}分 - {value['why']}")

        print(f"\n💡 南半球优化建议:")
        for i, advice in enumerate(score_data_southern["advice"], 1):
            print(f"   {i}. {advice}")

        # 保存结果
        result = {
            "northern_hemisphere": score_data_northern,
            "southern_hemisphere": score_data_southern
        }
        with open("demo_result_hemisphere.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: demo_result_hemisphere.json")

    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    demo_analysis()
