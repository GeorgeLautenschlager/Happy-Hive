import sys
import time
import hashlib
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4:e4b"
INBOX_PATH = Path.home() / "gtd" / "inbox.md"
SKILLS_DIR = Path(__file__).parent.parent / "skills"

@tool
def placeholder_tool(query: str) -> str:
    """A placeholder tool. Replace with real tools."""
    return f"Result for: {query}"

# llm = ChatOllama(model=MODEL, base_url=OLLAMA_BASE_URL, num_ctx=32768)
llm = ChatOpenAI(
    model="gemma-4-26b-a4b-it",  # must match what's loaded in LM Studio
    base_url="http://100.126.84.49:1234/v1",
    api_key="lm-studio",  # arbitrary, LM Studio ignores it
)

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
        "Then process each line item individually, top to bottom, using the following rules:\n\n"
        "1. If the item already has a ❓ annotation, skip it — it is awaiting clarification.\n"
        "2. If the item is already struck through (~~text~~), skip it — it has been organized.\n"
        "3. If the item has enough information to make an organize decision (even a rough one), "
        "apply the organize skill immediately. You do NOT need to fully understand the item — "
        "you only need enough to route it. 'fix bathroom fan' is sufficient to route to a home "
        "maintenance project or loose-actions.md. Make the call.\n"
        "4. If the item is genuinely ambiguous about its *destination* (not its details), "
        "apply the clarify skill: annotate it with a single question and move on. "
        "Do NOT ask the user anything interactively. Write the question into the file and skip the item.\n\n"
        "IMPORTANT: Do not ask the user any questions at any point. "
        "Make all routing decisions autonomously based on the item text. "
        "When in doubt, pick the most reasonable destination and route it.\n\n"
        f"Write all changes back to \"{INBOX_PATH}\" using the write_file tool."
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

