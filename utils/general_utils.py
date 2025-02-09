import json
import streamlit as st


def configure_assistant_prompt(prompt_path: str = "./prompts/llm_prompts.json"):
    llm_prompts = json.load(open(prompt_path))  
    assistant_prompt = llm_prompts.get("assistant_prompt")
    assistant_prompt = assistant_prompt.replace("{context}", st.session_state.mermaid_input)
    assistant_prompt = assistant_prompt.replace("{mermaid_code}", st.session_state.mermaid_code)
    return assistant_prompt


def check_and_rerun():
    # Store previous state
    if 'prev_mermaid_code_chat_based' not in st.session_state:
        st.session_state.prev_mermaid_code_chat_based = st.session_state.mermaid_code_chat_based
    if 'prev_mermaid_link_chat_based' not in st.session_state:
        st.session_state.prev_mermaid_link_chat_based = st.session_state.mermaid_link_chat_based
    if 'prev_text_to_download_chat_based' not in st.session_state:
        st.session_state.prev_text_to_download_chat_based = st.session_state.text_to_download_chat_based

    # Check for changes
    if (st.session_state.mermaid_code_chat_based != st.session_state.prev_mermaid_code_chat_based or
        st.session_state.mermaid_link_chat_based != st.session_state.prev_mermaid_link_chat_based or
        st.session_state.text_to_download_chat_based != st.session_state.prev_text_to_download_chat_based):
        
        # Update previous state
        st.session_state.prev_mermaid_code_chat_based = st.session_state.mermaid_code_chat_based
        st.session_state.prev_mermaid_link_chat_based = st.session_state.mermaid_link_chat_based
        st.session_state.prev_text_to_download_chat_based = st.session_state.text_to_download_chat_based
        
        # Rerun the script
        st.experimental_rerun()
    
