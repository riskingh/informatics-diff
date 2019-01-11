from aiohttp import web

from informatics_diff.handlers import ping_handler
from informatics_diff.storage import Storage
from informatics_diff.config import config


class InformaticsDiffApplication(web.Application):
    def __init__(self, storage: Storage):
        super().__init__()
        self['storage'] = storage
        self.init_routes()
        self.on_startup.append(self.init_workers)

    @property
    def storage(self):
        return self['storage']

    def init_routes(self):
        self.add_routes([
            web.get('/ping', ping_handler),
        ])

    async def init_workers(self, app):
        print('init_workers...')


if __name__ == '__main__':
    print(config)
    app = InformaticsDiffApplication(
        storage=Storage()
    )
    web.run_app(app, host='0.0.0.0', port=8088)
