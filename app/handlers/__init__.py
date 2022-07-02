import logging
from aiogram import Dispatcher
from app.handlers.private import start, exchange, admin

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    log.info('Handlers are successfully configured')
    exchange.setup(dp)
    start.setup(dp)
    admin.setup(dp)

