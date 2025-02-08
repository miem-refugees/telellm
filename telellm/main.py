import os
import asyncio

from dotenv import load_dotenv

from bot import TelegramBot
from logger import init_logger


async def main():
    load_dotenv()
    init_logger()

    token = os.getenv("TOKEN")
    if token is None:
        raise RuntimeError("TOKEN is not set")

    bot = TelegramBot(token)

    await bot.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
