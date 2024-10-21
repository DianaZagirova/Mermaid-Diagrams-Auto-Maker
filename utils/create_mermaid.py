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
from llm.llm_utils import init_llm
import streamlit.components.v1 as components

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
        height=600,
    )

    # html(
    #     f"""
    #     <pre class="mermaid">
    #         {code}
    #     </pre>

    #     <script type="module">
    #         import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    #         mermaid.initialize({{ startOnLoad: true, theme: "forest", themeVariables: {{ fontSize: "14px", padding: "10px" }} }});
        
    #     </script>
    #     """,
    #     height=st.session_state["svg_height"] + 50,
    # )
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


def mermaid_chart(mindmap_code):
    # html_code = f"""
    # <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    # <div class="mermaid">{mindmap_code}</div>
    # <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    # <script>
    #     mermaid.initialize({{
    #         startOnLoad: true,            
    #         fontFamily: "arial",
    #         themeVariables: {{
    #             fontSize: "30px",  
    #             primaryColor: "#96ab91",
    #             padding: "15px"   
    #         }}
    #     }});
    # </script>
    # """
    
    html_code = f'''
    <div class="mermaid">
    {mindmap_code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    '''
    components.html(html_code, height=600)

    return html_code

def render_mermaid_chart(context):
    mermaid_code, mermaid_link, text_to_download = get_mermaid_data(context)
    st.code(mermaid_code)    
    # html(mermaid_chart(mermaid_code), width=1005, height=900)
    # mermaid_chart(mermaid_code)
    mermaid(mermaid_code)
    st.download_button(
            label="Download mermaid file",
            data=text_to_download.getvalue(),
            file_name="mermaid_diagram.txt",
            mime="text/plain"
        )
    
    link='The link for flowchart rendering on  [mermaid_live]({mermaid_live})'.format(mermaid_live=mermaid_link)
    st.markdown(link, unsafe_allow_html=True)


def get_mermaid_data(context):
        llm = init_llm()  
        llm_prompts = json.load(open("./prompts/llm_prompts.json"))           
        # msg = [
        #     SystemMessage(content=system_prompt),
        #     HumanMessage(content=user_prompt),
        #     AIMessage(content=assistant_prompt),
        #     HumanMessage(content = context)
        # ]    
        msg = [          
             SystemMessage(content=llm_prompts['system_prompt_for_mermaid']),
            HumanMessage(content = context)
        ]      
        res = llm(messages=msg)
        # mermaid_code = res.content.strip('```').strip('\n```').strip('```\n').strip('```\n\n').strip('\n\n```')
        
        mermaid_code = res.content.strip('```').strip('\n```').strip('```\n').strip('```\n\n').strip('\n\n```').splitlines()[0:-1]
        mermaid_code = '\n'.join(mermaid_code)
        text_to_download = StringIO(mermaid_code) 
        mermaid_link = genPakoLink(mermaid_code)
        return mermaid_code, mermaid_link, text_to_download 
            


