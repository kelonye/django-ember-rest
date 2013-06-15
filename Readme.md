Install
---

    $ pip install django-ember-rest

Use
---

```

from django_ember_rest import Apis

class Model:
    ...
    # define model permissions
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
    fields = (
        'username',
    )
    # define custom plural name
    plural_name = 'people'

class ModelApi:
    model = Model
    fields = (
        'name',
        'content',
    )

apis = Apis(UserApi, ModelApi)

urlpatterns = patterns('',
    url(r'^', include(apis.urls)),
)

```

Example
---
    
    $ make example


Test
---

    $ make test


Licence
---

MIT