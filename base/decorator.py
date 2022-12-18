from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def unauthothenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allow_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allow_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse('You are not authorized on this site.')
        return wrapper_func
    return decorator


def admin_site_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'member':
            return redirect('member_logged_in')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func


