from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.permission import SUPERUSER,Permission
from nonebot import on_message, on_notice, on_type,on_keyword
from nonebot.rule import keyword
from nonebot.adapters.onebot.v11 import (
	Message,
	MessageEvent,
	MessageSegment,
	Bot,
	Event,
	NoticeEvent,
	NotifyEvent,
	PokeNotifyEvent,
	GroupMessageEvent,
	PrivateMessageEvent,
	escape,
	unescape,
)
import re, random

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="mine_sweeper",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

startgamehandle=on_message(keyword("kaishi"),priority=1)