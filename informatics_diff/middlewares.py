import asyncio
import logging
from aiohttp import web

log = logging.getLogger()


@web.middleware
async def exception_middleware(request, handler):
    try:
        return await handler(request)
    except asyncio.CancelledError:
        pass
    except Exception:
        log.exception('Handler failed.')
        return web.json_response({}, status=500)

