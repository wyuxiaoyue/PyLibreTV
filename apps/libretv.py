import hashlib
import json

import aiohttp_jinja2
from aiohttp import ClientSession, hdrs, web
from yarl import URL

from settings import ADMIN_PASSWORD, HOST, PASSWORD
from sites import SITES_KEY, Site

SESSION_KEY = web.AppKey("SESSION_KEY", ClientSession)


def sha256(string: str):
    return hashlib.sha256(string.encode()).hexdigest() if string else ""


def convert_site(url: URL, name: str, site: Site):
    return {"name": site.name, "api": str(url.joinpath(name))}


async def session_context(app):
    async with ClientSession() as session:
        app[SESSION_KEY] = session
        yield


async def handler(request: web.Request):
    name = request.url.name
    template_name = "player.html" if name == "player.html" else "index.html"
    context = {"PASSWORD": sha256(PASSWORD), "ADMINPASSWORD": sha256(ADMIN_PASSWORD)}
    return await aiohttp_jinja2.render_template_async(template_name, request, context)


async def hook_app_handler(request: web.Request):
    data = [key for key in request.app[SITES_KEY].keys()][:10]
    selected_apis = json.dumps(data, ensure_ascii=False)
    context = {"selected_apis": selected_apis}
    return await aiohttp_jinja2.render_template_async("app.js", request, context)


async def hook_config_handler(request: web.Request):
    host, port, *_ = request.transport.get_extra_info("sockname")
    url = URL.build(scheme="http", host=HOST or host, port=port, path="/site/libretv")
    sites = request.app[SITES_KEY]
    context = {"sites": {n: convert_site(url, n, site) for n, site in sites.items()}}
    return await aiohttp_jinja2.render_template_async("config.js", request, context)


async def proxy_handler(request: web.Request):
    session = request.app[SESSION_KEY]
    url = URL(request.match_info.get("url"))
    headers = request.headers.copy()
    headers[hdrs.HOST] = url.host
    headers[hdrs.REFERER] = str(url.origin())
    async with session.get(url, headers=headers, auto_decompress=False) as resp:
        response = web.StreamResponse(status=resp.status, headers=resp.headers)
        await response.prepare(request)
        async for chunk in resp.content.iter_chunked(8192):
            await response.write(chunk)
        await response.write_eof()
        return response


def setup(app: web.Application):
    app.cleanup_ctx.append(session_context)
    routes = [
        web.get("/", handler),
        web.get("/index.html", handler),
        web.get("/player.html", handler),
        web.get("/s={keyword}", handler),
        web.get("/js/app.js", hook_app_handler),
        web.get("/js/config.js", hook_config_handler),
        web.get("/proxy/{url}", proxy_handler),
        web.static("/", "templates/LibreTV"),
    ]
    app.add_routes(routes)
