import asyncio

import httpx
from loguru import logger as log

from const import PASSWORD, USERNAME
from script.qb_web_api import Application, Authentication, Torrent_management
from script.tracker import tasks


async def main() -> None:
    _tracker_urls_list = await tasks()  # 获取验证之后的tracker列表
    async with httpx.AsyncClient(timeout=httpx.Timeout(50.0), verify=False) as client:
        await Authentication.login(client=client, username=USERNAME, password=PASSWORD)
        _str = r"\n\n"
        log.debug(f"Tracker urls: {_str.join(_tracker_urls_list)}")
        await Application.set_preferences(
            client, f'{{"add_trackers": "{_str.join(_tracker_urls_list)}"}}'
        )
        log.info("qb默认添加的tracker已更改")
        torrents = await Torrent_management.info(client)
        for i in torrents:
            a = await Torrent_management.trackers(client, i)
            _i = ""
            for __i in a:
                if __i["url"] == "** [DHT] **":
                    continue
                if __i["url"] == "** [PeX] **":
                    continue
                if __i["url"] == "** [LSD] **":
                    continue
                _i += f"{__i['url']}|"
            _i = _i[:-1]
            await Torrent_management.removeTrackers(client, _i, i)
            await Torrent_management.add_trackers(
                client, "\n\n".join(_tracker_urls_list), i
            )
            log.info(f"{i.name}的tracker已更改")


if __name__ == "__main__":
    asyncio.run(main())
