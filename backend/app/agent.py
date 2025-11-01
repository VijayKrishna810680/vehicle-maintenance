# Simple LangChain agent skeleton. Configure your provider (OpenAI or other) via env vars.
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

def calc_tool_fn(inp: str) -> str:
    try:
        return str(eval(inp))
    except Exception as e:
        return f"Error: {e}"

tools = [Tool(name="calculator", func=calc_tool_fn, description="Use to calculate math")]

llm = OpenAI(temperature=0.7)

# Example empty tool list — you can add custom tools later
agent = initialize_agent(
    tools=[],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)