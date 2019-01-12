class Storage:
    def __init__(self):
        self._data = {}

    async def set(self, key, value):
        self._data[key] = value

    async def get(self, key):
        return self._data[key]

    async def has(self, key):
        return key in self._data
