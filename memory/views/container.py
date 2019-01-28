# -*- coding: utf-8 -*-
from ..models import Container
from ..models import Content
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config


# create wuth POST
# Update with PATCH
# Reading with GET
# replace with PUT
# delete with DELETE


@view_config(request_method='GET', context=Container, renderer='json')
def get_container(context, request):
    retrieve = context.retrieve()
    if retrieve is None:
        raise HTTPNotFound()
    else:
        return retrieve


@view_config(request_method='POST', context=Container, renderer='json')
def create_content(context, request):
    content_id = request.json_body.get('content_id', None)
    container_id = request.json_body.get('container_id', None)
    if not content_id and not container_id:
        raise HTTPBadRequest(
            'You need content_id or container_id in your json data {0}'.format(
                request.json_body
            )
        )
    if content_id:
        Content(context, content_id, request.json_body)
    else:
        Container(context, container_id)

    return Response(
        status='201 Created',
        content_type='application/json; charset=UTF-8')


@view_config(request_method='DELETE', context=Container, renderer='json')
def delete_content(context, request):
    context.delete()
    return Response(
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')
