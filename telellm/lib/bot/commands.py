from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

from telellm.lib.redis import redis_client, STATUS_KEY_PREFIX
from .auth import auth
from .bot import bot
from .keyboard import start_kb
from .ollama import memory

commands = [
    BotCommand(command="start", description="Start"),
    BotCommand(command="reset", description="Reset Chat"),
    BotCommand(command="history", description="Look through messages"),
    BotCommand(command="pullmodel", description="Pull a model from Ollama"),
]

command_router = Router()


async def update_bot_commands():
    await bot.set_my_commands(commands)


@command_router.message(CommandStart())
@auth
async def command_start(message: Message):
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}!</b> 🦙",
        parse_mode=ParseMode.HTML,
        reply_markup=start_kb.as_markup(),
        disable_web_page_preview=True,
    )


@command_router.message(Command("reset"))
@auth
async def command_reset(message: Message):
    memory.reset(message)
    await message.answer("Cleared context 🧹")


@command_router.message(Command("history"))
@auth
async def command_history(message: Message):
    messages = memory.get(message, {}).get("messages")
    if not messages:
        await message.answer("No history 📭")

    context = ""
    for msg in messages:
        context += f"*{msg['role'].capitalize()}*: {msg['content']}\n"

    await bot.send_message(
        chat_id=message.chat.id,
        text=context,
        parse_mode=ParseMode.MARKDOWN,
    )


@command_router.message(Command("status"))
@auth
async def status_command(message: Message):
    """Позволяет пользователю узнать статус своей задачи"""
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Использование: /status <task_id>")
        return

    task_id = args[1]
    result = redis_client.get(f"{STATUS_KEY_PREFIX}{task_id}")

    if result:
        await message.reply(f"📢 Ответ:\n\n{result.decode()}")
        redis_client.delete(task_id)  # Удаляем после отправки
    else:
        await message.reply("⏳ Ваша задача все еще в обработке или не найдена.")
