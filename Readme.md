Install
---

    $ pip install django-ember-rest
    $ component install kelonye/django-ember-rest

Use
---

```

# models

class Model(db.Models):
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


# apis

from django_ember_rest import Apis

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


# urls

apis = Apis(UserApi, ModelApi)

urlpatterns = patterns('',
    url(r'^', include(apis.urls)),
)

```

Then on client side, define your store as

```

App.Adapter = require('django-ember-rest').extend({
  namespace: 'api'
});

App.Store = DS.Store.extend({
  revision: DS.CURRENT_API_REVISION,
  adapter: 'App.Adapter'
});

```

Example
---
    
    $ make example


Test
---

    $ make test


Motivation
---

Frustration with `django-tastypie`

License
---

MIT