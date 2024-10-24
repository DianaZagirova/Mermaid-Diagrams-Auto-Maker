### Copyright (c) 2024 Insilico Medicine ###

import streamlit as st
st.set_page_config(page_title="Mermaid", page_icon=":page_facing_up:", layout="wide")
import json
from utils.create_mermaid import get_mermaid_data, mermaid, get_prompt, render_mermaid
from llm.llm_utils import get_llm_response_model_specific, init_llm_model_specific
from formatting.custom_styles import apply_custom_style
from formatting.chat_interface import handle_userInput 
from utils.initiate_states import init_states 
from utils.general_utils import configure_assistant_prompt, check_and_rerun
from pydantic import BaseModel, Field, Extra
from typing import Dict, List, Type, Optional, Any
from langchain.schema import SystemMessage
from langchain.callbacks import get_openai_callback
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.tools import DuckDuckGoSearchRun
from agent.agent import Agent
from langchain.schema import HumanMessage, SystemMessage, AIMessage


apply_custom_style()
init_states()

st.markdown('<div class="header">Create Mermaid Diagram</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Input your document to generate an insightful diagram</div>', unsafe_allow_html=True)

col_settings, col_text = st.columns([1,3])
with col_settings:
    graph_type = st.radio(
    "1. Select the graph type",
    ["**Graphical abstract** 📚", "**Flowchart**", "**Sequence Diagram**", "**State Diagram**"],
    captions=[
        "Graphical abstract of the paper",
        "Illustrate processes or workflows with steps and decision points",
        "Show interactions between entities over time",
        "Illustrate changes in a system's state over time"
    ],
)
    make_summary = False


    
with col_text:
    st.session_state.text_input = st.text_area("2. Input text", height=300, key="input_text", 
                                            value = st.session_state.text_input,
                       help="Paste your document text here.", placeholder="Enter your document text...")
    
    if "prompt_for_diagram_creation" not in st.session_state.prompt_for_diagram_creation:        
        st.session_state.prompt_for_diagram_creation[graph_type] = get_prompt(graph_type)

    with st.expander('3. Edit prompt for a diagram creation'):
        st.session_state.selected_prompt_for_diagram_creation = st.text_area("", height=300, value = st.session_state.prompt_for_diagram_creation.get(graph_type))    

    col_model_main , col_temperature_main = st.columns([1,1])
    with col_model_main:
         diagram_model = st.radio(
        "Model to use for diagram creation",
        ["gpt-4o", "gpt-4o-mini"],
        key="model_main"
    ) 
    with col_temperature_main:
            main_temperature = st.slider(
                "Model temperature",0.0, 2.0, 0.2, 0.1,
                key="temperature_main"
            ) 
    llm_prompts = json.load(open("./prompts/llm_prompts.json"))
    summary_prompt = llm_prompts['summary_prompt']
    if "selected_prompt_for_summarization" not in st.session_state:
        st.session_state.selected_prompt_for_summarization = summary_prompt 
    summarization_model= None
    summarization_temperature = None
    
    if graph_type == "**Graphical abstract** 📚":
        st.divider()
        make_summary = st.checkbox("Make a text summary prior to diagram creation", value=True)
        if make_summary:                       
            with st.expander('**Settings for summarization 💬**'):
                col_model_summary , col_temperature_summary = st.columns([1,1])
                with col_model_summary:
                    summarization_model = st.radio(
                    "Model to use for summarization",
                    ["gpt-4o", "gpt-4o-mini"],
                    key="model_summary"
                ) 
                with col_temperature_summary:
                    summarization_temperature = st.slider(
                    "Model temperature",0.0, 2.0, 0.8, 0.1,
                    key="temperature_summary"
                ) 
                st.session_state.selected_prompt_for_summarization = st.text_area("Prompt for summarization", height=300, value = st.session_state.selected_prompt_for_summarization)  
        

st.session_state.settings_current = {"text":st.session_state.text_input, 
                                    "graph_type":graph_type,
                                    "make_summary":make_summary,
                                    "summarization_model":summarization_model,
                                    "diagram_model":diagram_model,
                                    "prompt_for_diagram_creation":  st.session_state.selected_prompt_for_diagram_creation,
                                    "main_temperature":main_temperature,
                                    "prompt_for_summarization": st.session_state.selected_prompt_for_summarization,
                                    "summarization_temperature":summarization_temperature}
st.divider()

if st.button('Generate Mermaid!') and st.session_state.settings_current != st.session_state.settings_previous:
    if not st.session_state.text_input:
        st.stop()
        st.write('Text input is empty. Please provide text for a diagram')
    
    if make_summary:        
        st.session_state.mermaid_input = get_llm_response_model_specific(diagram_model, st.session_state.selected_prompt_for_summarization, st.session_state.text_input, summarization_temperature)
        with st.expander('Document Summary'):
            st.write(st.session_state.mermaid_input)      
    else:
        st.session_state.mermaid_input = st.session_state.text_input
    st.session_state.settings_previous = st.session_state.settings_current 
    st.session_state.mermaid_code_chat_based, st.session_state.mermaid_link_chat_based, st.session_state.text_to_download_chat_based = "", "", "" 
    st.session_state.question_previous = ""
    st.session_state.question_current = ""
    st.session_state.chat_history = []
    st.session_state.internal_history = []
          
    st.session_state.mermaid_code, st.session_state.mermaid_link, st.session_state.text_to_download = get_mermaid_data(st.session_state.mermaid_input, st.session_state.selected_prompt_for_diagram_creation, diagram_model, main_temperature, review_code=False)

user_question = []
col_chat , col_diagram  = st.columns([1,1])

with col_chat:
    st.session_state.question_current = st.text_area(label="**Chat on a diagram (Agent already knows about your data/code)**", height = 130, placeholder="Fix the diagram to add a new block - 'Current treatment options'")
    assistant_prompt = configure_assistant_prompt() 
      
    col_run, col_clear , colf1, colf2, colf3 = st.columns([2,2, 1, 1, 1])
    with col_run: 
        run_chat = st.button('Run chat')
    with col_clear: 
        clear_chat = st.button('Clear chat')
    if clear_chat:
        st.session_state.question_previous = ""
        st.session_state.question_current = ""
        st.session_state.chat_history = []
        st.session_state.internal_history = []

    if st.session_state.question_current and run_chat:        
        with get_openai_callback() as cb: 
                if not st.session_state.internal_history:
                    st.session_state.internal_history.append(SystemMessage(content=assistant_prompt))
                st.session_state.internal_history.append(HumanMessage(content=st.session_state.question_current)) 
                st.session_state.mermaid_code_chat_based, st.session_state.mermaid_link_chat_based, st.session_state.text_to_download_chat_based = get_mermaid_data(st.session_state.question_current, assistant_prompt, "gpt-4o", 0.2, review_code=False, user_history=True, history = st.session_state.internal_history)
        st.session_state.internal_history.append(AIMessage(content=st.session_state.mermaid_code_chat_based))
        st.session_state.question_previous = st.session_state.question_current 
        st.session_state.chat_history.append(st.session_state.mermaid_code_chat_based)
        st.session_state.chat_history.append(st.session_state.question_current)        
        handle_userInput(st.session_state.chat_history)
    else:
        handle_userInput(st.session_state.chat_history)
    check_and_rerun()

with col_diagram:
    render_mermaid()

