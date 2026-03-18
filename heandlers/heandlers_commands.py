from aiogram.filters import Command
from aiogram.types import Message
from services.vars import *
from aiogram.enums import ParseMode
from aiogram import Router

comm_router = Router()

@comm_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(text=START_MESSAGE, parse_mode=ParseMode.HTML)


@comm_router.message(Command("info"))
async def cmd_criteria(message: Message):
    await message.answer(text=INFO_MESSAGE, parse_mode=ParseMode.HTML)


@comm_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)