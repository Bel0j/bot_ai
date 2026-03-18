from aiogram import F
from aiogram.types import Message
from aiogram.enums import ParseMode

from services.connect_ai import ai_on
from services.result import format_result
from config.config import bot, MAX_TEXT_LENGTH

from aiogram import Router

text_rout = Router()

@text_rout.message(F.text)
async def handle_text(message: Message):
    text = message.text

    if text.startswith('/'):
        return

    if len(text) < 100:
        await message.answer("❌ Текст слишком короткий. Минимум 100 символов.")
        return

    if len(text) > MAX_TEXT_LENGTH:
        await message.answer(f"❌ Текст слишком длинный. Максимум {MAX_TEXT_LENGTH} символов.")
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    progress_msg = await message.answer("⏳ Анализирую работу через нейросеть... Это займет 10-30 секунд.")

    try:
        result = await ai_on(text)
        formated = format_result(result)
        await progress_msg.edit_text(formated, parse_mode=ParseMode.HTML)
    except Exception as e:
        await progress_msg.edit_text(f"❌ Произошла ошибка: {e}")