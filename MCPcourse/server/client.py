import asyncio
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("OPEN_AI_API_KEY")

# Final validation
if not api_key:
    raise EnvironmentError("❌ OPEN_AI_API_KEY not set correctly! Please set it in your .env file.")

# Set it as an env variable (for any library that uses it internally)
os.environ["OPENAI_API_KEY"] = api_key

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    config_file = "server/weather.json"

    print("Initializing chat...")

    # Create MCP client and agent
    client = MCPClient.from_config_file(config_file)
    llm = ChatOpenAI(model="gpt-4o")

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,  # Built-in conversation memory
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
