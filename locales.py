#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多语言配置文件
Multi-language configuration file
"""

# 中文文本
ZH_TEXTS = {
    # 页面标题和描述
    "page_title": "房屋布局评分系统",
    "page_description": "基于中国传统风水学（八宅理论）的智能房屋布局评分系统",
    
    # 侧边栏
    "sidebar_title": "⚙️ 设置参数",
    "north_degree_label": "真北角度 (°)",
    "north_degree_help": "真北相对于图像上方的角度（顺时针度数）",
    "house_facing_label": "房屋朝向",
    "auto_infer": "自动推断",
    "usage_instructions": "📖 使用说明",
    "usage_steps": [
        "上传清晰的房屋平面图",
        "调整真北角度（如需要）",
        "选择房屋朝向或让系统自动推断",
        "点击\"开始分析\"获取评分结果"
    ],
    "supported_rooms": "🏠 支持的房间类型",
    "room_types": {
        "entry": "入口",
        "bedroom": "卧室", 
        "kitchen": "厨房",
        "bathroom": "卫浴",
        "storage": "储物"
    },
    "room_examples": {
        "entry": "entry, porch, foyer",
        "bedroom": "master_bedroom, bedroom",
        "kitchen": "kitchen, pantry",
        "bathroom": "bath, wc, ensuite, laundry",
        "storage": "garage, store, wir, robe"
    },
    
    # 主界面
    "upload_section": "📁 上传平面图",
    "upload_label": "选择平面图文件",
    "upload_help": "支持 PNG, JPG, JPEG 格式",
    "uploaded_image_caption": "上传的平面图",
    "analyze_button": "🔍 开始分析",
    "analyzing_text": "正在分析平面图...",
    "analysis_success": "分析完成！",
    "analysis_error": "分析失败",
    
    # 结果展示
    "results_section": "📊 分析结果",
    "no_analysis_yet": "请先上传平面图并开始分析",
    "score_preview": "🎯 评分标准预览",
    "grade_levels": {
        "S": "S级: 90-100分 (优秀)",
        "A": "A级: 80-89分 (良好)",
        "B": "B级: 70-79分 (中等)",
        "C": "C级: 60-69分 (一般)",
        "D": "D级: 0-59分 (较差)"
    },
    
    # 评分卡片
    "total_score": "综合评分",
    "grade": "等级",
    "points": "分",
    "level": "级",
    
    # 详细评分
    "detailed_scores": "📋 详细评分",
    "score_items": {
        "main_door": "大门位置",
        "master_bed": "主卧位置",
        "kitchen": "厨房位置",
        "bath_laundry": "卫浴/洗衣房",
        "other_bed": "其他卧室",
        "garage_store": "车库/储物间",
        "center_c": "中宫占用",
        "throughline": "穿堂直冲"
    },
    "score": "得分",
    "explanation": "说明",
    
    # 检测房间
    "detected_rooms": "🏠 检测到的房间",
    "no_rooms_detected": "未检测到任何房间",
    "original_text": "原始",
    "position": "位置",
    "direction": "方向",
    "confidence": "置信度",
    
    # 优化建议
    "optimization_advice": "💡 优化建议",
    "no_advice": "暂无特殊建议",
    "advice_prefix": "建议"
}

# 英文文本
EN_TEXTS = {
    # Page title and description
    "page_title": "House Layout Scoring System",
    "page_description": "An intelligent house layout scoring system based on traditional Chinese Feng Shui (Eight Mansions theory)",
    
    # Sidebar
    "sidebar_title": "⚙️ Settings",
    "north_degree_label": "True North Angle (°)",
    "north_degree_help": "True north angle relative to image top (clockwise degrees)",
    "house_facing_label": "House Orientation",
    "auto_infer": "Auto Infer",
    "usage_instructions": "📖 Usage Instructions",
    "usage_steps": [
        "Upload a clear floor plan image",
        "Adjust true north angle (if needed)",
        "Select house orientation or let system auto-infer",
        "Click 'Start Analysis' to get scoring results"
    ],
    "supported_rooms": "🏠 Supported Room Types",
    "room_types": {
        "entry": "Entry",
        "bedroom": "Bedroom",
        "kitchen": "Kitchen", 
        "bathroom": "Bathroom",
        "storage": "Storage"
    },
    "room_examples": {
        "entry": "entry, porch, foyer",
        "bedroom": "master_bedroom, bedroom",
        "kitchen": "kitchen, pantry",
        "bathroom": "bath, wc, ensuite, laundry",
        "storage": "garage, store, wir, robe"
    },
    
    # Main interface
    "upload_section": "📁 Upload Floor Plan",
    "upload_label": "Select Floor Plan File",
    "upload_help": "Supports PNG, JPG, JPEG formats",
    "uploaded_image_caption": "Uploaded Floor Plan",
    "analyze_button": "🔍 Start Analysis",
    "analyzing_text": "Analyzing floor plan...",
    "analysis_success": "Analysis completed!",
    "analysis_error": "Analysis failed",
    
    # Results display
    "results_section": "📊 Analysis Results",
    "no_analysis_yet": "Please upload a floor plan and start analysis first",
    "score_preview": "🎯 Scoring Criteria Preview",
    "grade_levels": {
        "S": "S Grade: 90-100 points (Excellent)",
        "A": "A Grade: 80-89 points (Good)",
        "B": "B Grade: 70-79 points (Average)",
        "C": "C Grade: 60-69 points (Fair)",
        "D": "D Grade: 0-59 points (Poor)"
    },
    
    # Score card
    "total_score": "Total Score",
    "grade": "Grade",
    "points": "points",
    "level": "Grade",
    
    # Detailed scores
    "detailed_scores": "📋 Detailed Scores",
    "score_items": {
        "main_door": "Main Door Position",
        "master_bed": "Master Bedroom Position",
        "kitchen": "Kitchen Position",
        "bath_laundry": "Bathroom/Laundry",
        "other_bed": "Other Bedrooms",
        "garage_store": "Garage/Storage",
        "center_c": "Center Palace Usage",
        "throughline": "Direct Line Through"
    },
    "score": "Score",
    "explanation": "Explanation",
    
    # Detected rooms
    "detected_rooms": "🏠 Detected Rooms",
    "no_rooms_detected": "No rooms detected",
    "original_text": "Original",
    "position": "Position",
    "direction": "Direction",
    "confidence": "Confidence",
    
    # Optimization advice
    "optimization_advice": "💡 Optimization Advice",
    "no_advice": "No special advice available",
    "advice_prefix": "Advice"
}

# 语言映射
LANGUAGES = {
    "中文": "zh",
    "English": "en"
}

def get_texts(language="zh"):
    """获取指定语言的文本"""
    if language == "en":
        return EN_TEXTS
    else:
        return ZH_TEXTS

def get_language_options():
    """获取语言选项列表"""
    return list(LANGUAGES.keys())
