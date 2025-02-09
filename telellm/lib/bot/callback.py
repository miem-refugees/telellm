from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .bot import bot, get_model_name
from .keyboard import settings_kb
from .ollama import llm

callback_router = Router()


@callback_router.callback_query(lambda query: query.data == "settings")
async def settings_callback_handler(query: CallbackQuery):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Choose the right option.",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=settings_kb.as_markup(),
    )


@callback_router.callback_query(lambda query: query.data == "switchllm")
async def switchllm_callback_handler(query: CallbackQuery):
    models = await llm.model_list()
    switchllm_builder = InlineKeyboardBuilder()
    for model in models:
        modelname = model["name"]
        modelfamilies = ""
        if model["details"]["families"]:
            modelicon = {"llama": "🦙", "clip": "📷"}
            try:
                modelfamilies = "".join(
                    [modelicon[family] for family in model["details"]["families"]]
                )
            except KeyError:
                modelfamilies = "✨"
        switchllm_builder.row(
            InlineKeyboardButton(
                text=f"{modelname} {modelfamilies}", callback_data=f"model_{modelname}"
            )
        )
    await query.message.edit_text(
        f"{len(models)} models available.\n🦙 = Regular\n🦙📷 = Multimodal",
        reply_markup=switchllm_builder.as_markup(),
    )


@callback_router.callback_query(lambda query: query.data.startswith("model_"))
async def model_callback_handler(query: CallbackQuery):
    global model_name
    model_name = query.data.split("model_")[1]
    await query.answer(f"Chosen model: {get_model_name()}")


@callback_router.callback_query(lambda query: query.data == "about")
async def about_callback_handler(query: CallbackQuery):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"<b>Telellm</b>\nCurrently using: <code>{get_model_name()}</code>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
