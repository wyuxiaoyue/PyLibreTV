from aiohttp import web

from apps import libretv, tvbox


def setup(app: web.Application):
    tvbox.setup(app)
    libretv.setup(app)
