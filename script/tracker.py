import asyncio

import httpx
from loguru import logger as log

from BitTorrent_Tracker_Checker import check_tracker_url
from const import (
    RETRY_TIMES,
    SEMAPHORE_THREAD_HOLD,
    TRACKER_URL_LIST,
    TRACKER_URLS_LIST,
)


def retry(func):
    async def _wrapper(*args, **kwargs):
        _result_list = list()
        for i in range(RETRY_TIMES):
            log.info(f"{args[1]}正在尝试第{i + 1}次")
            _result = await func(*args, **kwargs)
            if len(_result) != 0:
                # 其中有一次成功则立刻跳出循环
                log.info(f"{args[1]}第{i + 1}次尝试成功")
                return _result
            else:
                log.info(f"{args[1]}第{i + 1}次尝试失败")
                _result_list.append(_result)
        return _result_list

    return _wrapper


async def get_trackers():
    @retry
    async def get_tracker_url(client, url: str):
        _trackers_set = list()
        try:
            _get_raw_data = await client.get(url)
        except Exception as e:
            log.error(f"网络访问错误:{url}\n错误内容:{e}")
            return _trackers_set
        if _get_raw_data.status_code == 200:
            for i in _get_raw_data.text.splitlines():
                if i == "":
                    continue
                _trackers_set.append(i)
        else:
            log.error(f"网络访问错误:{url}\n错误代码:{_get_raw_data.status_code}")
        return _trackers_set

    async with httpx.AsyncClient(timeout=httpx.Timeout(50.0), verify=False) as client:
        tasks = [
            asyncio.create_task(get_tracker_url(client, i)) for i in TRACKER_URLS_LIST
        ]
        done, task = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        _trackers_set = set()
        for i in done:
            _trackers_set.update(i.result())
    log.debug(f"获取到的tracker: {_trackers_set}")
    return _trackers_set


async def tasks():
    _tasks_set = set()  # 存储当前正在运行的任务
    _success_list: list[str] = []  # 存储成功验证的tracker
    _trackers: set[str] = await get_trackers()  # 获取tracker列表
    _return_list = []
    for i in range(SEMAPHORE_THREAD_HOLD):
        if len(_trackers) == 0:
            break
        _temp = _trackers.pop()
        _tasks_set.add(asyncio.create_task(check_tracker_url(_temp), name=_temp))
    log.debug(f"初始任务: {_tasks_set}")
    while _tasks_set:
        done, _tasks_set = await asyncio.wait(
            _tasks_set, return_when=asyncio.FIRST_COMPLETED
        )
        for task in done:
            if task.result() is None:
                _success_list.append(task.get_name())
                log.info(f"Tracker验证成功:{task.get_name()}")
            else:
                log.info(f"Tracker验证失败:{task.get_name()}\n原因:{task.result()}")
            if len(_trackers) == 0:
                log.debug("任务完成, 无空余任务")
                continue
            _temp = _trackers.pop()
            new_task = asyncio.create_task(check_tracker_url(_temp), name=_temp)
            _tasks_set.add(new_task)  # 添加新任务到集合
            log.debug(f"添加新任务: {new_task}")
        _tasks_set -= done  # 从集合中移除已完成的任务
        log.debug(f"剩余任务: {len(_tasks_set)}, 已完成任务: {done}")
    for i in TRACKER_URL_LIST:
        _return_list.append(i)
    for i in _success_list:
        _return_list.append(i)
    return _return_list
