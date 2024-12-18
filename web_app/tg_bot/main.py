import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from core.handlers.base_cmds import base_cmd_router
from core.handlers.dialog.start_dialog import msg_router
from core.handlers.dialog.photo_search import photos_router
from core.handlers.dialog.text_search import short_msg_router
from core.handlers.dialog.guide import guide_router
from core.database.models import async_main
from core.callbacks.callback import clbks_router


async def main():
    load_dotenv()

    await async_main()

    bot = Bot(token=os.getenv('TOKEN_BOT'))
    dp = Dispatcher()

    dp.include_routers(base_cmd_router, msg_router, photos_router, short_msg_router, guide_router, clbks_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
