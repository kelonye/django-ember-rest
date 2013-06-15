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

class UserApi(Api):
    model = User
    fields = [
        'username'
    ]

class ModelApi(Api):
    model = Model
    fields = [
        'name',
        'content'
    ]

apis = Apis(UserApi, ModelApi)

urlpatterns = patterns('',
    url(r'^', include(apis.urls)),
)

```

Licence
---

MIT