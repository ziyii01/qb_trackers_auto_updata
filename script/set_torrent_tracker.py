import argparse
import http.cookiejar
import json
import urllib.parse
import urllib.request

URL = "http://127.0.0.1:8080"
USERNAME = ""
PASSWORD = ""


cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)


def post(url, data):
    encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded_data, method="POST")
    with opener.open(req) as response:
        response_data = response.read()
        return response_data.decode("utf-8")


def main(torrent_hash):
    post(f"{URL}/api/v2/auth/login", {"username": USERNAME, "password": PASSWORD})
    trackers = post(f"{URL}/api/v2/torrents/trackers", {"hash": torrent_hash})
    trackers = json.loads(trackers)
    _remove_trackers = ""
    for _i in trackers:
        if _i["url"] == "** [DHT] **":
            continue
        if _i["url"] == "** [PeX] **":
            continue
        if _i["url"] == "** [LSD] **":
            continue
        _remove_trackers += f"{_i['url']}|"
    _remove_trackers = _remove_trackers[:-1]
    post(
        f"{URL}/api/v2/torrents/removeTrackers",
        {"hash": torrent_hash, "urls": _remove_trackers},
    )
    post(
        f"{URL}/api/v2/torrents/addTrackers",
        {
            "hash": torrent_hash,
            "urls": "https://btn-prod.ghostchu-services.top/tracker/announce",
        },
    )


parser = argparse.ArgumentParser(description="qb 种子修改 tracker")
parser.add_argument("-I", type=str, help="种子的 v1 哈希值")
args = parser.parse_args()
main(args.I)
