from aiohttp import web

from informatics_diff import logic


async def ping_handler(request):
    return web.Response(text='pong')


async def get_standings_snapshots(request):
    return web.json_response(
        await logic.get_standings_snapshots(request.app.storage)
    )


async def get_standings_diff(request):
    pass
