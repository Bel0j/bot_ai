import asyncio
from aiogram import Dispatcher
from config.config import bot
from heandlers.heandlers_commands import comm_router
from heandlers.heandlers_files import files_router
from heandlers.heandlers_text import text_rout

dp = Dispatcher()

dp.include_router(comm_router)
dp.include_router(text_rout)
dp.include_router(files_router)




async def main():
    print("Работает")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())