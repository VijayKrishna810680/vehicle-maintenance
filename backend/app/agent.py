# Simple LangChain agent skeleton. Configure your provider (OpenAI or other) via env vars.
from langchain_openai import OpenAI
from langchain.agents import Tool, initialize_agent

def calc_tool_fn(inp: str) -> str:
    try:
        return str(eval(inp))
    except Exception as e:
        return f"Error: {e}"

tools = [Tool(name="calculator", func=calc_tool_fn, description="Use to calculate math")]

llm = OpenAI(temperature=0)  # configure with OPENAI_API_KEY or alternative provider
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
