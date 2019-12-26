import time
import requests
from watched_schema import validators
from .config import config
from .common import logger


def _addons(ctx, **kwargs):
    addons = []
    # TODO: Make this async
    for addon in config.addons.values():
        addons.append(addon.infos(ctx, index=True, **kwargs))
    return addons


class Context(object):
    def __init__(self, addon_id, action):
        if action == 'addons':
            self.fn = _addons
        elif action in ('infos', 'directory', 'metadata', 'source', 'subtitle', 'resolve'):
            if addon_id == 'repository':
                addon_id = config.repository.id
            addon = config.addons.get(addon_id)
            if not addon:
                raise ValueError(
                    'Addon {} not found (called with action {})'.format(addon_id, action))
            self.fn = getattr(addon, action)
        else:
            raise ValueError('Unknown action '+action)

        self.action = action
        self.schema = validators['actions'][action]

    def run(self, request):
        request = self.schema['request'](request)
        logger.info("Calling %s: %s", self.action, request)
        response = self.fn(self, **request)
        return self.schema['response'](response)

    def fetch(self, url, method="GET", **kwargs):
        return requests.request(method, url, **kwargs)

    def fetch_remote(self, *args, **kwargs):
        return self.fetch(*args, **kwargs)
