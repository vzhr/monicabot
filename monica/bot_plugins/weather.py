from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command

from monica.services.common import ServiceException
from monica.services.weather import get_current_weather_short

__plugin_name__ = '天气'
__plugin_usage__ = '用法：对我说 "天气 苏州" '

# 表示 “不是私聊” 或 “超级用户” 可以触发此命令
weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuse


@on_command('weather', aliases=('气温', '天气'), permission=weather_permission)
async def _(session: CommandSession):
    # 尝试从用户提供的信息中提取参数，如果没有参数，则主动询问
    city = session.current_arg_text.strip()
    if not city:
        city = await session.aget(prompt='请问是哪个城市呢？', at_sender=True)

    # 在这里调用 weather service，获取结果
    try:
        result = await get_current_weather_short(city)
    except ServiceException as e:
        result = e.message

    await session.send(result)
