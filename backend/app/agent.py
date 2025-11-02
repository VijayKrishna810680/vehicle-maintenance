# Simple LangChain agent skeleton. Configure your provider (OpenAI or other) via env vars.
import os
from typing import Optional

try:
    from langchain_openai import OpenAI
    from langchain.agents import initialize_agent, AgentType
    from langchain.tools import Tool
    
    def calc_tool_fn(inp: str) -> str:
        try:
            return str(eval(inp))
        except Exception as e:
            return f"Error: {e}"
    
    tools = [Tool(name="calculator", func=calc_tool_fn, description="Use to calculate math")]
    
    # Check if OpenAI API key is available
    if os.getenv("OPENAI_API_KEY"):
        llm = OpenAI(temperature=0.7)
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    else:
        # Fallback agent that doesn't require API key
        class MockAgent:
            def run(self, message: str) -> str:
                return f"Mock response to: {message}. Please set OPENAI_API_KEY environment variable for full functionality."
        
        agent = MockAgent()
        
except ImportError:
    # Fallback if langchain packages not available
    class MockAgent:
        def run(self, message: str) -> str:
            return f"Simple echo response: {message}"
    
    agent = MockAgent()