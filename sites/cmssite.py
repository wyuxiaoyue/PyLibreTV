from aiohttp import web
from yarl import URL

from sites import Site


class CMSSite(Site):
    """通用 CMS 视频站点

    兼容与适配支持 MacCMS V10.x 接口的站点。
    """

    base_url: str

    async def parse_request(self, request):
        query = request.query
        kwargs = {k: query[k] for k in ["ac", "ids", "t", "pg", "wd"] if k in query}

        app = request.match_info.get("app")
        if app not in ["libretv", "tvbox"]:
            raise web.HTTPNotFound
        elif app == "libretv":
            kwargs["ac"] = "detail"
        elif "ac" not in kwargs:
            kwargs["ac"] = "list"

        url = URL(self.base_url).extend_query(**kwargs)
        async with self.session.get(url) as resp:
            return await resp.read()


class MTSite(CMSSite):
    """https://mtzy.me/"""

    name = "茅台资源"
    base_url = "https://caiji.maotaizy.cc/api.php/provide/vod/"


class LZSite(CMSSite):
    """https://lzizy.net/"""

    name = "量子资源"
    base_url = "https://cj.lziapi.com/api.php/provide/vod/"


class DYTTSite(CMSSite):
    """http://caiji.dyttzyapi.com/"""

    name = "电影天堂资源"
    base_url = "http://caiji.dyttzyapi.com/api.php/provide/vod/"


class RYSite(CMSSite):
    """https://www.ryzyw.com/"""

    name = "如意资源"
    base_url = "https://cj.rycjapi.com/api.php/provide/vod/"


class BFSite(CMSSite):
    """https://bfzy.tv/"""

    name = "暴风资源"
    base_url = "http://by.bfzyapi.com/api.php/provide/vod/"


class TYYSSite(CMSSite):
    """https://tyyszy.com/"""

    name = "天涯影视资源"
    base_url = "https://ty.tyyszy5.com/api.php/provide/vod/"


class WWSite(CMSSite):
    """https://wwzy.tv/"""

    name = "旺旺资源"
    base_url = "https://api.wwzy.tv/api.php/provide/vod/"


class FFSite(CMSSite):
    """https://tyyszy.com/"""

    name = "非凡资源"
    base_url = "http://api.ffzyapi.com/api.php/provide/vod/"


class HMESite(CMSSite):
    """https://heimuer.tv/"""

    name = "黑木耳资源"
    base_url = "https://json02.heimuer.xyz/api.php/provide/vod/"


class T60Site(CMSSite):
    """https://360zy.com/"""

    name = "360资源"
    base_url = "https://360zy.com/api.php/provide/vod/"


class WLSite(CMSSite):
    """https://wolongzyw.com/"""

    name = "卧龙资源"
    base_url = "https://collect.wolongzy.cc/api.php/provide/vod/"


class JSSite(CMSSite):
    """https://jszyapi.com/"""

    name = "极速资源"
    base_url = "https://jszyapi.com/api.php/provide/vod/"


class DBSite(CMSSite):
    """https://dbzy.tv/"""

    name = "豆瓣资源"
    base_url = "https://caiji.dbzy5.com/api.php/provide/vod/"


class MZSite(CMSSite):
    """https://mozhuazy.com/"""

    name = "魔爪资源"
    base_url = "https://mozhuazy.com/api.php/provide/vod/"


class MDSite(CMSSite):
    """https://www.mdzyapi.com/"""

    name = "魔都资源"
    base_url = "https://www.mdzyapi.com/api.php/provide/vod/"


class ZDSite(CMSSite):
    """https://www.zuidazy.co/"""

    name = "最大资源"
    base_url = "https://api.zuidapi.com/api.php/provide/vod"


class YHSite(CMSSite):
    """https://yhzy.cc/"""

    name = "樱花资源"
    base_url = "https://m3u8.apiyhzy.com/api.php/provide/vod/"


class BDSite(CMSSite):
    """https://api.apibdzy.com/"""

    name = "百度资源"
    base_url = "https://api.apibdzy.com/api.php/provide/vod/"


class WJSite(CMSSite):
    """https://www.wujinzy.com/"""

    name = "无尽资源"
    base_url = "https://api.wujinapi.me/api.php/provide/vod/"


class IKSite(CMSSite):
    """https://www.ikunzy.com/"""

    name = "iKun资源"
    base_url = "https://ikunzyapi.com/api.php/provide/vod/"
