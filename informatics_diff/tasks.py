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
    _LOGIN_URL = config.informatics_proxy_url + '/login'
    _STANDINGS_URL = config.informatics_proxy_url + '/standings'

    _username = config.informatics_username
    _password = config.informatics_password
    _sleep = config.watch_sleep
    _max_snapshots = config.watch_max_snapshots

    def __init__(self, storage, key, statement_id, group_id):
        super().__init__()
        self.cookie_cache = cachetools.TTLCache(
            1,
            config.informatics_cookie_ttl,
        )
        self._storage = storage
        self._key = key
        self._statement_id = statement_id
        self._group_id = group_id

    @property
    def storage(self):
        return self._storage

    @property
    def key(self):
        return self._key

    async def get_cookies(self):
        if 'cookie' not in self.cookie_cache:
            json = {
                'username': self._username,
                'password': self._password,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self._LOGIN_URL, json=json) as response:
                    assert response.status == 200, 'Login failed.'
                    self.cookie_cache['cookie'] = await response.json()
        return self.cookie_cache['cookie']

    async def get_standings(self):
        cookies = await self.get_cookies()
        params = {
            'statement_id': self._statement_id,
            'group_id': self._group_id,
        }
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(self._STANDINGS_URL, params=params) as response:
                assert response.status == 200, 'Standings failed.'
                return await response.json()

    async def _run(self):
        if not await self.storage.has(self.key):
            await self.storage.set(self.key, [])

        for i in range(3):
            # Add locking here one day
            try:
                standings = await self.get_standings()
            except Exception:
                log.exception('Failed to get standings.')
            else:
                stored = await self.storage.get(self.key)
                await self.storage.set(self.key, stored + [standings])
            finally:
                await asyncio.sleep(self._sleep)
