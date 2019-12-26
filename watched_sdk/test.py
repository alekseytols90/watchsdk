import sys
import json
import random
from watched_schema import validators
from .config import config
from .context import Context
from .common import logger


def call(addon_id, action, **kwargs):
    ctx = Context(addon_id, action)
    response = ctx.run(data)
    if response is None:
        raise ValueError('empty')
    return response


def test_addon(addon):
    logger.warning('- Testing addon %s', addon.id)
    test_items = []
    test_sources = []

    def add_item(item):
        test_items.append(item)
        for source in item.get('sources', []):
            source['item'] = item
            test_sources.append(source)

    def has_action(action):
        return any(action in r['actions'] for r in addon['resources'])

    if addon.test_items:
        map(add_item, addon.test_items)
    for dashboard in addon['dashboards']:
        logger.warning('-- Dashboard %s', dashboard['name'])
        res = call(addon.id, 'directory', **dashboard['args'])
        logger.warning('--- items=%s, hasMore=%s',
                       len(res['items']), res['hasMore'])
        map(add_item, res['items'])
    if has_action('directory'):
        for directory in addon['dashboards']:
            id = directory.get("args", {}).get('resourceId', "default")
            logger.warning('-- Testing resource %s', id)
            res = call(addon.id, 'directory', resourceId=id)
            logger.warning('--- items=%s, hasMore=%s',
                           len(res['items']), res['hasMore'])
            map(add_item, res['items'])
        n = 0
        random.shuffle(test_items)
        for item in test_items:
            if item['type'] != 'directory':
                continue
            logger.warning('-- Directory %s', item['id'])
            res = call(addon.id, 'directory', resourceId=id,
                       directoryId=item['id'])
            logger.warning('--- items=%s, hasMore=%s',
                           len(res['items']), res['hasMore'])
            map(add_item, res['items'])
            n += 1
            if n > 5:
                break
    if has_action('metadata'):
        for _ in range(5):
            item = random.choice(test_items)
            if item['type'] == 'directory':
                continue
            logger.warning('-- Metadtata %s', item['ids'][addon.id])
            res = call(addon.id, 'metadata', **item)
            logger.warning('--- %r', res)
    if has_action('source'):
        for _ in range(5):
            item = random.choice(test_items)
            if item['type'] == 'directory':
                continue
            logger.warning('-- Source %s', item['ids'][addon.id])
            res = call(addon.id, 'source', **item)
            logger.warning('--- %r', res)
    if has_action('resolve') and test_sources:
        for _ in range(5):
            source = random.choice(test_sources)
            if source['item']['type'] == 'directory':
                continue
            logger.warning('-- Resolve %s', source['url'])
            res = call(addon.id, 'resolve', **source)
            logger.warning('--- %r', res)


def test_addons(*args):
    for addon in config.addons.values():
        if not args or addon.id in args:
            test_addon(addon)
