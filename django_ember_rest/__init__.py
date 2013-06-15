import re
import simplejson as json
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.db.models.fields.files import FieldFile
from django.db.models.fields.related import ForeignKey
from django.conf.urls.defaults import patterns, include, url


class Api:
    def __init__(self, model):
        for attr in [
            '__is_creatable__',
            '__is_readable__',
            '__is_updatable__',
            '__is_removable__'
        ]:
            if not getattr(model, attr, None):
                raise Exception(
                    'please implement %s.%s(self, req)' % (
                        model.__name__,
                        attr
                    )
                )

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

    def itemToJSON(self, item):
        data = json.loads(
            serializers.serialize('json', [item])
        )[0]
        item_json = data['fields']
        item_json['id'] = data['pk']
        for field in self.model._meta.fields:
            field_name = field.verbose_name
            # ForeignKey
            print field
            if type(field) == ForeignKey:
                belongsTo = field_name.replace(' ', '_')
                item_json[belongsTo + '_id'] = item_json[belongsTo]
                del item_json[belongsTo]
            # FileField, ImageField
            else:
                file_field = getattr(item, field_name, None)
                if isinstance(file_field, FieldFile):
                    file_path = item_json[field_name]
                    del item_json[field_name]
                    item_json[field_name.replace(' ', '_')] = settings.MEDIA_URL + file_path
        return item_json

    # GET /`model`/
    def all(self, req):
        items = self.model.objects.all()
        items_json = []
        for item in items:
            if not isinstance(item.__is_readable__(req), HttpResponse):
                items_json.append(self.itemToJSON(item))
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
        json_data = {}
        json_data[self.name] = self.itemToJSON(item)
        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

class Apis(list):

    def __init__(self, *args):
        super(list, self).__init__([])
        for model in args:
            api = Api(model)
            for url in api.urls:
                self.append(url)

    @property
    def urls(self):
        return patterns('',
            *self
        )
