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


class UserApi:
    model = User
    fields = ()
        'username'
    )
    plural_name = 'people' # custom plural name

class ModelApi:
    model = Model
    fields = (
          'name'
        , 'content'
    )

apis = Apis(UserApi, ModelApi)

urlpatterns = patterns('',
    url(r'^', include(apis.urls)),
)

```

Licence
---

MIT