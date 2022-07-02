from aiogram import Dispatcher
from app.handlers.private import start, exchange, admin


def setup(dp: Dispatcher):
    exchange.setup(dp)
    start.setup(dp)
    admin.setup(dp)
