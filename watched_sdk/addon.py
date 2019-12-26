from watched_schema import validators
from .config import config


def hard_copy(obj):
    if isinstance(obj, (set, list, tuple)):
        return list(map(hard_copy, obj))
    if isinstance(obj, dict):
        return {key: hard_copy(value) for key, value in obj.items()}
    return obj


class Addon(object):
    test_items = None

    def __init__(self):
        props = {'type': 'worker'}
        props.update(self.get_props())

        if config.repository:
            p = config.repository.props
            if not props.get('id'):
                props['id'] = p['id']
            if not props.get('name'):
                props['name'] = p['name']
            if not props.get('version'):
                props['version'] = p['version']
            if not props.get('homepage') and p.get('homepage'):
                props['homepage'] = p['homepage']

        self.props = validators['models']['addon'](props)
        config.register_addon(self)

    def get_props(self):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self.props[key]

    @property
    def id(self):
        return self.props["id"]

    @property
    def type(self):
        return self.props["type"]

    def get_cache(self, key):
        return config.cache.get([self.id, key])

    def set_cache(self, key, value, ttl=24 * 3600):
        return config.cache.set([self.id, key], value, ttl)

    def delete_cache(self, key):
        return config.cache.delete([self.id, key])

    def infos(self, ctx, **kwargs):
        return hard_copy(self.props)

    def directory(self, ctx, **kwargs):
        raise NotImplementedError()

    def metadata(self, ctx, **kwargs):
        raise NotImplementedError()

    def source(self, ctx, **kwargs):
        raise NotImplementedError()

    def subtitle(self, ctx, **kwargs):
        raise NotImplementedError()

    def resolve(self, ctx, **kwargs):
        raise NotImplementedError()


def create_addon(props):
    class MyAddon(Addon):
        def get_props(self):
            return props
    return MyAddon()


def setup_repository(props):
    new_props = {'mirrors': [props['homepage']]
                 if props.get('homepage') else []}
    new_props.update(props)
    new_props.update({'type': 'repository'})
    config.set_repository(create_addon(new_props))
