from aiogram import types, Bot
import logging


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand("start", "[Re]Start bot"),
            types.BotCommand("admin", "Admin panel")
        ]
    )
    logging.info("Установка комманд прошла успешно")

