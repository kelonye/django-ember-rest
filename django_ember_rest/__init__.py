import re
import simplejson as json
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.conf.urls import patterns, include, url
from django.db.models.fields.files import FieldFile
from django.db.models.fields.related import ForeignKey

class Api:
    def __init__(self, cls):
        
        self.cls = cls
        self.model = cls.model
        self.fields = cls.fields

        for attr in [
            '__is_creatable__',
            '__is_readable__',
            '__is_updatable__',
            '__is_removable__'
        ]:
            if not getattr(self.model, attr, None):
                raise Exception(
                    'please implement %s.%s(self, req)' % (
                        self.model.__name__,
                        attr
                    )
                )

    @property
    def name(self):
        return re.sub('(?!^)([A-Z]+)', r'_\1', self.model.__name__).lower()

    @property
    def plural_name(self):
        plural_name = getattr(self.cls, 'plural_name', None)
        if not plural_name:
            plural_name = '%ss' % self.name
        return plural_name

    @property
    def urls(self):
        return [
            url(
                  r'^%s/$' % self.plural_name
                , self.all
                , name=self.plural_name
            ),
            url(
                  r'^%s/(?P<pk>\d+)/$' % self.plural_name
                , self.one
                , name=self.name
            ),
        ]

    def itemToJSON(self, item):
        data = json.loads(
            serializers.serialize('json', [item], fields=self.fields)
        )[0]
        item_json = data['fields']
        item_json['id'] = data['pk']
        for field_name in self.fields:
            field = getattr(item, field_name)
            # ForeignKey
            if getattr(field, 'pk', None):
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
        is_readable = item.__is_readable__(req)
        if isinstance(is_readable, HttpResponse):
            res = is_readable
            return res
        json_data = {}
        json_data[self.name] = self.itemToJSON(item)
        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

class Apis(list):

    def __init__(self, *args):
        super(list, self).__init__()

        for cls in args:
            api = Api(cls)
            for url in api.urls:
                self.append(url)

    @property
    def urls(self):
        return patterns('',
            *self
        )
