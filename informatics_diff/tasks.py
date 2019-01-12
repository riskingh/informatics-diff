import aiohttp
import asyncio
import logging
import cachetools

from informatics_diff.config import config

log = logging.getLogger()


class BaseTask:
    async def _run(self):
        raise NotImplementedError

    async def _close(self):
        pass

    async def run(self):
        try:
            await self._run()
        except asyncio.CancelledError:
            pass
        except Exception:
            log.exception('Task failed.')
        finally:
            await self._close()


class StandingLoader(BaseTask):
    _login_url = config.informatics_proxy_url + '/login'
    _username = config.informatics_username
    _password = config.informatics_password

    def __init__(self):
        super().__init__()
        self.cookie_cache = cachetools.TTLCache(
            1,
            config.informatics_cookie_ttl,
        )

    async def get_cookies(self):
        if 'cookie' not in self.cookie_cache:
            json = {
                'username': self._username,
                'password': self._password,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self._login_url, json=json) as response:
                    self.cookie_cache['cookie'] = await response.json()
        return self.cookie_cache['cookie']

    async def _run(self):
        log.info('run...')
        for i in range(5):
            print(await self.get_cookies())
            await asyncio.sleep(2)
