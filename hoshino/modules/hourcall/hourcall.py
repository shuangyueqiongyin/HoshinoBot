import os
import pytz
from datetime import datetime
import hoshino
from hoshino import Service, R, config

sv = Service('hourcall', enable_on_default=False, help_='时报')
tz = pytz.timezone('Asia/Shanghai')


def get_hour_call():
    """挑出一组时报，每日更换，一日之内保持相同"""
    cfg = hoshino.config.hourcall
    now = datetime.now(tz)
    hc_groups = cfg.HOUR_CALLS_ON
    g = hc_groups[now.day % len(hc_groups)]
    return cfg.HOUR_CALLS[g], g


@sv.scheduled_job('cron', hour='*')
async def hour_call():
    now = datetime.now(tz)
    if 2 <= now.hour <= 4:
        return  # 宵禁 免打扰
    hc, g = get_hour_call()
    msg = hc[now.hour]
    if os.path.exists(os.path.join(config.__bot__.RES_DIR, 'rec', g)):
        recfile = f'{g}/{now.hour}.mp3'
        await sv.broadcast(R.rec(recfile).cqcode, 'hourcall', 0.1)
    await sv.broadcast(msg, 'hourcall', 0)
