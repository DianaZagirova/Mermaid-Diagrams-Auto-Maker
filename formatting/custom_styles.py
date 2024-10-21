### Copyright (c) 2024 Insilico Medicine ###

import streamlit as st

def apply_custom_style():
    st.markdown(
    """
    <style>
    .header {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: #1a73e8;
    }
    .subheader {
        text-align: center;
        font-size: 20px;
        color: #555555;
    }
    .text-area {
        margin: 20px 0;
    }
    
    button[kind="secondary"] {
        background-color: #f0f0f0; /* Light background for secondary button */
        color: #1a73e8; /* Primary color for text */
        border: 2px solid #1a73e8; /* Border matching primary color */
        padding: 12px 24px; /* Increased padding */
        border-radius: 8px; /* More rounded corners */
        cursor: pointer; /* Pointer cursor */
        font-size: 16px; /* Font size */
        font-weight: bold; /* Bold text */
        transition: background-color 0.3s, transform 0.2s, color 0.3s; /* Transition effects */
    }
    button[kind="secondary"]:hover {
        background-color: #edf6ff; /* Change background to primary color on hover */
        transform: scale(1.05); /* Slightly enlarge on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)