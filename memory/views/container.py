# -*- coding: utf-8 -*-
from ..models import Container
from ..models import Content
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config


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

    # if content_id:
    #     new_content = Content(content_id)
    #     new_content.__name__ = content_id
    #     new_content.__parent__ = context
    #     new_content['data'] = request.json_body
    #     context[content_id] = new_content
    # if container_id:
    #     new_container = Container(container_id)
    #     new_container.__name__ = container_id
    #     new_container.__parent__ = context
    #     context[container_id] = new_container

    return Response(
        status='201 Created',
        content_type='application/json; charset=UTF-8')


@view_config(request_method='DELETE', context=Container, renderer='json')
def delete_content(context, request):
    context.delete()
    return Response(
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')


class UserList(list):
    def add_or_merge(self, obj):
        # check if user already exist with the same municipality_id
        if len(self) == 0:
            self.append(obj)
        else:
            for item in self:
                index = self.index(item)
                # import ipdb; ipdb.set_trace()
                if obj.get('user_id') == item.get('user_id'):
                    # merge
                    user_id = obj.get('user_id')
                    old_app_id = item.get('app_id')
                    new_app_id = obj.get('app_id')
                    item['old_{0}_password'.format(old_app_id)] = item.get('password')
                    item['old_{0}_password'.format(new_app_id)] = obj.get('password')
                    item['old_{0}_userid'.format(old_app_id)] = user_id
                    item['old_{0}_userid'.format(new_app_id)] = user_id
                    self[index] = item
                elif obj.get('user_id') not in self.get('user_id'):
                    self.append(obj)
                else:
                    pass

    def keys(self):
        listkeys = []
        for row in self:
            for key in row.keys():
                if key not in listkeys:
                    listkeys.append(key)
        return listkeys

    def get(self, key):
        return [val[key] for val in self]

    def values(self):
        keys = self.keys()
        vals = []
        for row in self:
            list = []
            for key in keys:
                if key not in row.keys():
                    row[key] = ''
                list.append(row[key])
            vals.append(list)
        return vals


@view_config(name='csv', context=Container, renderer='csv')
def merged_csv(context, request):
    headers = [
        'app_id',
        'municipality_id',
        'user_id',
        'fullname',
        'email',
        'password'
    ]
    rows = UserList()
    for app_id, app in context.items():
        for user_id, user in app.data.items():
            new_user = {}
            new_user['municipality_id'] = context.__name__
            new_user['app_id'] = app_id
            new_user['user_id'] = user.get('content_id')
            for head in headers:
                if not new_user.get(head, ''):
                    new_user[head] = user.get(head)
            rows.add_or_merge(new_user)
    return {
      'header': rows.keys(),
      'rows': rows.values(),
    }
