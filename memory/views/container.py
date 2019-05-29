# -*- coding: utf-8 -*-
from ..models import Container
from ..models import Content
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config


@view_config(request_method="GET", context=Container, renderer="json")
def get_container(context, request):
    retrieve = context.retrieve()
    if retrieve is None:
        raise HTTPNotFound()
    else:
        return retrieve


@view_config(request_method="POST", context=Container, renderer="json")
def create_content(context, request):
    content_id = request.json_body.get("content_id", None)
    container_id = request.json_body.get("container_id", None)
    if not content_id and not container_id:
        raise HTTPBadRequest(
            "You need content_id or container_id in your json data {0}".format(
                request.json_body
            )
        )
    if content_id:
        Content(context, content_id, request.json_body)
    else:
        Container(context, container_id)

    return Response(
        status="201 Created", content_type="application/json; charset=UTF-8"
    )


@view_config(request_method="DELETE", context=Container, renderer="json")
def delete_content(context, request):
    context.delete()
    return Response(
        status="202 Accepted", content_type="application/json; charset=UTF-8"
    )


class UserList(list):
    def add_or_merge(self, obj):
        # check if user already exist with the same municipality_id
        if len(self) == 0:
            self.append(obj)
        else:
            for item in self:
                index = self.index(item)
                # import ipdb; ipdb.set_trace()
                if obj.get("user_id") == item.get("user_id"):
                    # merge
                    user_id = obj.get("user_id")
                    old_app_id = item.get("app_id")
                    new_app_id = obj.get("app_id")
                    item["old_{0}_password".format(old_app_id)] = item.get("password")
                    item["old_{0}_password".format(new_app_id)] = obj.get("password")
                    item["old_{0}_userid".format(old_app_id)] = user_id
                    item["old_{0}_userid".format(new_app_id)] = user_id
                    self[index] = item
                elif obj.get("user_id") not in self.get("user_id"):
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
                    row[key] = ""
                list.append(row[key])
            vals.append(list)
        return vals


@view_config(name="csv", context=Container, renderer="csv")
def merged_csv(context, request):
    headers = ["app_id", "municipality_id", "user_id", "fullname", "email", "password"]
    rows = UserList()
    for app_id, app in context.items():
        for user_id, user in app.data.items():
            new_user = {}
            new_user["municipality_id"] = context.__name__
            new_user["app_id"] = app_id
            new_user["user_id"] = user.get("content_id").lower()
            for head in headers:
                if not new_user.get(head, ""):
                    new_user[head] = user.get(head)
            rows.add_or_merge(new_user)
    filename = f"{context.__name__}.csv"
    request.response.content_disposition = "attachment;filename=" + filename
    return {"header": rows.keys(), "rows": rows.values()}


@view_config(name="json", request_method="GET", context=Container, renderer="json")
def get_json(context, request):
    retrieve = context.retrieve()
    if retrieve is None:
        raise HTTPNotFound()
    result = {}
    users = []
    for app_id, app in context.items():
        if isinstance(app, Content):
            raise HTTPNotFound()
        for user_id, user in app.data.items():
            juser = {}
            locality_slug = user.get("mun_slug")
            juser["username"] = user.get("username")
            juser["uuid"] = ""
            juser["first_name"] = ""
            juser["last_name"] = ""
            juser["email"] = user.get("email")
            juser["password"] = user.get("password")
            juser["allowed_services"] = user.get("allowed_services")
            users.append(juser)
    result["users"] = users
    locality = {}
    locality["name"] = context.__name__
    locality["slug"] = locality_slug
    result["locality"] = locality
    services = []
    service = {}
    service["name"] = "{0} {1}".format(
        context.__name__, app_id.lower().replace(".", "")
    )
    service["slug"] = "{0}-{1}".format(
        context.__name__, app_id.lower().replace(".", "")
    )
    service["client_id"] = ""
    service["client_secret"] = ""
    service["redirect_uris"] = []
    service["post_logout_redirect_uris"] = []
    service["frontchannel_logout_uri"] = ""
    service["open_to_all"] = False
    services.append(service)
    result["services"] = services
    return result
