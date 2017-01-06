from functools import wraps

from django.http import HttpResponse


class ValidateRole(object):
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, function):
        @wraps(function)
        def wrapped(request, *args, **kwargs):
            print self.roles
            if request.user.profile.get_type() not in self.roles:
                return HttpResponse('You are not allowed to do this operation.')
            return function(request, *args, **kwargs)

        return wrapped
