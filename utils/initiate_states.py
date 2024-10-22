import streamlit as st


def init_states():
    if "text_input" not in st.session_state:
        st.session_state.text_input = ""

    if "prompt_for_diagram_creation" not in st.session_state:
        st.session_state.prompt_for_diagram_creation = {}
    if "selected_prompt_for_diagram_creation" not in st.session_state:
        st.session_state.selected_prompt_for_diagram_creation = ""      

    if "mermaid_input" not in st.session_state:
        st.session_state.mermaid_input = ""

    if "settings_current" not in st.session_state:
        st.session_state.settings_current = {}
    if "settings_previous" not in st.session_state:
        st.session_state.settings_previous = {}
    
    if "mermaid_code" not in st.session_state:
        st.session_state.mermaid_code = ""

    if "mermaid_code_corrected" not in st.session_state:
        st.session_state.mermaid_code_corrected = ""

    if "mermaid_link" not in st.session_state:
        st.session_state.mermaid_link = ""

    if "text_to_download" not in st.session_state:
        st.session_state.text_to_download = ""

    if "question_current" not in st.session_state:
            st.session_state.question_current = ''
            
    if "question_previous" not in st.session_state:
            st.session_state.question_previous = ''

    if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

