Install
---

    $ pip install django-ember-rest

Use
---

```

from django_ember_rest import Apis

class Model:
    ...
    def __is_creatable__(self, req):
        return HttpResponse(status=403)
    def __is_readable__(self, req):
        return
    def __is_updatable__(self, req):
        return HttpResponse(status=403)
    def __is_removable__(self, req):
        return HttpResponse(status=403)

apis = Apis(User, Model, ...)

urlpatterns = patterns('',
    url(r'^', include(apis.urls)),
)

```

Licence
---

MIT