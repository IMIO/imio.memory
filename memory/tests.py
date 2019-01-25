# -*- coding: utf-8 -*-
from pyramid import testing

import unittest


class RootModelTests(unittest.TestCase):

    def _getTargetClass(self):
        from .models import Root
        return Root

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        wiki = self._makeOne()
        self.assertEqual(wiki.__parent__, None)
        self.assertEqual(wiki.__name__, None)


class AppmakerTests(unittest.TestCase):

    def _callFUT(self, zodb_root):
        from .models import appmaker
        return appmaker(zodb_root)

    def test_it(self):
        root = {}
        self._callFUT(root)
        self.assertEqual(root['app_root']['exported_users'].keys()[0], 'imio')


class AddViewContainerTests(unittest.TestCase):
    def _callFUT(self, context, request):
        from .views.default import view_page
        return view_page(context, request)

    def test_it(self):
        root = testing.DummyResource()
        root['MyTestApp'] = testing.DummyResource()
        group_id = testing.DummyResource(data={'municipality_id':'liege', 'imioapp_name':'iasmartweb', 'username':'bsuttor'})
        context.__parent__ = root
        context.__name__ = 'theapp'
        request = testing.DummyRequest()
        info = self._callFUT(context, request)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(info['imioapp_name'], 'iasmartweb')

# class ViewTests(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()
#
#     def tearDown(self):
#         testing.tearDown()
#
#     def test_my_view(self):
#         from .views.default import view_root
#         request = testing.DummyRequest()
#         info = my_view(request)
#         self.assertEqual(info['project'], 'memory')
