# -*- coding: utf-8 -*-
from .models import appmaker
from .models import Container
from .models import Content
from .views.root import get_root
from pyramid import testing
from webtest.app import AppError

import json
import pytest
import unittest


class AppmakerTests(unittest.TestCase):

    def _callFUT(self, zodb_root):
        return appmaker(zodb_root)

    def test_it(self):
        root = {}
        self._callFUT(root)
        self.assertEqual(root['app_root'], {})


class RootModelTests(unittest.TestCase):

    def _getTargetClass(self):
        from .models import Root
        return Root

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        root = self._makeOne()
        self.assertEqual(root.__parent__, None)
        self.assertEqual(root.__name__, None)


class ContainerTests(unittest.TestCase):
    def setUp(self):
        self.root = appmaker({})

    def test_add(self):
        app = Container(self.root, 'users')
        self.assertEqual(app.__parent__, self.root)
        Container(self.root, 'imio')
        request = testing.DummyRequest()
        keys = get_root(self.root, request)
        self.assertEqual(keys, ['users', 'imio'])

    def test_remove(self):
        app = Container(self.root, 'users')
        self.assertEqual(app.__parent__, self.root)
        self.assertEqual(len(self.root), 1)
        app.delete()
        self.assertEqual(len(self.root), 0)

    def test_add_container_in_container(self):
        app = Container(self.root, 'users')
        self.assertEqual(len(self.root), 1)
        company = Container(app, 'imio')
        self.assertEqual(company.__parent__.__name__, 'users')
        self.assertEqual(company.__name__, 'imio')
        self.assertEqual(len(self.root), 1)

    def test_remove_container_in_container(self):
        app = Container(self.root, 'users')
        company = Container(app, 'imio')
        self.assertEqual(len(company), 0)
        self.assertEqual(len(app), 1)
        company.delete()
        self.assertEqual(len(app), 0)


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.root = appmaker({})
        self.app = Container(self.root, 'users')

    def test_add(self):
        content = Content(self.app, 'bsuttor', {'username': 'bsuttor'})
        self.assertEqual(self.app.retrieve()[0], 'bsuttor')

    def test_remove(self):
        content = Content(self.app, 'bsuttor', {'username': 'bsuttor'})
        self.assertEqual(len(self.app.retrieve()), 1)
        content.delete()
        self.assertEqual(len(self.app.retrieve()), 0)


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        import tempfile
        import os.path
        from . import main
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = {'zodbconn.uri': uri,
                    'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm']}

        app = main({}, **settings)
        self.db = app.registry._zodb_databases['']
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        import shutil
        self.db.close()
        shutil.rmtree(self.tmpdir)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'' in res.body)

    def test_add_container(self):
        res = self.testapp.post_json('/', {'app_id': 'my_app'})
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'["my_app"]' in res.body)
        with pytest.raises(AppError):
            self.testapp.post_json('/', {'app_idd': 'my_app'})
        res = self.testapp.get('/my_app', status=200)
        res = self.testapp.post_json('/my_app', {'container_id': 'bsuttor'})
        res = self.testapp.get('/my_app', status=200)
        self.assertTrue(b'bsuttor' in res.body)

    def test_add_content(self):
        res = self.testapp.post_json('/', {'app_id': 'my_app'})
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'["my_app"]' in res.body)
        with pytest.raises(AppError):
            self.testapp.post_json('/', {'app_idd': 'my_app'})
        res = self.testapp.get('/my_app', status=200)
        res = self.testapp.post_json('/my_app', {'content_id': 'bsuttor'})
        res = self.testapp.get('/my_app', status=200)
        self.assertTrue(b'bsuttor' in res.body)

    def test_remove_content(self):
        res = self.testapp.post_json('/', {'app_id': 'my_app'})
        res = self.testapp.post_json('/my_app', {'container_id': 'imio'})
        res = self.testapp.post_json('/my_app/imio', {'container_id': 'iasmartweb'})
        res = self.testapp.post_json('/my_app/imio/iasmartweb', {
            'content_id': 'bsuttor',
            'username': 'bsuttor',
            'email': 'bsu@imio.be',
            'fullname': 'Benoît Suttor',
        })
        res = self.testapp.get('/my_app/imio/iasmartweb/bsuttor', status=200)
        self.assertEqual(res.json.get('email'), 'bsu@imio.be')
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)
        self.testapp.delete_json('/my_app/imio/iasmartweb/bsuttor')
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 0)

    def test_update_content(self):
        res = self.testapp.post_json('/', {'app_id': 'my_app'})
        res = self.testapp.post_json('/my_app', {'container_id': 'imio'})
        res = self.testapp.post_json('/my_app/imio', {'container_id': 'iasmartweb'})
        res = self.testapp.post_json('/my_app/imio/iasmartweb', {
            'content_id': 'bsuttor',
            'username': 'bsuttor',
            'email': 'bsu@imio.be',
            'fullname': 'Benoît Suttor',
        })
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)
        res = self.testapp.patch_json('/my_app/imio/iasmartweb/bsuttor', {
            'email': 'benoit@imio.be',
        })
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)
        res = self.testapp.get('/my_app/imio/iasmartweb/bsuttor', status=200)
        self.assertEqual(res.json.get('email'), 'benoit@imio.be')

    def test_replace_content(self):
        res = self.testapp.post_json('/', {'app_id': 'my_app'})
        res = self.testapp.post_json('/my_app', {'container_id': 'imio'})
        res = self.testapp.post_json('/my_app/imio', {'container_id': 'iasmartweb'})
        res = self.testapp.post_json('/my_app/imio/iasmartweb', {
            'content_id': 'bsuttor',
            'username': 'bsuttor',
            'email': 'bsu@imio.be',
            'fullname': 'Benoît Suttor',
        })
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)
        res = self.testapp.put_json('/my_app/imio/iasmartweb/bsuttor', {
            'content_id': 'benoit',
            'username': 'benoit',
            'email': 'ben@imio.be',
            'fullname': 'Ben Suttor',
        })
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)
        res = self.testapp.get('/my_app/imio/iasmartweb/bsuttor', status=404)
        self.assertEqual(res.body, b'The path /my_app/imio/iasmartweb/bsuttor is not found')  # noqa
        res = self.testapp.get('/my_app/imio/iasmartweb/benoit', status=200)
        self.assertEqual(res.json.get('email'), 'ben@imio.be')
        res = self.testapp.get('/my_app/imio/iasmartweb', status=200)
        self.assertEqual(len(res.json), 1)


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
