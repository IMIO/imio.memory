from pyramid.view import notfound_view_config


@notfound_view_config(renderer='string')
def notfound_view(request):
    request.response.status = 404
    return 'This app id not found'
