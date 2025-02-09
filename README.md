# Mermaid Diagram Generator

🤖 A user-friendly Streamlit application that automatically transforms text into Mermaid diagrams using LLM. Whether you need flowcharts, sequence diagrams, state diagrams, or other visualization types, this tool makes diagram creation intuitive and efficient. Chat on the resulted diagram and ask LLM to improve or modify it!

## Features

- **Multiple Diagram Types**: Create various types of Mermaid diagrams including:
  - Flowcharts
  - Sequence diagrams
  - State diagrams
  - Class diagrams
  - Entity Relationship diagrams
  - And more!

- **AI-Powered Generation**: 
  - Intelligent conversion of text descriptions into structured diagrams
  - Automatic summarization for better diagram clarity
  - Smart validation and error correction

- **Interactive Chat Interface**: 
  - Engage in a conversation with the AI agent to refine your diagrams
  - Real-time diagram updates based on your feedback
  - Natural language interaction for diagram adjustments

- **Quality Assurance**:
  - Automatic validation of generated Mermaid syntax
  - Built-in error correction and retry mechanisms
  - Export diagrams as SVG files

## Getting Started

1. Clone the repository
2. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key
   ```
3. Build and run using Docker:
   ```bash
   docker-compose up --build
   ```
4. Open your browser and navigate to `http://localhost:8510`

## Usage

1. Enter your text to convert into a diagram
2. Select the desired diagram type
3. The AI will generate an initial diagram based on your input
4. Use the chat interface to refine the diagram:
   - Request changes to specific parts
   - Add or remove elements
   - Modify relationships or connections
   - Adjust the layout or style

## How It Works

1. **Text Processing**:
   - AI analyzes your input text to understand the structure and relationships
   - Automatic summarization for complex inputs
   - Smart context management for diagram refinements

2. **Diagram Generation**:
   - Converts natural language into valid Mermaid syntax
   - Applies best practices for diagram layout and organization
   - Supports multiple diagram types with appropriate validation

3. **Interactive Refinement**:
   - Chat with the AI to modify your diagrams
   - Real-time updates as you make changes
   - Natural language commands for diagram adjustments

4. **Export Options**:
   - Save diagrams as SVG files
   - Copy Mermaid code for use in other tools
   - Direct links to edit in Mermaid Live Editor

## Resources

- [Mermaid Documentation](https://mermaid.js.org)
- [Mermaid Live Editor](https://mermaid.live)
- [Mermaid CLI GitHub](https://github.com/mermaid-js/mermaid-cli)tual modifications to the diagrams.