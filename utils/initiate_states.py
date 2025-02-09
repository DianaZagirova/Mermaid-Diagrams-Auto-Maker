import os
import streamlit as st
from pathlib import Path

# Constants
DEFAULT_EXAMPLE_TEXT_PATH = "./data/example_text.txt"
DEV_MODE = "public" #"dev" / "public"

def load_example_text():
    """Load example text from file with proper error handling"""
    try:
        with Path(DEFAULT_EXAMPLE_TEXT_PATH).open('r') as file:
            return file.read()
    except FileNotFoundError:
        st.warning(f"Example text file not found at {DEFAULT_EXAMPLE_TEXT_PATH}")
        return ""
    except Exception as e:
        st.error(f"Error reading example text file: {str(e)}")
        return ""

def init_states():
    """Initialize Streamlit session state variables.
    
    Groups related variables and sets their default values:
    1. Application settings and mode
    2. User input and prompts
    3. Mermaid diagram states
    4. Chat and question states
    """
    
    # Application settings and mode
    if "app_mode" not in st.session_state:
        st.session_state.app_mode = DEV_MODE
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    if "review_code" not in st.session_state:
        st.session_state.review_code = False
    
    # User input and prompts
    if "text_input" not in st.session_state:
        st.session_state.text_input = load_example_text()
    if "prompt_for_diagram_creation" not in st.session_state:
        st.session_state.prompt_for_diagram_creation = {}
    if "selected_prompt_for_diagram_creation" not in st.session_state:
        st.session_state.selected_prompt_for_diagram_creation = ""
    if "mermaid_input" not in st.session_state:
        st.session_state.mermaid_input = ""
    
    # Settings state
    if "settings_current" not in st.session_state:
        st.session_state.settings_current = {}
    if "settings_previous" not in st.session_state:
        st.session_state.settings_previous = {}
    
    # Mermaid diagram states
    if "mermaid_code" not in st.session_state:
        st.session_state.mermaid_code = ""
    if "mermaid_code_corrected" not in st.session_state:
        st.session_state.mermaid_code_corrected = ""
    if "mermaid_link" not in st.session_state:
        st.session_state.mermaid_link = ""
    if "text_to_download" not in st.session_state:
        st.session_state.text_to_download = ""
    
    # Chat-based diagram states
    if "mermaid_code_chat_based" not in st.session_state:
        st.session_state.mermaid_code_chat_based = ""
    if "mermaid_link_chat_based" not in st.session_state:
        st.session_state.mermaid_link_chat_based = ""
    if "text_to_download_chat_based" not in st.session_state:
        st.session_state.text_to_download_chat_based = ""
    
    # Chat and history states
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "internal_history" not in st.session_state:
        st.session_state.internal_history = []
    if "question_current" not in st.session_state:
        st.session_state.question_current = ''
    if "question_previous" not in st.session_state:
        st.session_state.question_previous = ''
    

