# -*- coding: utf-8 -*-


class Resource(dict):

    def __init__(self, ref, parent):
        self.__name__ = ref
        self.__parent__ = parent

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.__name__)


class Root(Resource):

    def __init__(self):
        Resource.__init__(self, ref=None, parent=None)


class Container(Resource):

    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.__parent__[name] = self

    def retrieve(self):
        return [elem for elem in self]

    def delete(self):
        del self.__parent__[self.__name__]


class Content(object):
    def __init__(self, parent, name, data={}):
        self.__parent__ = parent
        self.__name__ = name
        self.__parent__[self.__name__] = self
        self.data = data

    def update(self, data):
        self.data.update(data)

    def delete(self):
        del self.__parent__[self.__name__]

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
    return zodb_root['app_root']
