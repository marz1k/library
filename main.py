import asyncio
import logging
from aiogram import types
from handlers.handlers import dp, db

logger = logging.getLogger(__name__)


async def main():
    await db.create_db()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    await dp.skip_updates()
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запуск бота")])

    await dp.start_polling(dp)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)