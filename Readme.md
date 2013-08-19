Install
---

    $ pip install django-ember-rest
    $ component install kelonye/django-ember-rest

Use
---

```python

# apis.py

from django_ember_rest import Api, Apis

class UserApi(Api):
    # model
    model = User
    # fields
    fields = (
        'username',
    )
    # permissions
    def __is_creatable__(self, req, item):
        return HttpResponse(status=403)
    def __is_readable__(self, req, item):
        return
    def __is_updatable__(self, req, item):
        return HttpResponse(status=403)
    def __is_removable__(self, req, item):
        return HttpResponse(status=403)

class ModelApi:
    model = Model
    fields = (
        'name',
        'content',
    )
    ...

urls = Apis(UserApi, ModelApi)


# urls.py

from apis import urls

urlpatterns = patterns('',
    url(r'^', include(urls)),
)

```

Then on client side, define your store as

```javascript

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

jQuery.ajax({
    url: '/posts/',
    method: 'POST',
    dataType: 'json',
    data: JSON.stringify({ query: {
        filter: {
            post__pk: 1
        },
        exclude: {
            user__pk: 1
        },
        order_by: 'title',
        limit: [50, 60]
    }}),
    success: function(items){
        console.log(items);
    }
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