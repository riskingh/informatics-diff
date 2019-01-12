import os
import logging
import importlib.util
from dataclasses import dataclass, fields


@dataclass
class Config:
    logging_level: int = logging.DEBUG
    informatics_proxy_url = 'http://localhost:8089'
    informatics_username: str = 'test'
    informatics_password: str = 'test'
    informatics_cookie_ttl: int = 600


config_path = os.environ.get('CONFIG_PATH')
if config_path:
    spec = importlib.util.spec_from_file_location('config_module', config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    kwargs = {}
    for field in fields(Config):
        value = config_module.__dict__[field.name]
        if not isinstance(value, field.type):
            value = field.type(value)
        kwargs[field.name] = value
    config = Config(**kwargs)
else:
    config = Config()
