# -*- coding: utf-8 -*-
from ..models import Container
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


@view_config(context='..models.Container', renderer='json')
def view_container(context, request):
    return context.keys()


@view_config(context='..models.Container', name='add_container')
def add_container(context, request):
    name = request.POST['id']
    new_container = Container(name, context, name)
    context[name] = new_container
    url = request.resource_url(new_container)
    return HTTPFound(location=url)


@view_config(context='..models.Container', name='remove_container')
def remove_container(context, request):
    parent = context.__parent__
    id = request.POST['id']
    if id not in parent.keys():
        return '{0} not exists in {1}'.format(id, parent.__name__)
    del parent[id]
    url = request.resource_url(parent)
    return HTTPFound(location=url)
