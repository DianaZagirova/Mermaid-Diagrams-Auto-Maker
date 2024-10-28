from time import sleep
import base64
import json
import zlib
import streamlit as st
from io import StringIO
import os
from langchain.schema import HumanMessage, SystemMessage
from llm.llm_utils import init_llm_model_specific
import streamlit.components.v1 as components
import subprocess
import tempfile
from IPython.display import SVG, display
from typing import Tuple, Optional, Dict, Any, Union
import logging
import io
logging.basicConfig(level=logging.INFO)

def mermaid(code: str) -> None:
    """
    Renders a Mermaid diagram using the provided code string and displays it in HTML format.

    This function takes a string containing the Mermaid syntax for a diagram and embeds it within 
    an HTML structure that utilizes Mermaid's JavaScript library to visualize the diagram. 
    Parameters:
    ----------
    code : str
        A string that contains the Mermaid diagram definition code.

    Returns:
    -------
    None           
    """
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

def get_mermaid_as_html(code: str) -> str:
    """
    Generates an HTML string that embeds a Mermaid diagram.

    This function takes a Mermaid code string as input and returns a formatted HTML document. 
    The generated HTML includes the necessary JavaScript to import and initialize Mermaid when the document is loaded.

    Parameters:
    code (str): A string containing the Mermaid syntax to define the diagram.

    Returns:
    str: A string containing the complete HTML document ready for rendering a Mermaid diagram.
    """
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

def js_btoa(data: bytes) -> bytes:
    """
    Encodes the input bytes using Base64 encoding.

    Parameters:
    ----------
    data : bytes
        The input data to be encoded.

    Returns:
    -------
    bytes
        The Base64 encoded data.

    Raises:
    ------
    TypeError
        If the input is not of type bytes.
    """
    if not isinstance(data, bytes):
        raise TypeError("Input must be of type bytes")
    return base64.b64encode(data)

def pako_deflate(data: bytes) -> bytes:
    """
    Compresses the input data using zlib compression.

    Parameters:
    ----------
    data : bytes
        The input data to be compressed.

    Returns:
    -------
    bytes
        The compressed data.

    Raises:
    ------
    TypeError
        If the input is not of type bytes.
    """
    if not isinstance(data, bytes):
        raise TypeError("Input must be of type bytes")
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def genPakoLink(graphMarkdown: str) -> str:
    """
    Generates a Mermaid Live Editor link for the given graph markdown.

    Parameters:
    ----------
    graphMarkdown : str
        The Mermaid graph markdown to be encoded in the link.

    Returns:
    -------
    str
        A URL for the Mermaid Live Editor with the encoded graph.

    Raises:
    ------
    json.JSONDecodeError
        If there's an error in JSON encoding.
    """
    try:
        jGraph = {"code": graphMarkdown, "mermaid": {"theme": "default"}}
        byteStr = json.dumps(jGraph).encode('utf-8')
        deflated = pako_deflate(byteStr)
        dEncode = js_btoa(deflated)
        link = 'http://mermaid.live/edit#pako:' + dEncode.decode('ascii')
        return link
    except json.JSONDecodeError as e:
        logging.error(f"Error in JSON encoding: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in genPakoLink: {str(e)}")
        raise

def get_prompt(graph_type: str) -> Optional[str]:
    """
    Retrieves the appropriate prompt for a given graph type from a JSON file.

    Parameters:
    ----------
    graph_type : str
        The type of graph for which to retrieve the prompt.

    Returns:
    -------
    Optional[str]
        The prompt for the specified graph type, or None if not found.

    Raises:
    ------
    FileNotFoundError
        If the JSON file containing prompts is not found.
    json.JSONDecodeError
        If there's an error in decoding the JSON file.
    """
    graph_type_to_prompt = {
        "**Graphical abstract** 📚": "system_prompt_for_mermaid_graphical_abstract",
        "**Flowchart**": "system_prompt_for_mermaid_flowchart",
        "**Sequence Diagram**": "system_prompt_for_mermaid_sequence_diagram",
        "**State Diagram**": "system_prompt_for_mermaid_state_diagram",
        "**Timeline Diagram**": "system_prompt_for_mermaid_timeline_diagram",
        "**Pie Chart**": "system_prompt_for_mermaid_flowchart_pie_chart"
    }
    selected_prompt = graph_type_to_prompt.get(graph_type)
    if not selected_prompt:
        logging.warning(f"No prompt found for graph type: {graph_type}")
        return None

    try:
        with open("./prompts/llm_prompts.json", 'r') as f:
            llm_prompts = json.load(f)
        return llm_prompts.get(selected_prompt)
    except FileNotFoundError:
        logging.error("llm_prompts.json file not found")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in llm_prompts.json: {str(e)}")
        raise

def validate_mermaid_syntax(mermaid_code: str) -> Tuple[bool, str]:
    """
    Validates the syntax of Mermaid code by attempting to generate an SVG using the Mermaid CLI.
    
    Parameters:
    - mermaid_code (str): The Mermaid code to validate.
    
    Returns:
    - Tuple[bool, str]: A tuple containing a boolean indicating if the syntax is valid,
                        and a string with an error message if invalid (empty string if valid).
    """
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_file:
        temp_output_path = temp_file.name

    try:
        is_valid = run_mermaid_cli(mermaid_code, streamlit_usage=False, output_file_path=temp_output_path)
        
        if is_valid:
            return True, ""
        else:
            return False, "Failed to generate SVG from Mermaid code. The syntax may be invalid."
    
    except Exception as e:
        return False, f"An error occurred while validating Mermaid syntax: {str(e)}"
    
    finally:
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

def get_mermaid_data(context: str, prompt: str, diagram_model: str, main_temperature: float, review_code: bool =False, user_history: bool = False, history: list = None, n_retries: int = 3) -> Tuple[str, str, StringIO]:
    """
    Generates and returns Mermaid diagram data, download link, and a string buffer for export.
    Given a text (context) and prompt this function initializes the LLM to retrieve a Mermaid diagram.
    It will retry generating valid Mermaid code up to n_retries times if the initial attempt is not successful.

    Parameters:
    - context (str): The context or content that will be interpreted by LLM.
    - prompt (str): The prompt to initiate the interaction with LLM.
    - diagram_model (str): The specific diagram model identifier for initializing the LLM.
    - main_temperature (float): The temperature setting for generating variations in LLM outputs.
    - history (list): The list of the previous messages
    - n_retries (int): The number of times to retry generating valid Mermaid code.


    Returns:
    - Tuple[str, str, StringIO]: Returns a tuple containing Mermaid code, 
                                  a downloadable link for the code, and a StringIO
                                  object representing the text to be downloaded.
    """
    llm = init_llm_model_specific(diagram_model)
    
    for attempt in range(n_retries):
        if user_history:
            messages = history
        else:
            messages = [
                    SystemMessage(content=prompt),
                    HumanMessage(content=context)
                ]
            
        response = llm(messages=messages, temperature=main_temperature)
        raw_content = response.content
        
        if review_code:
            llm_prompts = json.load(open("./prompts/llm_prompts.json"))
            messages = [
                    SystemMessage(content=llm_prompts.get("diagram_reviewer_prompt")),
                    HumanMessage(content=raw_content)
                ]
            response = llm(messages=messages, temperature=main_temperature)
            raw_content = response.content

        mermaid_code = extract_mermaid_code(raw_content)    
        is_valid, error_message = validate_mermaid_syntax(mermaid_code)
        # st.write(f"attempt - {attempt}, is_valid - {is_valid}, error_message - {error_message}") #print logs
        if is_valid:
            text_to_download = StringIO(mermaid_code)
            mermaid_link = genPakoLink(mermaid_code)
            return mermaid_code, mermaid_link, text_to_download
        else:
            logging.error(f"Attempt {attempt + 1}/{n_retries}: Mermaid syntax error: {error_message}")            
            if attempt == n_retries - 1:
                logging.error(f"Failed to generate valid Mermaid code after {n_retries} attempts.")    
        
    text_to_download = StringIO(mermaid_code)
    mermaid_link = genPakoLink(mermaid_code)
    return mermaid_code, mermaid_link, text_to_download

def extract_mermaid_code(raw_content: str) -> str:
    """
    Extracts and refines Mermaid code from raw LLM response content.

    This function removes unwanted characters and markdown artifacts, providing
    clean Mermaid code ready for use or download.
    Assume the Mermaid code is enclosed within Markdown code block syntax.

    Parameters:
    - raw_content (str): The raw content string from the LLM response.

    Returns:
    - str: Refined Mermaid code as a string.
    """
    stripped_content = raw_content.strip('```').strip().split('\n')
    
    if stripped_content and stripped_content[0].startswith('mermaid'):
        stripped_content = stripped_content[1:]
    
    return '\n'.join(stripped_content).strip() 
            
def run_mermaid_cli(
    mermaid_syntax: str,
    streamlit_usage: bool = True,
    output_file_path: str = "./files/mermaid_output.svg"
) -> bool:
    """
    Generates an SVG file from Mermaid syntax using the Mermaid CLI.
    This function takes Mermaid syntax as input and utilizes the Mermaid CLI to generate an SVG file.
    It supports both Streamlit and non-Streamlit environments, allowing for different ways of interacting
    with the generated SVG content.

    Parameters:
    -----------
    mermaid_syntax : str
        A string with the Mermaid syntax to convert into an SVG file.
    streamlit_usage : bool, optional
        If set to True, the function integrates with Streamlit by providing a download button for the SVG file.
        If set to False, the SVG content is displayed directly in environments like Jupyter Notebook. Default is True.
    output_file_path : str, optional
        The file path where the SVG file will be saved. The default path is "./files/mermaid_output.svg".
        The function will create any necessary directories if they do not exist.    
    
    Returns:
    --------
    bool: True if the Mermaid CLI executed successfully, False otherwise.

    Notes:
    ------
    - Ensure that the Mermaid CLI (mmdc) and necessary configurations are correctly installed and configured.
    - In Streamlit mode, a download button is rendered to allow users to save the SVG file.
    - In non-Streamlit environments, the SVG content is displayed directly using IPython's display utilities.
    """
    logging.basicConfig(level=logging.INFO) 
    input_file_name: Optional[str] = None
    output_file_name: Optional[str] = None

    try:            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mmd') as input_file:
            input_file_name = input_file.name
            input_file.write(mermaid_syntax.encode('utf-8'))
            input_file.flush()  

        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as output_file:
            output_file_name = output_file.name

        command = [
            'mmdc',
            '-i', input_file_name,
            '-o', output_file_name,
            '--puppeteerConfigFile', 'puppeteer-config.json'
        ]

        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("Mermaid CLI executed successfully.")              

        if streamlit_usage and st is not None:
            with open(output_file_name, 'rb') as svg_file:
                st.download_button(
                    label="Save Mermaid as SVG",
                    data=svg_file,
                    file_name='mermaid_file.svg',
                    mime='image/svg+xml'
                )
        elif display is not None:
            with open(output_file_name, 'r') as svg_file:
                svg_content = svg_file.read()
                display(SVG(svg_content))
        else:
            logging.info("Streamlit or Jupyter display not available.")

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_name, 'r') as svg_file, open(output_file_path, 'w') as output_file:
            output_file.write(svg_file.read())
            logging.info(f"SVG file saved as {output_file_path}")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while executing the Mermaid CLI command")
        logging.debug("Output: %s", e.output.decode('utf-8'))
        logging.debug("Error: %s", e.stderr.decode('utf-8'))
        return False
        
    except FileNotFoundError:
        logging.error("The 'mmdc' command is not found. Ensure Mermaid CLI is installed and available in your PATH.")
        if streamlit_usage and st is not None:
            st.error("The 'mmdc' command is not found. Make sure Mermaid CLI is installed and available in your PATH.")        
        return True        
    
    finally:
        if input_file_name and os.path.exists(input_file_name):
            os.remove(input_file_name)
        if output_file_name and os.path.exists(output_file_name):
            os.remove(output_file_name)

def download_buttons_layout(data_to_visualize):
    """
    Creates the layout for download buttons for SVG, TXT, and HTML formats.
    """
    col_download_svg, col_download_code, col_download_html = st.columns([2, 2, 2])

    # Download SVG
    with col_download_svg:
        svg_status = run_mermaid_cli(data_to_visualize['code'])

    # Download TXT file
    with col_download_code:
        st.download_button(
            label="Save Mermaid as TXT",
            data=data_to_visualize['text'].getvalue() if isinstance(data_to_visualize['text'], io.StringIO) else data_to_visualize['text'],
            file_name="mermaid_diagram.txt",
            mime="text/plain"
        )

    # Download HTML file
    with col_download_html:
        st.download_button(
            label="Save Mermaid as HTML",
            data=get_mermaid_as_html(data_to_visualize['code']),
            file_name="mermaid_diagram.html",
            mime="text/html"
        )

def render_mermaid() -> None:
    """
    Renders the Mermaid diagram based on user input stored in session state.
    Provides options to download the diagram in multiple formats.
    """
    if not st.session_state.mermaid_code:
        st.write('There has been no diagram created yet')

    else:
        st.write('**Mermaid data**')
        
        if st.session_state.mermaid_code_chat_based:
            data_to_visualize = {"code":st.session_state.mermaid_code_chat_based, "link":st.session_state.mermaid_link_chat_based, "text":st.session_state.text_to_download_chat_based, "type" : "chat_based"}
        else:
            data_to_visualize = {"code":st.session_state.mermaid_code, "link":st.session_state.mermaid_link, "text":st.session_state.text_to_download, "type" : "initial"}
        
        with st.expander('Mermaid code'):
            st.code(data_to_visualize.get('code'))              

        with st.expander('Text for a diagram creation'):
            st.write(st.session_state.mermaid_input) 

        download_buttons_layout(data_to_visualize)
          
        link='**The link for flowchart rendering on**  [mermaid_live]({mermaid_live})'.format(mermaid_live=data_to_visualize.get('link'))
        st.markdown(link, unsafe_allow_html=True) 

        mermaid(data_to_visualize.get('code'))

