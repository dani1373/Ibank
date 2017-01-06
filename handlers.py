from functools import wraps

from django.http import HttpResponseRedirect


class ValidateRole(object):
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, function):
        @wraps(function)
        def wrapped(request, *args, **kwargs):
            if request.user.profile.get_type() not in self.roles:
                return HttpResponseRedirect('/')
            return function(request, *args, **kwargs)

        return wrapped
