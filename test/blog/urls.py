from django_ember_rest import patterns, include, url
from apis import apis

urlpatterns = patterns('',
    url(r'^', include(apis.urls, namespace='apis')),
)