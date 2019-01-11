import asyncio


class BaseTask:
    async def _run(self):
        raise NotImplementedError

    async def _close(self):
        pass

    async def run(self):
        try:
            await self._run(self)
        except asyncio.CancelledError:
            pass
        finally:
            await self._close()


class StandingLoader(BaseTask):
    def __init__(self):
        pass
