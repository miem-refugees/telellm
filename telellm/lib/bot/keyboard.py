from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_kb = InlineKeyboardBuilder()
settings_kb = InlineKeyboardBuilder()

start_kb.row(
    InlineKeyboardButton(text="ℹ️ About", callback_data="about"),
    InlineKeyboardButton(text="⚙️ Settings", callback_data="settings"),
)
settings_kb.row(
    InlineKeyboardButton(text="🔄 Switch LLM", callback_data="switchllm"),
)
