# auth methods

from django.http import HttpResponse

def superuser(self, req, item):
    user = req.user
    if not user or not user.is_superuser:
        return HttpResponse(status=403)
    return

def owner(self, req, item):
    user = req.user
    if not user or item.user != user:
        return HttpResponse(status=403)
    return

def anyone(self, req, item):
    return

def none(self, req, item):
    return HttpResponse(status=403)
