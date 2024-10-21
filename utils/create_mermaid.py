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

def convert_to_single_line(output):
    lines = output.strip().split('\n')
    single_line = ';'.join(lines) + ';'
    return single_line

def mermaid(code: str) -> None:
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=800,
    )

def save_mermaid_as_html(code: str, filename: str = "mermaid_diagram.html") -> None:
    html_content = f"""
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body>
        <pre class="mermaid">
            {code}
        </pre>
    </body>
    </html>
    """
    return html_content

    
def js_btoa(data):
    return base64.b64encode(data)

def pako_deflate(data):
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def genPakoLink(graphMarkdown: str):
    jGraph = {"code": graphMarkdown, "mermaid": {"theme": "default"}}
    byteStr = json.dumps(jGraph).encode('utf-8')
    deflated = pako_deflate(byteStr)
    dEncode = js_btoa(deflated)
    link = 'http://mermaid.live/edit#pako:' + dEncode.decode('ascii')
    return link


def get_prompt(graph_type):
    graph_type_to_prompt = {"**Graphical abstract** 📚": "system_prompt_for_mermaid_graphical_abstract",
                                "**Flowchart**" :"system_prompt_for_mermaid_flowchart", 
                                "**Sequence Diagram**":"system_prompt_for_mermaid_sequence_diagram", 
                                "**State Diagram**":"system_prompt_for_mermaid_state_diagram",
                                "**Timeline Diagram**":"system_prompt_for_mermaid_timeline_diagram", 
                                "**Pie Chart**":"system_prompt_for_mermaid_flowchart_pie_chart"}
    selected_prompt = graph_type_to_prompt.get(graph_type)
    llm_prompts = json.load(open("./prompts/llm_prompts.json"))  
    return llm_prompts.get(selected_prompt)

def get_mermaid_data(context, prompt, diagram_model, main_temperature):            
        llm = init_llm_model_specific(diagram_model)
        msg = [          
            SystemMessage(content=prompt),
            HumanMessage(content = context)
        ]      
        res = llm(messages=msg, temperature = main_temperature)        
        mermaid_code = res.content.strip('```').strip('\n```').strip('```\n').strip('```\n\n').strip('\n\n```').splitlines()[0:-1]
        mermaid_code = '\n'.join(mermaid_code)
        text_to_download = StringIO(mermaid_code) 
        mermaid_link = genPakoLink(mermaid_code)
        return mermaid_code, mermaid_link, text_to_download 
            


