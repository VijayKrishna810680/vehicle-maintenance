# AI Agent with Dual Mode (Real AI + Offline Fallback)
import os
from typing import Optional

try:
    from langchain_openai import OpenAI
    from langchain.agents import initialize_agent, AgentType
    from langchain.tools import Tool
except ImportError:
    OpenAI = None
    initialize_agent = None
    AgentType = None
    Tool = None

# --- Simple offline AI responses (no API key needed) ---
OFFLINE_KNOWLEDGE = {
    "oil": [
        "Change your engine oil every 10,000 km or 6 months.",
        "Always use manufacturer-recommended oil grade for better performance."
    ],
    "service": [
        "Regular servicing every 6 months keeps your car in top shape.",
        "Skipping service can reduce mileage and engine life."
    ],
    "engine": [
        "If the engine makes noise, check oil levels or spark plugs.",
        "The check engine light often means a sensor issue."
    ],
    "tyre": [
        "Check tyre pressure weekly for safety and fuel efficiency.",
        "Rotate tyres every 10,000 km to prevent uneven wear."
    ],
    "battery": [
        "Car batteries last about 3–5 years.",
        "Clean terminals regularly to prevent corrosion."
    ],
}

def offline_ai(message: str) -> str:
    msg = message.lower()
    for topic, replies in OFFLINE_KNOWLEDGE.items():
        if topic in msg:
            import random
            return random.choice(replies)
    if "hi" in msg or "hello" in msg:
        return "Hey there 👋! I'm your car assistant. How can I help?"
    if "thank" in msg:
        return "You're welcome! 😊"
    return "I'm running in offline mode — I can answer basic maintenance questions like oil, tyres, or engine!"

# --- Real AI mode using OpenAI if API key exists ---
if os.getenv("OPENAI_API_KEY") and OpenAI is not None:
    try:
        def calc_tool_fn(inp: str) -> str:
            try:
                return str(eval(inp))
            except Exception as e:
                return f"Error: {e}"

        tools = [Tool(name="calculator", func=calc_tool_fn, description="Use to calculate math")]

        llm = OpenAI(temperature=0.7)
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

        def run(prompt: str):
            """Use real GPT-4 AI"""
            return agent.run(prompt)

    except Exception as e:
        print("⚠️ Error loading LangChain agent:", e)
        def run(prompt: str):
            return offline_ai(prompt)

else:
    # Offline fallback
    def run(prompt: str):
        return offline_ai(prompt)
