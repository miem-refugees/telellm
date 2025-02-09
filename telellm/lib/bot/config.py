from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("TOKEN")
MODEL_NAME = getenv("MODEL_NAME", "llama3.2")
CHAT_IDS = list(map(int, getenv("GROUP_IDS", "").split(",")))
USER_IDS = list(map(int, getenv("USER_IDS", "").split(",")))
OLLAMA_HOST = str(getenv("OLLAMA_HOST") or "localhost")
OLLAMA_PORT = int(getenv("OLLAMA_PORT") or 11434)
