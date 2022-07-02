import logging
from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: tuple[int, ...]


@dataclass
class Miscellaneous:
    log_level: int


@dataclass
class Currency:
    DOT_rate: float
    DOGE_rate: float
    DOT_reserve: float
    DOGE_reserve: float
    wallet_address: str


@dataclass
class Config:
    bot: TgBot
    misc: Miscellaneous
    curr: Currency

    @classmethod
    def from_env(cls, path: Union[str, None] = None) -> 'Config':
        env = Env()
        env.read_env(path)

        return Config(
            bot=TgBot(
                token=env.str('BOT_TOKEN'),
                admin_ids=tuple(map(int, env.list('ADMIN_IDS')))
            ),
            misc=Miscellaneous(
                log_level=env.log_level('LOG_LEVEL', logging.INFO)
            ),
            curr=Currency(
                DOT_rate=round(env.float('DOT_RATE'), 8),
                DOGE_rate=round(float(1/env.float('DOT_RATE')), 8),
                DOT_reserve=env.float('DOGE_RESERVE'),
                DOGE_reserve=env.float('DOGE_RESERVE'),
                wallet_address=env.str('WALLET_ADDRESS')
            )

        )
