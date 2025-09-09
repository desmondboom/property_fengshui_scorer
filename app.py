#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import json
import tempfile
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Import our modules
from fp2layout import detect_layout
from zhongxuan_scorer import score_layout

# Page configuration
st.set_page_config(
    page_title="房屋布局评分系统",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .grade-s {
        color: #ffd700;
        font-size: 3rem;
        font-weight: bold;
    }
    .grade-a {
        color: #c0c0c0;
        font-size: 3rem;
        font-weight: bold;
    }
    .grade-b {
        color: #cd7f32;
        font-size: 3rem;
        font-weight: bold;
    }
    .grade-c {
        color: #8b4513;
        font-size: 3rem;
        font-weight: bold;
    }
    .grade-d {
        color: #696969;
        font-size: 3rem;
        font-weight: bold;
    }
    .room-item {
        background: #f0f2f6;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
    }
    .advice-box {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 房屋布局评分系统</h1>', unsafe_allow_html=True)
    st.markdown("基于中国传统风水学（八宅理论）的智能房屋布局评分系统")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ 设置参数")
        
        # North degree setting
        north_deg = st.slider(
            "真北角度 (°)",
            min_value=0.0,
            max_value=360.0,
            value=0.0,
            step=1.0,
            help="真北相对于图像上方的角度（顺时针度数）"
        )
        
        # House facing setting
        facing_options = ["自动推断", "N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        facing_choice = st.selectbox("房屋朝向", facing_options)
        house_facing = None if facing_choice == "自动推断" else facing_choice
        
        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 上传清晰的房屋平面图
        2. 调整真北角度（如需要）
        3. 选择房屋朝向或让系统自动推断
        4. 点击"开始分析"获取评分结果
        """)
        
        st.markdown("### 🏠 支持的房间类型")
        st.markdown("""
        - **入口**: entry, porch, foyer
        - **卧室**: master_bedroom, bedroom
        - **厨房**: kitchen, pantry
        - **卫浴**: bath, wc, ensuite, laundry
        - **储物**: garage, store, wir, robe
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 上传平面图")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "选择平面图文件",
            type=['png', 'jpg', 'jpeg'],
            help="支持 PNG, JPG, JPEG 格式"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="上传的平面图", use_column_width=True)
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                image.save(tmp_file.name)
                temp_path = tmp_file.name
            
            # Analysis button
            if st.button("🔍 开始分析", type="primary", use_container_width=True):
                with st.spinner("正在分析平面图..."):
                    try:
                        # Step 1: Detect layout
                        layout_data = detect_layout(temp_path, north_deg, house_facing)
                        
                        # Step 2: Score layout
                        score_data = score_layout(layout_data)
                        
                        # Store results in session state
                        st.session_state.layout_data = layout_data
                        st.session_state.score_data = score_data
                        st.session_state.analysis_done = True
                        
                        st.success("分析完成！")
                        
                    except Exception as e:
                        st.error(f"分析失败: {str(e)}")
                    finally:
                        # Clean up temp file
                        os.unlink(temp_path)
    
    with col2:
        st.header("📊 分析结果")
        
        if st.session_state.get('analysis_done', False):
            score_data = st.session_state.score_data
            layout_data = st.session_state.layout_data
            
            # Display score and grade
            display_score_card(score_data)
            
            # Display breakdown
            display_breakdown(score_data)
            
            # Display detected rooms
            display_detected_rooms(layout_data)
            
            # Display advice
            display_advice(score_data)
            
        else:
            st.info("请先上传平面图并开始分析")
            st.markdown("### 🎯 评分标准预览")
            st.markdown("""
            - **S级**: 90-100分 (优秀)
            - **A级**: 80-89分 (良好)  
            - **B级**: 70-79分 (中等)
            - **C级**: 60-69分 (一般)
            - **D级**: 0-59分 (较差)
            """)

def display_score_card(score_data):
    """Display the main score card"""
    total = score_data['total']
    grade = score_data['grade']
    house_gua = score_data['house_gua']
    
    # Grade color mapping
    grade_colors = {
        'S': 'grade-s',
        'A': 'grade-a', 
        'B': 'grade-b',
        'C': 'grade-c',
        'D': 'grade-d'
    }
    
    st.markdown(f"""
    <div class="score-card">
        <h2>综合评分</h2>
        <div class="{grade_colors.get(grade, 'grade-d')}">{total}分</div>
        <h3>等级: {grade}级</h3>
        <p>{house_gua}</p>
    </div>
    """, unsafe_allow_html=True)

def display_breakdown(score_data):
    """Display detailed breakdown"""
    st.subheader("📋 详细评分")
    
    breakdown = score_data['breakdown']
    
    # Create a DataFrame for better display
    import pandas as pd
    
    breakdown_data = []
    for key, value in breakdown.items():
        breakdown_data.append({
            '项目': get_chinese_name(key),
            '得分': value['score'],
            '说明': value['why']
        })
    
    df = pd.DataFrame(breakdown_data)
    
    # Color code the scores
    def color_score(val):
        if val > 0:
            return 'background-color: #d4edda; color: #155724'
        elif val < 0:
            return 'background-color: #f8d7da; color: #721c24'
        else:
            return 'background-color: #f8f9fa; color: #6c757d'
    
    styled_df = df.style.applymap(color_score, subset=['得分'])
    st.dataframe(styled_df, use_container_width=True)

def display_detected_rooms(layout_data):
    """Display detected rooms"""
    st.subheader("🏠 检测到的房间")
    
    rooms = layout_data.get('rooms', [])
    
    if rooms:
        for room in rooms:
            st.markdown(f"""
            <div class="room-item">
                <strong>{room['norm_label']}</strong> 
                (原始: {room['raw_text']})<br>
                位置: {room['palace9']} | 方向: {room['direction8']} | 置信度: {room['conf']:.1f}%
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("未检测到任何房间")

def display_advice(score_data):
    """Display advice"""
    st.subheader("💡 优化建议")
    
    advice_list = score_data.get('advice', [])
    
    if advice_list:
        for i, advice in enumerate(advice_list, 1):
            st.markdown(f"""
            <div class="advice-box">
                <strong>建议 {i}:</strong> {advice}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无特殊建议")

def get_chinese_name(key):
    """Get Chinese name for breakdown items"""
    name_mapping = {
        'main_door': '大门位置',
        'master_bed': '主卧位置', 
        'kitchen': '厨房位置',
        'bath_laundry': '卫浴/洗衣房',
        'other_bed': '其他卧室',
        'garage_store': '车库/储物间',
        'center_c': '中宫占用',
        'throughline': '穿堂直冲'
    }
    return name_mapping.get(key, key)

if __name__ == "__main__":
    main()
