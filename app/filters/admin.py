from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from app.config import Config


class AdminFilter(BoundFilter):
    async def check(self, msg: Message):
        return msg.from_user.id in Config.from_env().bot.admin_ids