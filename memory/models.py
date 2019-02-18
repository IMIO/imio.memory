# -*- coding: utf-8 -*-
from persistent import Persistent
from persistent.mapping import PersistentMapping

import transaction


class Container(PersistentMapping):

    def __init__(self, parent, name):
        PersistentMapping.__init__(self)
        self.__parent__ = parent
        self.__name__ = name
        self.__parent__[name] = self

    # def update(self, child):
    #     self.data = self.data.update({child.__name__: child})

    def retrieve(self):
        # import ipdb; ipdb.set_trace()
        return [elem for elem in self]

    def delete(self):
        del self.__parent__[self.__name__]

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.__name__)


class Root(Container):
    __name__ = None
    __parent__ = None

    def __init__(self):
        PersistentMapping.__init__(self)


class Content(Persistent):
    def __init__(self, parent, name, data={}):
        Persistent.__init__(self)
        # import ipdb; ipdb.set_trace()
        self.__parent__ = parent
        self.__name__ = name
        self.__parent__[self.__name__] = self
        self.data = data

    def update(self, data):
        self.data.update(data)

    def delete(self):
        del self.__parent__[self.__name__]

    def keys(self):
        return self.data.keys()

    def get(self, key):
        return self.data.get(key, '')

    def __repr__(self):
        return '<{0} {1}/{2}>'.format(
            self.__class__.__name__,
            self.__parent__.__name__,
            self.__name__
        )



def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = Root()
        zodb_root['app_root'] = app_root
        transaction.commit()
    return zodb_root['app_root']
