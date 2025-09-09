#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
南半球功能测试脚本
Southern Hemisphere functionality test script
"""

from zhongxuan_scorer import score_layout, house_group_and_gua


def test_hemisphere_differences():
    """测试南北半球风水理论差异"""
    print("🌍 南北半球风水理论差异测试")
    print("=" * 60)

    # 测试数据
    test_data = {
        "house_facing": "S",
        "rooms": [
            {"norm_label": "entry", "palace9": "S", "center_xy": [0.5, 0.1]},
            {"norm_label": "master_bedroom", "palace9": "N", "center_xy": [0.5, 0.9]},
            {"norm_label": "kitchen", "palace9": "E", "center_xy": [0.8, 0.5]},
            {"norm_label": "bath", "palace9": "W", "center_xy": [0.2, 0.5]},
        ],
    }

    print("📋 测试房屋信息:")
    print(f"   朝向: {test_data['house_facing']}")
    print("   房间分布:")
    for room in test_data["rooms"]:
        print(f"     - {room['norm_label']}: {room['palace9']}")

    print("\n" + "=" * 60)

    # 北半球分析
    print("🌍 北半球分析:")
    northern_result = score_layout(test_data, "northern")
    print(f"   总分: {northern_result['total']}分")
    print(f"   等级: {northern_result['grade']}级")
    print(f"   宅卦: {northern_result['house_gua']}")

    print("\n   详细评分:")
    for key, value in northern_result["breakdown"].items():
        print(f"     {key}: {value['score']}分 - {value['why']}")

    print("\n" + "=" * 60)

    # 南半球分析
    print("🌏 南半球分析:")
    southern_result = score_layout(test_data, "southern")
    print(f"   总分: {southern_result['total']}分")
    print(f"   等级: {southern_result['grade']}级")
    print(f"   宅卦: {southern_result['house_gua']}")

    print("\n   详细评分:")
    for key, value in southern_result["breakdown"].items():
        print(f"     {key}: {value['score']}分 - {value['why']}")

    print("\n" + "=" * 60)

    # 对比分析
    print("🔄 对比分析:")
    print(f"   北半球总分: {northern_result['total']}分 ({northern_result['grade']}级)")
    print(f"   南半球总分: {southern_result['total']}分 ({southern_result['grade']}级)")

    score_diff = southern_result["total"] - northern_result["total"]
    if score_diff > 0:
        print(f"   📈 南半球评分高 {score_diff} 分")
    elif score_diff < 0:
        print(f"   📉 北半球评分高 {abs(score_diff)} 分")
    else:
        print(f"   ⚖️ 评分相同")

    print("\n💡 南半球优化建议:")
    for i, advice in enumerate(southern_result["advice"], 1):
        print(f"   {i}. {advice}")

    print("\n✅ 南半球功能测试完成！")
    print("✅ Southern Hemisphere functionality test completed!")


def test_hemisphere_theory():
    """测试南北半球理论差异"""
    print("\n🧭 南北半球理论差异测试")
    print("=" * 60)

    # 测试不同朝向的吉凶方位
    facings = ["N", "S", "E", "W"]

    for facing in facings:
        print(f"\n朝向 {facing}:")

        # 北半球
        group_n, gua_n, good_n, bad_n = house_group_and_gua(facing, "northern")
        print(f"  北半球: {gua_n}宅 - 吉位: {sorted(good_n)}")

        # 南半球
        group_s, gua_s, good_s, bad_s = house_group_and_gua(facing, "southern")
        print(f"  南半球: {gua_s}宅 - 吉位: {sorted(good_s)}")

        # 差异
        diff = good_s - good_n
        if diff:
            print(f"  差异: 南半球额外吉位 {sorted(diff)}")
        else:
            print(f"  差异: 无差异")


if __name__ == "__main__":
    test_hemisphere_differences()
    test_hemisphere_theory()
