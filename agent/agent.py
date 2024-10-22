import streamlit as st
import json
import os
import re
from llm.llm_utils import init_llm_model_specific
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferMemory
from pydantic import BaseModel, Field, Extra
from typing import Dict, List, Type, Optional, Any
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from typing import Any, Sequence

class Agent:
    iterations = 10
    time = 20 * 60
    memory_buffer = 16000

    def __init__(
        self,
        tools: Sequence,
        model_selected: str,
        modified_system_message: str,
        history,
        llm,
        streamlit_usage: bool = True,
    ) -> None:
        self.history = history   
        self.llm = llm         

        if model_selected == "gpt-4o":
            memory = ConversationSummaryBufferMemory(
                memory_key="memory",
                return_messages=True,
                llm=self.llm,
                max_token_limit=self.memory_buffer,
                chat_memory=self.history,
            )
        else:
            memory = ConversationBufferMemory(
                memory_key="memory",
                return_messages=True,
                llm=self.llm,
                max_token_limit=self.memory_buffer,
                chat_memory=self.history,
            )

        system_message = SystemMessage(content=modified_system_message)
        agent_kwargs = {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
            "system_message": system_message,
        }

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
            max_iterations=self.iterations,
            max_execution_time=self.time,
            early_stopping_method="generate",
            memory=memory,
        )

    


