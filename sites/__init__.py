import abc
import importlib
import logging
import pathlib

from aiocache import cached
from aiocache.serializers import PickleSerializer
from aiohttp import ClientError, ClientRequest, ClientSession, ClientTimeout, web

from settings import HEADERS, REQUEST_TIMEOUT, RETRY_TIMES

logger = logging.getLogger("sites")

SITES_KEY = web.AppKey("SITES_KEY", dict[str, "Site"])


async def retry_middleware(request: ClientRequest, handler):
    for i in range(RETRY_TIMES):
        try:
            return await handler(request)
        except ClientError as e:
            logger.warning("%s (Retries: %s)", e, i)
    raise web.HTTPServiceUnavailable


class Site:
    """任何站点都必须继承的基类

    它提供了一个基础的站点框架，通过重载 start_request() 响应特定站点的请求。
    """

    name: str

    def __init__(self, app: web.Application):
        self.app = app
        self.session = ClientSession(
            headers=HEADERS,
            timeout=ClientTimeout(total=REQUEST_TIMEOUT, connect=2),
            middlewares=(retry_middleware,),
        )

    @property
    def logger(self):
        return logging.getLogger(self.name)

    async def prepare(self):
        return self

    async def start_request(self, request: web.Request):
        return await self.parse_data(request, await self.parse_request(request))

    @abc.abstractmethod
    async def parse_request(self, request: web.Request):
        raise NotImplementedError

    async def parse_data(self, request: web.Request, data) -> bytes:
        return data

    async def close(self):
        await self.session.close()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r} at 0x{id(self):0x}>"


async def sites_context(app):
    sites = {}
    base = pathlib.Path(__file__).parent
    for file in base.iterdir():
        if not file.is_file() or file.suffix != ".py":
            continue
        path = f"{base.stem}.{file.stem}"
        module = importlib.import_module(path)
        for name, cls in module.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, Site) and hasattr(cls, "name"):
                sites[name] = await cls(app).prepare()
                logger.debug("Enabled %s.%s", path, name)

    app[SITES_KEY] = sites
    yield

    for site in sites.values():
        await site.close()


@cached(60, key_builder=lambda _, x: x.path_qs, serializer=PickleSerializer())
async def site_handler(request: web.Request):
    site = request.app[SITES_KEY][request.match_info["name"]]
    return web.json_response(body=await site.start_request(request))


def setup(app: web.Application):
    app.cleanup_ctx.append(sites_context)
    app.add_routes([web.get("/site/{app}/{name}", site_handler)])
