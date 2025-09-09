#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多语言功能测试脚本
Multi-language functionality test script
"""

from locales import get_texts, get_language_options


def test_language_switching():
    """测试语言切换功能"""
    print("🌐 测试多语言功能")
    print("=" * 50)

    # 测试语言选项
    print("📋 可用语言选项:")
    for lang in get_language_options():
        print(f"   - {lang}")

    print("\n" + "=" * 50)

    # 测试中文文本
    print("🇨🇳 中文界面测试:")
    zh_texts = get_texts("zh")
    print(f"   页面标题: {zh_texts['page_title']}")
    print(f"   页面描述: {zh_texts['page_description']}")
    print(f"   上传标签: {zh_texts['upload_label']}")
    print(f"   分析按钮: {zh_texts['analyze_button']}")
    print(f"   评分项目: {zh_texts['score_items']['main_door']}")

    print("\n" + "=" * 50)

    # 测试英文文本
    print("🇺🇸 English Interface Test:")
    en_texts = get_texts("en")
    print(f"   Page Title: {en_texts['page_title']}")
    print(f"   Page Description: {en_texts['page_description']}")
    print(f"   Upload Label: {en_texts['upload_label']}")
    print(f"   Analyze Button: {en_texts['analyze_button']}")
    print(f"   Score Items: {en_texts['score_items']['main_door']}")

    print("\n" + "=" * 50)

    # 测试评分等级
    print("📊 评分等级测试:")
    print("中文:")
    for grade, desc in zh_texts["grade_levels"].items():
        print(f"   {grade}: {desc}")

    print("\nEnglish:")
    for grade, desc in en_texts["grade_levels"].items():
        print(f"   {grade}: {desc}")

    print("\n✅ 多语言功能测试完成！")
    print("✅ Multi-language functionality test completed!")


if __name__ == "__main__":
    test_language_switching()
