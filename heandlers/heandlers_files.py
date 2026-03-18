from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F
import tempfile

from services.connect_ai import ai_on
from services.result import format_result
from services.use_files import get_text_from_file
from config.config import bot, MAX_FILE_SIZE, MAX_TEXT_LENGTH
import os

from aiogram import Router

files_router = Router()


@files_router.message(F.document)
async def handle_document(message: Message):
    document = message.document

    if document.file_size > MAX_FILE_SIZE:
        await message.answer(f"❌ Файл слишком большой. Максимум {MAX_FILE_SIZE // 1024 // 1024} МБ")
        return

    file_name = document.file_name or ""
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext not in {'.txt', '.pdf', '.docx', '.doc'}:
        await message.answer("❌ Неподдерживаемый формат. Поддерживаются: txt, pdf, docx")
        return

    progress_msg = await message.answer(f"⏳ Скачиваю и анализирую файл {file_name}...")

    try:
        file = await bot.get_file(document.file_id)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_path = tmp_file.name

        await bot.download_file(file.file_path, tmp_path)
        await progress_msg.edit_text(f"📥 Файл загружен. Извлекаю текст...")

        text = await get_text_from_file(tmp_path, file_ext)
        os.unlink(tmp_path)

        if not text or len(text) < 100:
            await progress_msg.edit_text("❌ Не удалось извлечь текст из файла или текст слишком короткий.")
            return

        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]
            await message.answer(f"⚠️ Файл большой, анализирую первые {MAX_TEXT_LENGTH} символов.")

        await progress_msg.edit_text(f"✅ Текст извлечен ({len(text)} символов). Анализирую...")

        result = await ai_on(text)
        formatted = format_result(result)
        await progress_msg.edit_text(formatted, parse_mode=ParseMode.HTML)

    except Exception as e:
        await progress_msg.edit_text(f"❌ Ошибка: {e}")