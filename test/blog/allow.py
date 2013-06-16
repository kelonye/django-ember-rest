# auth methods

from django.http import HttpResponse

def superuser(self, req):
    user = req.user
    if not user or not user.is_superuser:
        return HttpResponse(status=403)
    self.user = user
    return

def owner(self, req):
    user = req.user
    if not user or self.user != user:
        return HttpResponse(status=403)
    self.user = user
    return

def anyone(self, req):
    return

def none(self, req):
    return HttpResponse(status=403)
