URL_ROOT = "http://127.0.0.1:8090"  # Qb webui的地址
USERNAME = ""  # Qb webui的用户名
PASSWORD = ""  # Qb webui的密码
TRACKER_URLS_LIST = [
    "https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/ATline_best.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt",
    "https://cf.trackerslist.com/best.txt",
]  # 订阅的trackers地址列表
TRACKER_URL_LIST = [
    "http://open.acgtracker.com:1096/announce",
    "https://btn-prod.ghostchu-services.top/tracker/announce",
]  # 单独添加的tracker地址列表
SEMAPHORE_THREAD_HOLD = 16  # 检查tracker的线程数
ALLOW_HTTP_STATUS_CODE = (200, 403)  # 允许的http状态码
TIMEOUT = 5  # 超时时间
RETRY_TIMES = 3  # 重试次数
