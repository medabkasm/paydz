from functools import wraps
from accounts.models import User
from django.shortcuts import  redirect


def profile_done(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        if request.user.is_authenticated:
            if user.profile.profileComplete:
                return function(request, *args, **kwargs)
            else:
                return redirect("profiles:password_set",request.user.username)
        else:
            return function(request, *args, **kwargs)

    return wrap
