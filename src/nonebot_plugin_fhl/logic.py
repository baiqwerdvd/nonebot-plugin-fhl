from typing import List
from .config import config
from .api import api


class FeiHuaLing:
    subject: str
    history: List[str]
    turn_timer: int

    def __init__(self, user_id: str, game_mode: str, poetry_size: int) -> None:
        self.api = config.feihualing_api
        self.game_id = user_id
        self.game_mode = game_mode
        self.poetry_size = poetry_size

    async def init_game(self):
        resp = await api.get_topic(
            self.game_mode,
            self.poetry_size,
            self.game_id,
        )
        self.subject = resp.data.subjectstring
        return self.subject

    async def answer(self, answer: str):
        resp = await api.answer(
            self.game_id,
            answer,
        )
        self.history = resp.data.history
        return resp
