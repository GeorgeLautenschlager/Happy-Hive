import sys
import time
import hashlib
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4:e4b"
INBOX_PATH = Path.home() / "gtd" / "inbox.md"
SKILLS_DIR = Path(__file__).parent.parent / "skills"

@tool
def placeholder_tool(query: str) -> str:
    """A placeholder tool. Replace with real tools."""
    return f"Result for: {query}"

llm = ChatOllama(model=MODEL, base_url=OLLAMA_BASE_URL, num_ctx=32768)
agent = create_deep_agent(
    model=llm,
    tools=[placeholder_tool],
    skills=[str(SKILLS_DIR)],
    backend=FilesystemBackend(root_dir="/"),
    system_prompt=(
        "You are an expert on GTD. You are responsible for the Clarify and "
        "Organize steps.\n\n"
        "IMPORTANT: When using the read_file tool, you must use the argument name file_path. "
        "Do NOT use path.\n\n"
        "Correct usage: read_file(file_path=\"/home/user/...\") \n"
        "Incorrect usage: read_file(path=\"/home/user/...\")"
    ),
)

def run(message: str) -> None:
    for chunk in agent.stream({"messages": [("human", message)]}):
        print(chunk)
        print("---")

def process_inbox():
    prompt = (
        f"Use the read_file tool to read the file at file_path=\"{INBOX_PATH}\". "
        "Then apply the clarify skill to the contents, and write the result back "
        f"to \"{INBOX_PATH}\" using the write_file tool. "
        "After that, apply the organize skill to the updated contents."
    )
    run(prompt)

def watch():
    last_hash = None
    print(f"Starting periodic processing of {INBOX_PATH} every 15 minutes...")
    try:
        while True:
            if INBOX_PATH.exists():
                current_hash = hashlib.sha256(INBOX_PATH.read_bytes()).hexdigest()
                if current_hash != last_hash:
                    print(f"{INBOX_PATH} changed, processing...")
                    process_inbox()
                    last_hash = current_hash
                else:
                    print("No changes detected.")
            else:
                print(f"Warning: {INBOX_PATH} not found. Skipping this cycle.")

            print("Sleeping for 15 minutes...")
            time.sleep(15 * 60)
    except KeyboardInterrupt:
        print("\nStopping inbox bee...")
if __name__ == "__main__":
    watch()

