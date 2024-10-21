from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

load_dotenv()
azure_key_4o = os.getenv('AZURE_KEY')
openai_key = os.getenv('OPENAI_KEY')
# @st.cache_resource
def init_llm():
    llm = AzureChatOpenAI(
            azure_endpoint="https://dora-dev.openai.azure.com/",
            api_version="2024-02-15-preview",
            openai_api_key=azure_key_4o,
            openai_api_type="azure",
            model="gpt-4o",
            temperature=0.2        )

    return llm

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

def get_llm_response(system_prompt, user_query):
        llm = init_llm()             
        msg = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]        
        res = llm(messages=msg)
        return res.content
