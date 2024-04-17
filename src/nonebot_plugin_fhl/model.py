from msgspec import Struct, field


class GetTopicRequest(Struct):
    """获取飞花令题目请求"""

    modtype: str
    """飞花令题目类型"""

    size: int
    """诗句长度"""

    id_: str = field(name="id")
    """标识"""


class GetTopicData(Struct):
    modtype: str
    """飞花令题目类型"""

    size: int
    """诗句长度"""

    subjectstring: str
    """题目"""

    id_: str = field(name="id")
    """标识"""


class GetTopicResponse(Struct):
    code: int
    message: str
    data: GetTopicData


class AnswerRequest(Struct):
    text: str
    """提交的答案"""

    id_: str = field(name="id")
    """标识"""


class AnswerData(Struct):
    modtype: str
    """飞花令题目类型"""

    size: int
    """诗句长度"""

    subjectstring: str
    """题目"""

    text: str
    """回答的语句"""

    update: str
    """特殊标识"""

    history: list[str]
    """历史正确回答"""

    user: int
    """用户"""

    reason: str
    """回答不合题意的原因"""

    id_: str = field(name="id")
    """标识"""


class AnswerResponse(Struct):
    code: int
    message: str
    data: AnswerData
