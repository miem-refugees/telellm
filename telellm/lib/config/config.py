from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("TOKEN")
MODEL_NAME = getenv("MODEL_NAME", "llama3.2")
CHAT_IDS = list(map(int, getenv("GROUP_IDS", "").split(",")))
USER_IDS = list(map(int, getenv("USER_IDS", "").split(",")))
OLLAMA_HOST = str(getenv("OLLAMA_HOST", "localhost"))
OLLAMA_PORT = int(getenv("OLLAMA_PORT", 11434))
REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))
