# AI-Driven Mermaid Diagram Creation

This is the repository for an feature of DORA application that automates the creation of Mermaid diagrams from the paper text. This feature utilizes LLM to produce seveeral diagram types such as graphical abstracts, flowcharts, sequence diagrams, and state diagrams.

## Features
! Example workflow is added to ./examples/diagram_creation_flow.ipynb

### 1. Create Graphical Abstract
- **Converts scientific narrative into graphical abstracts.**
This type of the figure should be generated for each document that has section with a title "Abstract". 
- **Input:** All paper text. Preperably from with the rendered links in form Author, year; not with BIB_ID / CHUNK_ID.
- **Processing:** 
1. Prior to generation, the text should be summarized with LLM ('summary_prompt' from "./prompts/llm_prompts.json"). This ensures the better quality of the diagram.
2. Text summary should be used to create the graphical abstract. The graphical abstract is the flowchart type diagram from the mermaid. 
The main function - get_mermaid_data (utils.create_mermaid). This function outputs: mermaid code and the link to mermaid online editor.
3. The results could be saved to SVG through mermaid cli (https://github.com/mermaid-js/mermaid-cli). SVG could be rendered on DORA website.
- **Output:** A stylized Mermaid diagram visualizing the key concepts of the text.

### 2. Create Other Charts
- **Generates flowcharts, sequence diagrams, state diagrams, etc., based on user selection.**
This feature should be similiar to AI actions in DORA. User selects the part of the texts, and the options to create one of the 3 charts appear (flowchart, sequence diagram, state diagram). 
- **Input:** The selected text part
- **Processing:** 
1. The selected text without any processing is directly used for diagram creation. The corresponding prompt should be selected based on the specified graph type.
The main function - get_mermaid_data (utils.create_mermaid). This function outputs: mermaid code and the link to mermaid online editor.
2. The results could be saved to SVG through mermaid cli as well.
- **Output:** Mermaid diagram of the selected type.

### 3. Modify Chart with Custom prompts (Interactive Modifications)
- **Allows interactive modifications via a custom prompts.**
Feature that allow user to modify the generated figure: both graphical abstract and other chart types. 
By clicking on the figure, the user should see the area asking to insert the custom prompt to modify the diagram. The default option could be "Make this graph in green shades".
- **Input:** A user-defined command for changes.
- **Processing:** 
1. Configure the LLM to process this request. If this is the 1 interation of the user on this diagram, create message history with the system prompt. Configure the prompt to add the text based on which the diagram was created and the mermaid code itself.
2. Run LLM get_mermaid_data (utils.create_mermaid). This function outputs: mermaid code and the link to mermaid online editor.
3. Update the history to add user's questiona and the LLM response.
- **Output:** Updated Mermaid code reflecting the changes and the corresponding SVG.

## How It Works

1. **Text Summarization:**
   - Utilizes language models to summarize the input text if needed (only for Graphical Abstract)
   
2. **Diagram Generation:**
   - Employs specific prompts for each diagram type to convert text into Mermaid code.
   
3. **Rendering and Exporting:**
   - Processes the Mermaid code using the Mermaid CLI to generate SVG outputs.
   - Saves and provides links to the generated diagrams.

4. **Interactive Modifications:**
   - A chat history is maintained to facilitate contextual modifications to the diagrams.

