# -*- coding: utf-8 -*-
from pyramid.view import notfound_view_config


@notfound_view_config(renderer='string')
def notfound_view(request):
    request.response.status = 404
    path = '/' + '/'.join(request.traversed) + '/' + request.view_name
    return 'The path {0} is not found'.format(path)
