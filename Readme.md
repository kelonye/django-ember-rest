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
  namespace: ''
});

App.Store = DS.Store.extend({
  revision: DS.CURRENT_API_REVISION,
  adapter: 'App.Adapter'
});

```

Querying
---

The following query methods are supported:

- [filter](https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter)
- [exclude](https://docs.djangoproject.com/en/dev/ref/models/querysets/#exclude)
- [order_by](https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by)
- [limit](https://docs.djangoproject.com/en/dev/topics/db/queries/#limiting-querysets)

```javascript

// jquery

jQuery.ajax('/posts/', 'POST', {
  data: {
    query: {
        filter: {
            post__pk: 1
        },
        exclude: {
            user__pk: 1
        },
        order_by: 'title',
        limit: [50, 60]
    }
  }
}).then(function(json){
});


// ember-data

App.Post.find({
    filter: {
        post__pk: 1
    },
    exclude: {
        user__pk: 1
    },
    order_by: 'title',
    limit: [50, 60]
});

```

Example
---
  
    $ make deps example
    $ curl http://localhost:8000/users/
    $ curl http://localhost:8000/posts/
    $ curl http://localhost:8000/tags/
    $ curl http://localhost:8000/comments/


Test
---

    $ make deps test


Motivation
---

Frustration with `django-tastypie`

License
---

MIT