from .config import Config
from .api import api


class FeiHuaLing:
    subject: str
    history: list[str]
    turn_timer: int

    def __init__(self, user_id: str, game_mode: str, poetry_size: int) -> None:
        self.api = Config.feihualing_api
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
        return resp
