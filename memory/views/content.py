# -*- coding: utf-8 -*-
from pyramid.view import view_config


@view_config(context='..models.Content', renderer='json')
def view_content(context, request):
    return context.data


@view_config(context='..models.Content', name='add_content')
def add_content(context, request):
    # root = context.__parent__
    # import ipdb; ipdb.set_trace()
    return context.data
