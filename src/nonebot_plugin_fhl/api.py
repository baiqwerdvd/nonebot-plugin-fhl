import httpx
from msgspec import convert

from .config import config
from .model import (
    GetTopicRequest,
    GetTopicResponse,
    AnswerRequest,
    AnswerResponse,
)


class FHLApi:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(base_url=config.feihualing_api)

    async def get_topic(
        self,
        game_mode: str,
        poetry_size: int,
        game_id: str,
    ) -> GetTopicResponse:
        data = GetTopicRequest(
            modtype=game_mode,
            size=poetry_size,
            id_=game_id,
        )
        response = await self.client.post(
            "/gettopic",
            json=data,
        )
        return convert(response.json(), GetTopicResponse)

    async def answer(
        self,
        game_id: str,
        answer: str,
    ):
        data = AnswerRequest(
            id_=game_id,
            text=answer,
        )
        response = await self.client.post(
            "/answer",
            json=data,
        )
        return convert(response.json(), AnswerResponse)


api = FHLApi()
