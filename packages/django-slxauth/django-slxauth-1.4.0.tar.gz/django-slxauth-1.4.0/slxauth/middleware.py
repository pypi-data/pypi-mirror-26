from slxauth.utils import login_using_token


class TokenAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_authenticated():
            access_token = request.COOKIES.get('access_token')
            login_using_token(request, access_token)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

