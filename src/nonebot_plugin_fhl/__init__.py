from nonebot.plugin import PluginMetadata

__version__ = "0.1.0"

__plugin_meta__ = PluginMetadata(
    name="Fei Hua Ling",
    description="飞花令小游戏",
    usage="""
    /梦笔生花,
    /走马观花[5-9],
    /天女散花[13],
    /雾里看花[5-10],
""",
    type="application",
    homepage="",
    extra={"author": "qwerdvd"},
    supported_adapters={"~onebot.v11"},
)
