from aiohttp import web


async def ping_handler(request):
    return web.Response(text='pong')
