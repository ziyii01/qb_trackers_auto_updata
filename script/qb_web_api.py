from httpx import AsyncClient, Response

from const import URL_ROOT


class Torrent:
    """Torrent 类，用于存储 torrent 信息"""

    def __init__(
        self,
        added_on,
        amount_left,
        auto_tmm,
        availability,
        category,
        comment,
        completed,
        completion_on,
        content_path,
        dl_limit,
        dlspeed,
        download_path,
        downloaded,
        downloaded_session,
        eta,
        f_l_piece_prio,
        force_start,
        has_metadata,
        hash,
        inactive_seeding_time_limit,
        infohash_v1,
        infohash_v2,
        last_activity,
        magnet_uri,
        max_inactive_seeding_time,
        max_ratio,
        max_seeding_time,
        name,
        num_complete,
        num_incomplete,
        num_leechs,
        num_seeds,
        popularity,
        priority,
        private,
        progress,
        ratio,
        ratio_limit,
        reannounce,
        root_path,
        save_path,
        seeding_time,
        seeding_time_limit,
        seen_complete,
        seq_dl,
        size,
        state,
        super_seeding,
        tags,
        time_active,
        total_size,
        tracker,
        trackers_count,
        up_limit,
        uploaded,
        uploaded_session,
        upspeed,
    ):
        self.added_on = added_on
        self.amount_left = amount_left
        self.auto_tmm = auto_tmm
        self.availability = availability
        self.category = category
        self.comment = comment
        self.completed = completed
        self.completion_on = completion_on
        self.content_path = content_path
        self.dl_limit = dl_limit
        self.dlspeed = dlspeed
        self.download_path = download_path
        self.downloaded = downloaded
        self.downloaded_session = downloaded_session
        self.eta = eta
        self.f_l_piece_prio = f_l_piece_prio
        self.force_start = force_start
        self.has_metadata = has_metadata
        self.hash = hash
        self.inactive_seeding_time_limit = inactive_seeding_time_limit
        self.infohash_v1 = infohash_v1
        self.infohash_v2 = infohash_v2
        self.last_activity = last_activity
        self.magnet_uri = magnet_uri
        self.max_inactive_seeding_time = max_inactive_seeding_time
        self.max_ratio = max_ratio
        self.max_seeding_time = max_seeding_time
        self.name = name
        self.num_complete = num_complete
        self.num_incomplete = num_incomplete
        self.num_leechs = num_leechs
        self.num_seeds = num_seeds
        self.popularity = popularity
        self.priority = priority
        self.private = private
        self.progress = progress
        self.ratio = ratio
        self.ratio_limit = ratio_limit
        self.reannounce = reannounce
        self.root_path = root_path
        self.save_path = save_path
        self.seeding_time = seeding_time
        self.seeding_time_limit = seeding_time_limit
        self.seen_complete = seen_complete
        self.seq_dl = seq_dl
        self.size = size
        self.state = state
        self.super_seeding = super_seeding
        self.tags = tags
        self.time_active = time_active
        self.total_size = total_size
        self.tracker = tracker
        self.trackers_count = trackers_count
        self.up_limit = up_limit
        self.uploaded = uploaded
        self.uploaded_session = uploaded_session
        self.upspeed = upspeed


async def post_data(client: AsyncClient, data: dict, api: str) -> Response:
    """qb api post访问"""
    _response: Response = await client.post(
        URL_ROOT + api, data=data, headers={"Referer": f"{URL_ROOT}"}
    )
    return _response


class Authentication:
    @staticmethod
    async def login(client: AsyncClient, username: str, password: str) -> Response:
        """Qb 登录接口"""
        return await post_data(
            client=client,
            data={"username": username, "password": password},
            api="/api/v2/auth/login",
        )


class Application:
    @staticmethod
    async def set_preferences(client: AsyncClient, data: str) -> Response:
        """Qb 设置接口"""
        return await post_data(
            client=client,
            data={"json": data},
            api="/api/v2/app/setPreferences",
        )


class Torrent_management:
    @staticmethod
    async def info(client: AsyncClient) -> list[Torrent]:
        """Qb 获取种子信息接口 返回实例化后的种子列表"""
        _torrent_list: list[Torrent] = []
        _response: Response = await post_data(
            client=client,
            data={},
            api="/api/v2/torrents/info",
        )
        for _i in _response.json():
            _torrent_list.append(
                Torrent(
                    added_on=_i["added_on"],
                    amount_left=_i["amount_left"],
                    auto_tmm=_i["auto_tmm"],
                    availability=_i["availability"],
                    category=_i["category"],
                    comment=_i["comment"],
                    completed=_i["completed"],
                    completion_on=_i["completion_on"],
                    content_path=_i["content_path"],
                    dl_limit=_i["dl_limit"],
                    dlspeed=_i["dlspeed"],
                    download_path=_i["download_path"],
                    downloaded=_i["downloaded"],
                    downloaded_session=_i["downloaded_session"],
                    eta=_i["eta"],
                    f_l_piece_prio=_i["f_l_piece_prio"],
                    force_start=_i["force_start"],
                    has_metadata=_i["has_metadata"],
                    hash=_i["hash"],
                    inactive_seeding_time_limit=_i["inactive_seeding_time_limit"],
                    infohash_v1=_i["infohash_v1"],
                    infohash_v2=_i["infohash_v2"],
                    last_activity=_i["last_activity"],
                    magnet_uri=_i["magnet_uri"],
                    max_inactive_seeding_time=_i["max_inactive_seeding_time"],
                    max_ratio=_i["max_ratio"],
                    max_seeding_time=_i["max_seeding_time"],
                    name=_i["name"],
                    num_complete=_i["num_complete"],
                    num_incomplete=_i["num_incomplete"],
                    num_leechs=_i["num_leechs"],
                    num_seeds=_i["num_seeds"],
                    popularity=_i["popularity"],
                    priority=_i["priority"],
                    private=_i["private"],
                    progress=_i["progress"],
                    ratio=_i["ratio"],
                    ratio_limit=_i["ratio_limit"],
                    reannounce=_i["reannounce"],
                    root_path=_i["root_path"],
                    save_path=_i["save_path"],
                    seeding_time=_i["seeding_time"],
                    seeding_time_limit=_i["seeding_time_limit"],
                    seen_complete=_i["seen_complete"],
                    seq_dl=_i["seq_dl"],
                    size=_i["size"],
                    state=_i["state"],
                    super_seeding=_i["super_seeding"],
                    tags=_i["tags"],
                    time_active=_i["time_active"],
                    total_size=_i["total_size"],
                    tracker=_i["tracker"],
                    trackers_count=_i["trackers_count"],
                    up_limit=_i["up_limit"],
                    uploaded=_i["uploaded"],
                    uploaded_session=_i["uploaded_session"],
                    upspeed=_i["upspeed"],
                )
            )
        return _torrent_list

    @staticmethod
    async def properties():
        # TODO properties
        pass

    @staticmethod
    async def trackers(
        client: AsyncClient, torrent: Torrent
    ) -> list[dict[str, str | int]]:
        """获取种子trackers信息"""
        _response: Response = await post_data(
            client=client,
            data={"hash": f"{torrent.hash}"},
            api="/api/v2/torrents/trackers",
        )
        return _response.json()

    @staticmethod
    async def webseeds():
        # TODO webseeds
        pass

    @staticmethod
    async def files():
        # TODO files
        pass

    @staticmethod
    async def pieceStates():
        # TODO pieceStates
        pass

    @staticmethod
    async def pieceHashes():
        # TODO pieceHashes
        pass

    @staticmethod
    async def pause():
        # TODO pause
        pass

    @staticmethod
    async def resume():
        # TODO resume
        pass

    @staticmethod
    async def delete():
        # TODO delete
        pass

    @staticmethod
    async def recheck():
        # TODO recheck
        pass

    @staticmethod
    async def reannounce():
        # TODO reannounce
        pass

    @staticmethod
    async def add_trackers(
        client: AsyncClient, trackers: str, torrent: Torrent
    ) -> Response:
        """添加tracker, trackers以\\n\\n分割"""
        return await post_data(
            client=client,
            data={"hash": torrent.hash, "urls": trackers},
            api="/api/v2/torrents/addTrackers",
        )

    @staticmethod
    async def editTracker():
        # TODO editTracker
        pass

    @staticmethod
    async def removeTrackers(
        client: AsyncClient, trackers: str, torrent: Torrent
    ) -> Response:
        """Qb 删除tracker, trackers以|分割"""
        return await post_data(
            client=client,
            data={"hash": torrent.hash, "urls": trackers},
            api="/api/v2/torrents/removeTrackers",
        )
