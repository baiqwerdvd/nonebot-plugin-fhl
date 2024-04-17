import asyncio
from typing import Any, Dict, Optional, Type
from asyncio import TimerHandle
from typing_extensions import Annotated

from nonebot import on_regex, require
from nonebot.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.rule import to_me

require("nonebot_plugin_alconna")
require("nonebot_plugin_session")

from nonebot_plugin_alconna import (
    Alconna,
    UniMessage,
    on_alconna,
)

from nonebot_plugin_session import SessionId, SessionIdType

from .logic import FeiHuaLing
from .config import Config

__version__ = "1.0.0"

__plugin_meta__ = PluginMetadata(
    name="Fei Hua Ling",
    description="飞花令小游戏",
    usage="""
    /梦笔生花,
    [WIP] /走马观花[5-9] [WIP]
    [WIP] /天女散花[13] [WIP]
    [WIP] /雾里看花[5-10] [WIP]
""",
    type="application",
    homepage="https://github.com/baiqwerdvd/nonebot-plugin-fhl",
    config=Config,
    extra={"author": "baiqwerdvd", "example": "/梦笔生花"},
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_session"
    ),
)

games: Dict[str, FeiHuaLing] = {}
timers: Dict[str, TimerHandle] = {}

UserId = Annotated[str, SessionId(SessionIdType.GROUP)]


def game_is_running(user_id: UserId) -> bool:
    return user_id in games


def game_not_running(user_id: UserId) -> bool:
    return user_id not in games


fhl_mode_1 = on_alconna(
    Alconna("梦笔生花"),
    rule=to_me() & game_not_running,
    use_cmd_start=True,
    block=True,
    priority=13,
)
# fhl_mode_2 = on_alconna(
#     Alconna(
#         "走马观花",
#         Option("-l|--length", Args["length", int], help_text="诗句长度"),
#     ),
#     rule=to_me() & game_not_running,
#     use_cmd_start=True,
#     block=True,
#     priority=13,
# )
# fhl_mode_3 = on_alconna(
#     Alconna(
#         "天女散花",
#         Option("-l|--length", Args["length", int], help_text="诗句长度"),
#     ),
#     rule=to_me() & game_not_running,
#     use_cmd_start=True,
#     block=True,
#     priority=13,
# )
# fhl_mode_4 = on_alconna(
#     Alconna(
#         "雾里看花",
#         Option("-l|--length", Args["length", int], help_text="诗句长度"),
#     ),
#     rule=to_me() & game_not_running,
#     use_cmd_start=True,
#     block=True,
#     priority=13,
# )
fhl_stop = on_alconna(
    "结束飞花令",
    rule=game_is_running,
    use_cmd_start=True,
    block=True,
    priority=13,
)
poery_word: Optional[Type[Matcher]] = None


def stop_game(user_id: str):
    if timer := timers.pop(user_id, None):
        timer.cancel()
    games.pop(user_id, None)
    if poery_word:
        poery_word.destroy()


async def stop_game_timeout(matcher: Matcher, user_id: str):
    game = games.get(user_id, None)
    stop_game(user_id)
    if game:
        msg = "猜单词超时，游戏结束"
        if len(game.history) >= 1:
            msg += f"\n{game.history}"
        await matcher.send(msg)


def set_timeout(matcher: Matcher, user_id: str, timeout: float = 300):
    if timer := timers.get(user_id, None):
        timer.cancel()
    loop = asyncio.get_running_loop()
    timer = loop.call_later(
        timeout, lambda: asyncio.ensure_future(stop_game_timeout(matcher, user_id))
    )
    timers[user_id] = timer


@fhl_mode_1.handle()
async def fhl_1(
    matcher: Matcher,
    user_id: UserId,
):
    game_instance = FeiHuaLing(user_id, "A", 0)
    await game_instance.init_game()

    games[user_id] = game_instance
    set_timeout(matcher, user_id)
    global poery_word
    poery_word = on_regex(
        r"(?P<poetry>[\u4e00-\u9fa5]+)",
        rule=to_me() & game_is_running,
        block=True,
        priority=14,
    )
    poery_word.append_handler(handle_poery)

    msg = f"题目：{game_instance.subject}"
    await UniMessage.text(msg).send()


@fhl_stop.handle()
async def _(matcher: Matcher, user_id: UserId):
    game = games[user_id]
    stop_game(user_id)

    msg = "游戏已结束" + "\n"
    if len(game.history) >= 1:
        for i in game.history:
            msg += "\n" + i
    await matcher.finish(msg)


async def handle_poery(
    matcher: Matcher, user_id: UserId, matched: Dict[str, Any] = RegexDict()
):
    game = games[user_id]
    set_timeout(matcher, user_id)

    poetry = str(matched["poetry"])
    result = await game.answer(poetry)
    code = result.code

    if len(result.data.history) > 10:
        stop_game(user_id)
        msg = "已经答出10句, 本局游戏结束\n"
        if len(game.history) >= 1:
            for i in game.history:
                msg += "\n" + i
        await matcher.finish(msg)

    if code == 200:
        tup = ""
        if result.data.reason != "":
            tup = f"\nUpdate: {result.data.update}"
        history = ""
        for i in result.data.history:
            history += i + "\n"
        msg = f"题目: {result.data.subjectstring}\n历史:\n{history}{tup}"
        await UniMessage.text(msg).send()
    elif code == 201:
        # 不切题
        msg = f"不切题: {result.data.reason}"
        await UniMessage.text(msg).send()
    elif code == 202:
        # game finish
        stop_game(user_id)
        msg = f"游戏结束\n{user_id}获胜\n{result.data.history}"
        await UniMessage.text(msg).send()
    elif code == 203:
        pass
    else:
        pass
