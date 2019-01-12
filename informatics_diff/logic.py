from informatics_diff.config import config


async def get_standings_snapshots(storage):
    return await storage.get(config.storage_key)


async def get_standings_diff(from_ts, to_ts):
    pass
