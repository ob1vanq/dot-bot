from app.states.base import *


class ExchangeSG(StatesGroup):
    Amount = State()
    Email = State()
    Wallet = State()
    Tag = State()
    Show = State()