import traceback

from aiogram.enums import ParseMode
from aiogram.types import Message
from loguru import logger

from .bot import bot, get_model_name
from .config import OLLAMA_HOST, OLLAMA_PORT

from telellm.lib.ollama import Ollama
from .history.in_memory import INMemoryContext

llm = Ollama(OLLAMA_HOST, OLLAMA_PORT)
memory = INMemoryContext()


async def save_user_request(message: Message, prompt: str):
    context = memory.get(message)
    if context is None:
        context = {
            "model": get_model_name(),
            "messages": [],
        }

    context["messages"].append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    await memory.set(message, context)
    return context


async def ollama_request(message: Message, prompt: str):
    try:
        full_response = ""
        await bot.send_chat_action(message.chat.id, "typing")

        payload = await save_user_request(message, prompt)

        logger.info(
            "[Request] '{}' for {}",
            prompt,
            message.from_user.full_name,
        )

        async for response_data in llm.generate(get_model_name(), payload):
            msg = response_data.get("message")
            if msg is None:
                continue
            chunk = msg.get("content", "")
            full_response += chunk

            if any([c in chunk for c in ".\n!?"]) or response_data.get("done"):
                if await handle_response(message, response_data, full_response):
                    break

    except Exception as e:
        logger.error("Exception: {}", traceback.format_exc())
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Something went wrong: {str(e)}",
            parse_mode=ParseMode.HTML,
        )


async def handle_response(message: Message, response_data, full_response):
    full_response_stripped = full_response.strip()
    if full_response_stripped == "":
        return
    if response_data.get("done"):
        text = (
            f"{full_response_stripped}⚙️\n\n"
            f"{get_model_name()}\n"
            f"Generated in {response_data.get('total_duration') / 1e9:.2f}s."
        )
        await send_response(message, text)

        await memory.append_context(
            message,
            {
                "role": "assistant",
                "content": full_response_stripped,
            },
        )

        logger.info(
            f"[Response]: '{full_response_stripped}' for {message.from_user.first_name} {message.from_user.last_name}"
        )
        return True
    return False


async def send_response(message: Message, text: str):
    if message.chat.id < 0 or message.chat.id == message.from_user.id:
        await bot.send_message(
            chat_id=message.chat.id, text=text, parse_mode=ParseMode.MARKDOWN
        )
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
        )
