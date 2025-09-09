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
from locales import get_texts, get_language_options

# Page configuration
st.set_page_config(
    page_title="房屋布局评分系统",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


def main():
    # Initialize session state for language and hemisphere
    if "language" not in st.session_state:
        st.session_state.language = "zh"
    if "hemisphere" not in st.session_state:
        st.session_state.hemisphere = "northern"

    # Get current language texts
    texts = get_texts(st.session_state.language)

    # Sidebar
    with st.sidebar:
        selected_lang = st.selectbox(
            "🌐 Language / 语言",
            options=get_language_options(),
            index=0 if st.session_state.language == "zh" else 1,
            key="language_selector",
        )

        # Update language if changed
        if selected_lang == "English":
            st.session_state.language = "en"
        else:
            st.session_state.language = "zh"

        # Refresh texts after language change
        texts = get_texts(st.session_state.language)

        st.header(texts["sidebar_title"])

        # North degree setting
        north_deg = st.slider(
            texts["north_degree_label"],
            min_value=0.0,
            max_value=360.0,
            value=0.0,
            step=1.0,
            help=texts["north_degree_help"],
        )

        # Hemisphere setting
        hemisphere_options = [
            texts["hemisphere_northern"],
            texts["hemisphere_southern"],
        ]
        hemisphere_choice = st.selectbox(
            texts["hemisphere_label"],
            hemisphere_options,
            index=0 if st.session_state.hemisphere == "northern" else 1,
            help=texts["hemisphere_help"],
        )

        # Update hemisphere in session state
        if hemisphere_choice == texts["hemisphere_southern"]:
            st.session_state.hemisphere = "southern"
        else:
            st.session_state.hemisphere = "northern"

        # House facing setting
        facing_options = [
            texts["auto_infer"],
            "N",
            "NE",
            "E",
            "SE",
            "S",
            "SW",
            "W",
            "NW",
        ]
        facing_choice = st.selectbox(texts["house_facing_label"], facing_options)
        house_facing = None if facing_choice == texts["auto_infer"] else facing_choice

        st.markdown("---")
        st.markdown(f"### {texts['usage_instructions']}")
        for i, step in enumerate(texts["usage_steps"], 1):
            st.markdown(f"{i}. {step}")

        st.markdown(f"### {texts['supported_rooms']}")
        for room_type, examples in texts["room_examples"].items():
            st.markdown(f"- **{texts['room_types'][room_type]}**: {examples}")

    # Header
    st.markdown(
        f'<h1 class="main-header">🏠 {texts["page_title"]}</h1>', unsafe_allow_html=True
    )
    st.markdown(texts["page_description"])

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header(texts["upload_section"])

        # File uploader - PNG only
        uploaded_file = st.file_uploader(
            texts["upload_label"],
            type=["png"],
            help=texts["upload_help"],
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(
                image, caption=texts["uploaded_image_caption"], use_column_width=True
            )

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                image.save(tmp_file.name)
                temp_path = tmp_file.name

            # Analysis button
            if st.button(
                texts["analyze_button"], type="primary", use_container_width=True
            ):
                with st.spinner(texts["analyzing_text"]):
                    try:
                        # Step 1: Detect layout
                        layout_data = detect_layout(temp_path, north_deg, house_facing)

                        # Step 2: Score layout
                        score_data = score_layout(
                            layout_data,
                            st.session_state.hemisphere,
                            st.session_state.language,
                        )

                        # Store results in session state
                        st.session_state.layout_data = layout_data
                        st.session_state.score_data = score_data
                        st.session_state.analysis_done = True

                        st.success(texts["analysis_success"])

                    except Exception as e:
                        st.error(f"{texts['analysis_error']}: {str(e)}")
                    finally:
                        # Clean up temp file
                        os.unlink(temp_path)

    with col2:
        st.header(texts["results_section"])

        if st.session_state.get("analysis_done", False):
            score_data = st.session_state.score_data
            layout_data = st.session_state.layout_data

            # Display score and grade
            display_score_card(score_data, texts)

            # Display breakdown
            display_breakdown(score_data, texts)

            # Display detected rooms
            display_detected_rooms(layout_data, texts)

            # Display advice
            display_advice(score_data, texts)

        else:
            st.info(texts["no_analysis_yet"])
            st.markdown(f"### {texts['score_preview']}")
            for grade, description in texts["grade_levels"].items():
                st.markdown(f"- **{description}**")


def display_score_card(score_data, texts):
    """Display the main score card"""
    total = score_data["total"]
    grade = score_data["grade"]
    house_gua = score_data["house_gua"]

    # Grade color mapping
    grade_colors = {
        "S": "grade-s",
        "A": "grade-a",
        "B": "grade-b",
        "C": "grade-c",
        "D": "grade-d",
    }

    st.markdown(
        f"""
    <div class="score-card">
        <h2>{texts['total_score']}</h2>
        <div class="{grade_colors.get(grade, 'grade-d')}">{total}{texts['points']}</div>
        <h3>{texts['grade']}: {grade}{texts['level']}</h3>
        <p>{house_gua}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_breakdown(score_data, texts):
    """Display detailed breakdown"""
    st.subheader(texts["detailed_scores"])

    breakdown = score_data["breakdown"]

    # Create a DataFrame for better display
    import pandas as pd

    breakdown_data = []
    for key, value in breakdown.items():
        breakdown_data.append(
            {
                "Item": texts["score_items"].get(key, key),
                texts["score"]: value["score"],
                texts["explanation"]: value["why"],
            }
        )

    df = pd.DataFrame(breakdown_data)

    # Color code the scores
    def color_score(val):
        if val > 0:
            return "background-color: #d4edda; color: #155724"
        elif val < 0:
            return "background-color: #f8d7da; color: #721c24"
        else:
            return "background-color: #f8f9fa; color: #6c757d"

    styled_df = df.style.applymap(color_score, subset=[texts["score"]])
    st.dataframe(styled_df, use_container_width=True)


def display_detected_rooms(layout_data, texts):
    """Display detected rooms"""
    st.subheader(texts["detected_rooms"])

    rooms = layout_data.get("rooms", [])

    if rooms:
        for room in rooms:
            st.markdown(
                f"""
            <div class="room-item">
                <strong>{room['norm_label']}</strong> 
                ({texts['original_text']}: {room['raw_text']})<br>
                {texts['position']}: {room['palace9']} | {texts['direction']}: {room['direction8']} | {texts['confidence']}: {room['conf']:.1f}%
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.warning(texts["no_rooms_detected"])


def display_advice(score_data, texts):
    """Display advice"""
    st.subheader(texts["optimization_advice"])

    advice_list = score_data.get("advice", [])

    if advice_list:
        for i, advice in enumerate(advice_list, 1):
            st.markdown(
                f"""
            <div class="advice-box">
                <strong>{texts['advice_prefix']} {i}:</strong> {advice}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info(texts["no_advice"])


if __name__ == "__main__":
    main()
