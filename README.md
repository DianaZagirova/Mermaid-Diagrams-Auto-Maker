# AI-Driven Mermaid Diagram Creation

This repository is part of the DORA application and features an automated system for generating Mermaid diagrams from the text of scientific papers. This functionality leverages Large Language Models (LLMs) to produce various diagram types, including graphical abstracts, flowcharts, sequence diagrams, and state diagrams.

For more information on Mermaid, visit the official documentation: [Mermaid](https://mermaid.js.org). You can also use the online visualizer for Mermaid code here: [Mermaid Live Editor](https://mermaid.live).

## Features

An example workflow is provided in `./examples/diagram_creation_flow.ipynb`.
A main file for a diagram creation `./utils/create_mermaid.py`.


### 1. Create Graphical Abstract

- **Purpose:** Converts scientific narratives into graphical abstracts. This type of figure should be generated for every document that contains a section titled "Abstract."
- **Input:** Full text of the paper, preferably written with rendered links in the format Author, Year; do not use BIB_ID or CHUNK_ID.
- **Processing:**
  1. Prior to generation, the text is summarized using the LLM's 'summary_prompt' from `./prompts/llm_prompts.json`. This ensures better quality diagrams.
  2. The text summary is then utilized to create the graphical abstract, which takes the form of a flowchart diagram in Mermaid syntax. The main function for this process is `get_mermaid_data (utils.create_mermaid)`, which outputs both the Mermaid code and a link to the Mermaid online editor.

  ! Sometimes LLM fails to produce a valid mermaid code. There are some mechanisms that help to prevent this ( [validation function](https://gitlab.com/insilicoteam/pandomics/paperdrafttool/-/blob/mermaid_diagrams/utils/create_mermaid.py?ref_type=heads#L205) in `./utils/create_mermaid.py`):
  - Additional LLM call is used with the prompt that asks to check the produced code and correct it if needed.
  - Mermaid code is tried to be saved as SVG. If there are errors, retry is activated. 
  - If the number of retries would be increased, it also increases the cost of generaion. But with high retry number, it is save to use very cheap models such as gpt-4o-mini.

  3. The resulting diagram can be saved as an SVG file using the Mermaid CLI ([Mermaid CLI GitHub](https://github.com/mermaid-js/mermaid-cli)). The SVG can be rendered on the DORA website.
- **Output:** A visually appealing Mermaid diagram that illustrates the key concepts of the text.

### 2. Create Other Charts

- **Purpose:** Generates flowcharts, sequence diagrams, state diagrams, etc., based on user selection. This feature operates similarly to AI actions in DORA. Users can select a section of text, after which options to create one of the three chart types (flowchart, sequence diagram, state diagram) will appear.
- **Input:** The selected portion of the text.
- **Processing:**
  1. The selected text undergoes minimal processing. Currently, no defined procedure for processing exists, but it is anticipated that a processing function may be required in the future. The current implementation uses the selected text directly for diagram creation.
  2. The appropriate prompt is selected based on the chosen graph type. The main function for this process is also `get_mermaid_data (utils.create_mermaid)`, which generates the Mermaid code and provides a link to the Mermaid online editor.
  3. Results can also be saved as SVG files through the Mermaid CLI.
- **Output:** A Mermaid diagram of the specified type.

### 3. Modify Chart with Custom Prompts (Interactive Modifications)

- **Purpose:** Provides a feature for interactive modifications using custom prompts. Users can adjust the generated figures—both graphical abstracts and other chart types—by clicking on the figure to access an area for entering a custom prompt. A default option, such as "Make this graph in green shades," can be provided.
- **Input:** A user-defined command for modifications.
- **Processing:**
  1. The LLM is configured to process the user's request. If this is the user's first interaction with the diagram, message history is created with the system prompt. The prompt includes the original text used to generate the diagram and the Mermaid code itself.
  2. The LLM runs through `get_mermaid_data (utils.create_mermaid)`, which outputs the updated Mermaid code and a link to the editor.
  3. The history is updated to log the user's question and the LLM's response.
- **Output:** Updated Mermaid code reflecting the user changes, along with the corresponding SVG.

## How It Works

1. **Text Summarization:**
   - Utilizes LLMs to summarize the input text when necessary (applies only to graphical abstracts).
  
2. **Diagram Generation:**
   - Uses specific prompts for each diagram type to convert text into Mermaid code.
  
3. **Rendering and Exporting:**
   - Processes the Mermaid code through the Mermaid CLI to generate SVG files, saving and providing links to the created diagrams.
  
4. **Interactive Modifications:**
   - Maintains chat history to enable contextual modifications to the diagrams.