import nonebot
from nonebot.adapters.console import Adapter as CONSOLEAdapter

from nonebot.adapters.onebot.v11 import Adapter as QQAdapter



nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(CONSOLEAdapter)
driver.register_adapter(QQAdapter)

# nonebot.load_plugins("chem-bot-plus/plugins")
nonebot.load_builtin_plugins("echo")
#nonebot.load_plugins("")

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
    