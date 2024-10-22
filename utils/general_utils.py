from time import sleep
import base64
import json
import zlib
import streamlit as st
from io import StringIO
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval
from langchain_community.chat_models import AzureChatOpenAI
import os
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from llm.llm_utils import init_llm, init_llm_model_specific
import streamlit.components.v1 as components
import os


def configure_assistant_prompt():
    llm_prompts = json.load(open("./prompts/llm_prompts.json"))  
    assistant_prompt = llm_prompts.get("assistant_prompt")
    assistant_prompt = assistant_prompt.replace("{context}", st.session_state.mermaid_input)
    assistant_prompt = assistant_prompt.replace("{mermaid_code}", st.session_state.mermaid_code)
    return assistant_prompt
    
