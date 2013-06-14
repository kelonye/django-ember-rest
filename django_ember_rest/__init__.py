import re
import simplejson as json
from django.core import serializers
from django.http import HttpResponse
from django.db.models.fields.related import ForeignKey
from django.conf.urls.defaults import patterns, include, url


class Api:
    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        return re.sub('(?!^)([A-Z]+)', r'_\1', self.model.__name__).lower()

    @property
    def urls(self):
        return [
            url(r'^%ss/$' % self.name, self.all),
            url(r'^%ss/(?P<pk>\d+)/$' % self.name, self.one),
        ]

    def json(self, data):
        item = data['fields']
        item['id'] = data['pk']
        for field in self.model._meta.fields:
            if type(field) == ForeignKey:
                belongsTo = field.verbose_name.replace(' ', '_')
                item[belongsTo + '_id'] = item[belongsTo]
                del item[belongsTo]
        return item

    # GET /`model`/
    def all(self, req):
        items = self.model.objects.all()
        items_json = []
        for item in items:
            if not isinstance(item.__is_readable__(req), HttpResponse):
                string_data = serializers.serialize('json', [item])
                items_json.append(
                    self.json(json.loads(string_data)[0])
                )
        json_data = {}
        json_data['%ss' % self.name] = items_json
        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

    # GET /`model`/`pk`/
    def one(self, req, pk):
        item = self.model.objects.get(pk=pk)
        res = item.__is_readable__(req)
        if isinstance(res, HttpResponse):
            return res
        string_data = serializers.serialize('json', [item])
        json_data = {}
        json_data[self.name] = self.json(json.loads(string_data)[0])
        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

class Apis(list):

    def __init__(self, *args):
        super(list, self).__init__([])
        for model in args:

            for attr in [
                '__is_readable__'
            ]:

                if not getattr(model, attr, None):
                    raise Exception(
                        'please implement %s.%s(self, req)' % (
                            model.__name__,
                            attr
                        )
                    )

            for url in Api(model).urls:
                self.append(url)

    @property
    def urls(self):
        return patterns('',
            *self
        )
