import json
import redis
import asyncio

from loguru import logger

from telellm.lib.ollama.ollama import Ollama
from telellm.lib.config import OLLAMA_HOST, OLLAMA_PORT
from telellm.lib.redis import TASK_QUEUE, STATUS_KEY_PREFIX


async def process_tasks():
    ollama = Ollama(OLLAMA_HOST, OLLAMA_PORT)
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        _, task_data = redis_client.blpop(TASK_QUEUE)  # Блокирующее чтение из очереди
        task = json.loads(task_data)
        logger.info(f"Received task: {task}")

        task_id = task["task_id"]
        prompt = task["prompt"]

        redis_client.set(STATUS_KEY_PREFIX + task_id, "processing")

        try:
            response = ""
            async for chunk in ollama.generate(
                "llama3.2", {"messages": [{"role": "user", "content": prompt}]}
            ):
                msg = chunk.get("message")
                if msg:
                    response += msg.get("content", "")

            logger.info(f"Received response: {task_id}")
            redis_client.set(
                STATUS_KEY_PREFIX + task_id, response
            )  # Сохраняем результат
        except Exception as e:
            logger.error(e)

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(process_tasks())
