# -*- coding: utf-8 -*-
# from cornice import Service
from pyramid.view import view_config


@view_config(context='..models.Root', renderer='string')
def view_root(context, request):
    return 'You can get data from: {0}'.format('<br />-'.join(context.keys()))
