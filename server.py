import logging

import aiohttp_jinja2
import jinja2
from aiohttp import ClientConnectionResetError, web

import apps
import sites
from settings import LOG_LEVEL, PORT


@web.middleware
async def exception_middleware(request: web.Request, handler) -> web.StreamResponse:
    try:
        return await handler(request)
    except ClientConnectionResetError:
        raise web.HTTPAccepted


@web.middleware
async def compress_middleware(request: web.Request, handler) -> web.StreamResponse:
    response = await handler(request)
    response.enable_compression()
    return response


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)

    app = web.Application(middlewares=(exception_middleware, compress_middleware))

    apps.setup(app)
    sites.setup(app)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(["templates", "templates/LibreTV"]),
        keep_trailing_newline=True,
        autoescape=False,
        enable_async=True,
    )

    web.run_app(app, port=PORT)
