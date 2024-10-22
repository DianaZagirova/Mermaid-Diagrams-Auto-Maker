from time import sleep
import base64
import json
import zlib
import streamlit as st
from io import StringIO
from streamlit_js_eval import streamlit_js_eval
import os
from langchain.schema import HumanMessage, SystemMessage
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
            

def render_mermaid():
    if not st.session_state.mermaid_code:
        st.write('There has been no diagram created yet')
    else:
        st.write('**Mermaid data**')

        with st.expander('Mermaid code'):
            st.session_state.mermaid_code_corrected = st.text_area("", height = 200, value = st.session_state.mermaid_code)  

        with st.expander('Text for a diagram creation'):
            st.write(st.session_state.mermaid_input) 
        
        if st.session_state.mermaid_code_corrected != st.session_state.mermaid_code:
            st.session_state.text_to_download = StringIO(st.session_state.mermaid_code_corrected) 
            st.session_state.mermaid_link = genPakoLink(st.session_state.mermaid_code_corrected)
            st.session_state.mermaid_code = st.session_state.mermaid_code_corrected       
        

        col_download_code, col_download_html, colf1, colf2, colf3 = st.columns([2,2, 1, 1, 1])
        with col_download_code:
            st.download_button(
                label="Save Mermaid as TXT",
                data=st.session_state.text_to_download.getvalue(),
                file_name="mermaid_diagram.txt",
                mime="text/plain"
            )    
        with col_download_html:
            st.download_button(
                label="Save Mermaid as HTML",
                data=save_mermaid_as_html(st.session_state.mermaid_code),
                file_name="mermaid_diagram.html"
            )  
        link='**The link for flowchart rendering on**  [mermaid_live]({mermaid_live})'.format(mermaid_live=st.session_state.mermaid_link)
        st.markdown(link, unsafe_allow_html=True) 
        mermaid(st.session_state.mermaid_code)