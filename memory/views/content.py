# -*- coding: utf-8 -*-
from ..models import Content
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config


@view_config(request_method='GET', context=Content, renderer='json')
def get_content(context, request):
    return context.data


@view_config(request_method='PATCH', context=Content, renderer='json')
def update_content(context, request):
    context.update(request.json_body)


@view_config(request_method='PUT', context=Content, renderer='json')
def replace_content(context, request):
    content_id = request.json_body.get('content_id', None)
    if not content_id:
        raise HTTPBadRequest(
            'You need content_id in your json data {0}'.format(
                request.json_body
            )
        )
    context.delete()
    Content(context.__parent__, content_id, request.json_body)


@view_config(request_method='DELETE', context=Content, renderer='json')
def delete_content(context, request):
    context.delete()
    return Response(
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')
