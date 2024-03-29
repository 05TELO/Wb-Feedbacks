from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class BotConfig:
    token: str
    chat_id: int
    path: str
    resp_time: int


@dataclass
class Config:
    bot: BotConfig


def load_config(path: Optional[str]) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env.str("BOT_TOKEN"),
            chat_id=env.int("CHAT_ID"),
            path=env.str("FILE_PATH"),
            resp_time=env.int("RESP_TIME"),
        )
    )
