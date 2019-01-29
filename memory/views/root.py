# -*- coding: utf-8 -*-
# from cornice import Service
from ..models import Container
from ..models import Root
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config


@view_config(request_method='GET', renderer='json', context=Root)
def get_root(context, request):
    return list(context)


@view_config(request_method='POST', context=Root, renderer='json')
def create_container(context, request):
    app_id = request.json_body.get('app_id', None)
    if not app_id:
        raise HTTPBadRequest(
            'You need app_id in json data {0}'.format(request.json_body)
        )
    Container(context, app_id)
    return Response(
        status='201 Created',
        content_type='application/json; charset=UTF-8')
