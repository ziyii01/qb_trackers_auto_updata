import asyncio
import datetime
import os

import httpx
from httpx import AsyncClient, Response
from loguru import logger as log

from const import PASSWORD, TRACKER_URL_LIST, USERNAME
from script.qb_web_api import Application, Authentication, Torrent, Torrent_management
from script.tracker import tasks


async def set_torrents_trackers(
    client: AsyncClient, add_trackers: list, torrents: list[Torrent]
):
    async def remove_trackers(
        client: AsyncClient, remove_trackers: list, torrent: Torrent
    ) -> Response:
        _remove_trackers = ""
        for _i in remove_trackers:
            if _i["url"] == "** [DHT] **":
                continue
            if _i["url"] == "** [PeX] **":
                continue
            if _i["url"] == "** [LSD] **":
                continue
            _remove_trackers += f"{_i['url']}|"
        _remove_trackers = _remove_trackers[:-1]
        return await Torrent_management.removeTrackers(
            client=client, trackers=_remove_trackers, torrent=torrent
        )

    for i in torrents:
        a = await Torrent_management.trackers(client, i)
        await remove_trackers(client, a, i)
        await Torrent_management.add_trackers(client, "\n\n".join(add_trackers), i)
        log.info(f"{i.name}的tracker已更改")


def today_date():
    """获取今日日期,返回%Y-%m-%d格式的日期"""
    return datetime.datetime.today().strftime("%Y-%m-%d")


async def main() -> None:
    # 判断文件夹是否存在
    if os.path.isdir(f"./data/{today_date()}"):
        log.info("今日tracker验证已执行")
        with open(f"./data/{today_date()}/tracker_urls_list.txt") as f:
            _tracker_urls_list = f.read().split("\n\n")
    else:
        os.mkdir(f"./data/{today_date()}")
        _tracker_urls_list = await tasks()  # 获取验证之后的tracker列表
        with open(f"./data/{today_date()}/tracker_urls_list.txt", "w") as f:
            f.write("\n\n".join(_tracker_urls_list))
    async with httpx.AsyncClient(timeout=httpx.Timeout(50.0), verify=False) as client:
        log.debug("开始登录")
        await Authentication.login(client=client, username=USERNAME, password=PASSWORD)
        _str = r"\n\n"
        log.debug(f"Tracker urls: {_str.join(_tracker_urls_list)}")
        await Application.set_preferences(
            client, f'{{"add_trackers": "{_str.join(_tracker_urls_list)}"}}'
        )
        log.info("qb默认添加的tracker已更改")
        log.info("正在下载的种子修改tracker")
        downloading_torrents = await Torrent_management.info(client, "downloading")
        await set_torrents_trackers(client, _tracker_urls_list, downloading_torrents)
        log.info("正在做种的种子修改tracker")
        seeding_torrents = await Torrent_management.info(client, "seeding")
        await set_torrents_trackers(client, TRACKER_URL_LIST, seeding_torrents)


if __name__ == "__main__":
    asyncio.run(main())
