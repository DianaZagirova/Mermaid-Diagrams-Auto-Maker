from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

load_dotenv()
openai_key = st.session_state.openai_api_key

@st.cache_resource
def init_llm_model_specific(model, streaming = False):
    return ChatOpenAI(
        openai_api_key=openai_key,
        model_name=model,
        streaming=streaming,
        temperature=0.2,
        max_retries=3
    )
    
def ask_openai_llm(system_prompt, user_input):
    client = OpenAI(api_key = openai_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.8, 
        messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_input
        }
        ]
    )
    return response.choices[0].dict()['message']['content']

def get_llm_response_model_specific(model, system_prompt, user_query, summarization_temperature):
        llm = init_llm_model_specific(model)      
        msg = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]        
        res = llm(messages=msg, temperature = summarization_temperature)
        return res.content
