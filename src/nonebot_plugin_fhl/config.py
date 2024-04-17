from pydantic import BaseModel, Field


class Config(BaseModel):
    """Plugin Config Here"""

    feihualing_api: str = Field(default="106.54.63.95:8080")
    """飞花令api地址配置"""