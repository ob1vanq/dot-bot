import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import AllowedUpdates, ParseMode

from app import filters, handlers, middlewares
from app.config import Config
from app.misc.set_bot_commands import set_default_commands
from app.misc.notify_admins import on_startup_notify


log = logging.getLogger(__name__)


async def main():
    config = Config.from_env()
    logging.basicConfig(
        level=config.misc.log_level,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    log.info('Starting bot...')

    loop = asyncio.get_event_loop()
    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML, loop=loop)
    dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)

    allowed_updates = AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY + AllowedUpdates.EDITED_MESSAGE
    environments = dict(config=config)

    filters.setup(dp)
    handlers.setup(dp)

    await set_default_commands(bot)
    await on_startup_notify(bot, config.bot.admin_ids)

    try:
        await dp.skip_updates()
        await dp.start_polling(allowed_updates=allowed_updates, reset_webhook=True)
    finally:
        await (await bot.get_session()).close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Bot stopped!')
