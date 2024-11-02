"Главный файл запуска бота"
import asyncio

from aiogram import Bot, Dispatcher
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

from commands import commands_router

async def main():
    dp.include_router(commands_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
