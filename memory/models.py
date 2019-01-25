# -*- coding: utf-8 -*-
from persistent import Persistent
from persistent.mapping import PersistentMapping


class Root(PersistentMapping):
    __name__ = None
    __parent__ = None


class Container(dict):
    def __init__(self, name, parent, title=None):
        self.__name__ = name
        self.__parent__ = parent
        if not title:
            title = name
        self.title = title


class Content(object):
    def __init__(self, name, parent, data={}):
        self.__name__ = name
        self.__parent__ = parent
        self.data = data


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = Root()
        default_app_name = 'exported_users'
        container = Container(default_app_name, app_root)
        app_root[default_app_name] = container
        group_id = Container('imio', container)
        container['imio'] = group_id
        content = Content('bsuttor', group_id, {'imioapp': 'iasmartweb'})
        group_id['bsuttor'] = content
        # app.__name__ = default_app_name
        # app.__parent__ = app_root
        zodb_root['app_root'] = app_root
    return zodb_root['app_root']
