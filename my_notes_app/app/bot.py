from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
import aiohttp
from typing import Any, Dict

API_URL = "http://localhost:8000"  # URL FastAPI приложения
BOT_TOKEN = "your_bot_token"
YOUR_JWT_TOKEN = "your_jwt_token_here"  # Replace with actual JWT token or implement token retrieval logic

bot = Bot(token=BOT_TOKEN)
router = Router()

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для управления заметками. Используйте /notes для просмотра заметок.")

@router.message(Command("notes"))
async def list_notes(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/notes/", headers={"Authorization": f"Bearer {YOUR_JWT_TOKEN}"}) as response:
            if response.status == 200:
                notes: list[Dict[str, Any]] = await response.json()
                text = "\n".join([f"{hbold(note['title'])}: {note['content']}" for note in notes])
                await message.reply(f"Ваши заметки:\n{text}", parse_mode=ParseMode.HTML)
            else:
                await message.reply("Не удалось получить заметки. Пожалуйста, попробуйте позже.")

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())