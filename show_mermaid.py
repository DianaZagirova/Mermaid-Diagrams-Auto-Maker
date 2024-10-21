### Copyright (c) 2024 Insilico Medicine ###
import streamlit as st
st.set_page_config(page_title="Mermaid", page_icon=":page_facing_up:", layout="wide")
from langchain.schema import HumanMessage, SystemMessage
import json
from utils.create_mermaid import render_mermaid_chart
from llm.llm_utils import init_llm, ask_openai_llm

# Custom CSS for styling
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
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">Create Mermaid Diagram</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Input your document to generate a flowchart</div>', unsafe_allow_html=True)

# Input area
context = st.text_area("Input text", height=300, key="input_text", help="Paste your document text here.", placeholder="Enter your document text...")
make_summary = st.checkbox("Make a summary first", value=True)

# Generate button
if st.button('Generate Mermaid'):
    if make_summary:
        llm_prompts = json.load(open("./prompts/llm_prompts.json"))
        context = ask_openai_llm(llm_prompts['summary_prompt'], context)            
        with st.expander('Document Summary'):
            st.write(context) 
        # context = summary.content
    render_mermaid_chart(context)