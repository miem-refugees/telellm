import json

from aiohttp import ClientError, ClientSession, ClientResponseError, ClientTimeout
from loguru import logger

DEFAULT_TIMEOUT = 1 * 60  # 1 minute for generation


class Ollama:
    def __init__(self, host: str, port: int, gen_timeout=DEFAULT_TIMEOUT):
        self.api_url = f"http://{host}:{port}/api"
        self.generate_timeout = gen_timeout
        self.active_chats = {}

    async def pull(self, model_name: str) -> None:
        logger.info("pulling model: {}", model_name)

        async with ClientSession(timeout=ClientTimeout(10)) as session:
            data = json.dumps({"name": model_name})
            headers = {"Content-Type": "application/json"}

            async with session.post(
                f"{self.api_url}/pull", data=data, headers=headers
            ) as response:
                logger.info(f"pull model response status: {response.status}")
                response_text = await response.text()
                logger.info(f"pull model response text: {response_text}")

    async def model_list(self) -> list[str]:
        async with ClientSession(timeout=ClientTimeout(10)) as session:
            async with session.get(f"{self.api_url}/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    return data["models"]
                else:
                    return []

    async def generate(self, model_name: str, payload: dict):
        async with ClientSession(
            timeout=ClientTimeout(self.generate_timeout)
        ) as session:
            ollama_payload = {
                "model": model_name,
                "messages": payload.get("messages", []),
                "stream": payload.get("stream", True),
            }

            try:
                logger.debug(
                    "Sending request to Ollama: {}", ollama_payload.get("messages")
                )

                async with session.post(
                    f"{self.api_url}/chat", json=ollama_payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(
                            "ollama error: {} - {}", response.status, error_text
                        )
                        raise ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"API Error: {error_text}",
                        )

                    buffer = b""
                    async for chunk in response.content.iter_any():
                        buffer += chunk
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            line = line.strip()
                            if line:
                                try:
                                    yield json.loads(line)
                                except json.JSONDecodeError as e:
                                    logger.error(
                                        "ollama decode Error: {}, line: {}", e, line
                                    )

            except ClientError as e:
                logger.error("Client Error during request: {}", e)
                raise
