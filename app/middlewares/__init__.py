import logging
from aiogram import Dispatcher

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    log.info('Handlers are successfully configured')