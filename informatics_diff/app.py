import asyncio
from aiohttp import web

from informatics_diff.handlers import ping_handler
from informatics_diff.storage import Storage
from informatics_diff.log import configure_logging
from informatics_diff.tasks import StandingLoader


class InformaticsDiffApplication(web.Application):
    def __init__(self, storage):
        super().__init__()
        self['storage'] = storage
        self.init_routes()
        self.on_startup.append(self.start_background_tasks)
        self.on_cleanup.append(self.cleanup_background_tasks)

    @property
    def storage(self):
        return self['storage']

    def init_routes(self):
        self.add_routes([
            web.get('/ping', ping_handler),
        ])

    async def start_background_tasks(self, app):
        app['standings_loader'] = asyncio.create_task(StandingLoader().run())

    async def cleanup_background_tasks(self, app):
        await app['standings_loader'].cancel()


if __name__ == '__main__':
    configure_logging()
    app = InformaticsDiffApplication(
        storage=Storage(),
    )
    web.run_app(app, host='0.0.0.0', port=8088)
