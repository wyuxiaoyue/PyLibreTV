import functools
import json

from aiohttp import web
from yarl import URL

from settings import HOST
from sites import SITES_KEY, Site

dumps = functools.partial(json.dumps, ensure_ascii=False)


def convert_site(url: URL, name: str, site: Site):
    return {"key": name, "type": 1, "name": site.name, "api": str(url.joinpath(name))}


async def tvbox_handler(request: web.Request):
    host, port, *_ = request.transport.get_extra_info("sockname")
    url = URL.build(scheme="http", host=HOST or host, port=port, path="/site/tvbox")

    data = {"sites": [], "rules": []}
    for name, site in request.app[SITES_KEY].items():
        data["sites"].append(convert_site(url, name, site))
        if hasattr(site, "rule"):
            data["rules"].append({"name": site.name, **site.rule})

    return web.json_response(data, dumps=dumps)


def setup(app: web.Application):
    app.add_routes([web.get("/tvbox.json", tvbox_handler)])
