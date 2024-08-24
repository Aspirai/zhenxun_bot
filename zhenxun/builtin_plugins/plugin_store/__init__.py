from nonebot.permission import SUPERUSER # type: ignore
from nonebot.plugin import PluginMetadata # type: ignore
from nonebot_plugin_alconna import Alconna, Args, Subcommand, on_alconna # type: ignore
from nonebot_plugin_session import EventSession # type: ignore
from nonebot.exception import FinishedException  # type: ignore

from zhenxun.configs.utils import PluginExtraData  # type: ignore
from zhenxun.services.log import logger # type: ignore
from zhenxun.utils.enum import PluginType # type: ignore
from zhenxun.utils.message import MessageUtils # type: ignore

from .data_source import ShopManage

__plugin_meta__ = PluginMetadata(
    name="插件商店",
    description="插件商店",
    usage="""
    插件商店        : 查看当前的插件商店
    添加插件 id     : 添加插件
    移除插件 id     : 移除插件
    搜索插件 name or author     : 搜索插件
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)

_matcher = on_alconna(
    Alconna(
        "插件商店",
        Subcommand("add", Args["plugin_id", int]),
        Subcommand("remove", Args["plugin_id", int]),
        Subcommand("search", Args["plugin_name_or_author", str]),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_matcher.shortcut(
    r"添加插件",
    command="插件商店",
    arguments=["add", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    r"移除插件",
    command="插件商店",
    arguments=["remove", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    r"搜索插件",
    command="插件商店",
    arguments=["search", "{%0}"],
    prefix=True,
)


@_matcher.assign("$main")
async def _(session: EventSession):
    try:
        result = await ShopManage.get_plugins_info()
        logger.info("查看插件列表", "插件商店", session=session)
        await MessageUtils.build_message(result).finish()
    except FinishedException:
        pass
    except Exception as e:
        logger.error(f"查看插件列表失败 e: {e}", "插件商店", session=session, e=e)


@_matcher.assign("add")
async def _(session: EventSession, plugin_id: int):
    try:
        result = await ShopManage.add_plugin(plugin_id)
    except FinishedException:
        pass
    except Exception as e:
        logger.error(f"添加插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"添加插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"添加插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).finish()


@_matcher.assign("remove")
async def _(session: EventSession, plugin_id: int):
    try:
        result = await ShopManage.remove_plugin(plugin_id)
    except FinishedException:
        pass
    except Exception as e:
        logger.error(f"移除插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"移除插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"移除插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).finish()

@_matcher.assign("search")
async def _(session: EventSession, plugin_name_or_author: str):
    try:
        result = await ShopManage.search_plugin(plugin_name_or_author)
    except FinishedException:
        pass
    except Exception as e:
        logger.error(f"搜索插件 name: {plugin_name_or_author}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"搜索插件 name: {plugin_name_or_author} 失败 e: {e}"
        ).finish()
    logger.info(f"搜索插件 name: {plugin_name_or_author}", "插件商店", session=session)
    await MessageUtils.build_message(result).finish()
