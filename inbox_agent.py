from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4:e4b"


@tool
def placeholder_tool(query: str) -> str:
    """A placeholder tool. Replace with real tools."""
    return f"Result for: {query}"


tools = [placeholder_tool]

llm = ChatOllama(model=MODEL, base_url=OLLAMA_BASE_URL)

agent = create_react_agent(llm, tools)


def run(message: str) -> None:
    for chunk in agent.stream({"messages": [("human", message)]}):
        print(chunk)
        print("---")


if __name__ == "__main__":
    run("Hello, what can you help me with?")
