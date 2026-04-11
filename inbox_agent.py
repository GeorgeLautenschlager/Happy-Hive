import sys
import time
from pathlib import Path

from deepagents import create_deep_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from watchdog.observers import Observer

from inbox_handler import InboxHandler


OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4:e4b"
INBOX_PATH = Path.home() / "gtd" / "inbox.md"


@tool
def placeholder_tool(query: str) -> str:
    """A placeholder tool. Replace with real tools."""
    return f"Result for: {query}"

llm = ChatOllama(model=MODEL, base_url=OLLAMA_BASE_URL)

agent = create_deep_agent(
    model=llm,
    tools=[placeholder_tool],
    system_prompt=(
        "You are an expert on GTD. You are responsible for the Clarify and "
        "Organize steps."
    ),
)


def run(message: str) -> None:
    for chunk in agent.stream({"messages": [("human", message)]}):
        print(chunk)
        print("---")


def process_inbox():
    content = INBOX_PATH.read_text(encoding="utf-8")
    prompt = (
        "The GTD inbox has been updated. Here is the list of items:\n\n"
        "---\n"
        f"{content}\n"
        "---\n\n"
        "for each one, attempt to organize the item. If unable ask for clarification"
    )
    run(prompt)


def watch():
    if not INBOX_PATH.exists():
        print(f"Error: {INBOX_PATH} does not exist.", file=sys.stderr)
        sys.exit(1)

    observer = Observer()
    observer.schedule(InboxHandler(INBOX_PATH, process_inbox), str(INBOX_PATH.parent), recursive=False)
    observer.start()
    print(f"Watching {INBOX_PATH} for changes...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch()
