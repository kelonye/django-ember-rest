import re
import simplejson as json
from django.conf import settings
from django.core import serializers
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, include, url
from django.db.models.fields.files import FieldFile
from django.db.models.fields.related import ForeignKey
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect


class Permission:
    def __init__(self, model, attr):
        if not getattr(model, attr, None):
            opts = (model.__name__, attr)
            raise Exception(
                'please implement %s.%s(self, req)' % opts
            )


class Field:

    def __init__(self, name, field):
        self.name = name
        self.field = field

    @property
    def underscored_name(self):
        return self.name.replace(' ', '_')
    
    @property
    def belongs_to_name(self):
        return self.underscored_name + '_id'


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
            Permission(self.model, attr)

    @property
    def name(self):
        return re.sub('(?!^)([A-Z]+)', r'_\1', self.model.__name__).lower()

    @property
    def plural_name(self):
        plural_name = getattr(self.cls, 'plural_name', None)
        if not plural_name:
            plural_name = self.name + 's'
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

    @property
    def field_list(self):
        for field_name in self.fields:
            field = self.model._meta.get_field(field_name)
            yield Field(field_name, field)

    def item_to_JSON(self, item):
        
        items_string = serializers.serialize('json', [item], fields=self.fields)
        items_json = json.loads(items_string)
        item_json = items_json[0]
        item_data = item_json['fields']
        item_data['id'] = item_json['pk']

        for field in self.field_list:

            if isinstance(field.field, ForeignKey):
                pk = item_data[field.underscored_name]
                item_data[field.belongs_to_name] = pk
                del item_data[field.underscored_name]

            elif isinstance(field.field, FieldFile):
                file_path = item_data[field.name]
                item_data[field.underscored_name] = settings.MEDIA_URL + file_path
                del item_data[field.name]

        return item_data

    # GET /`model`/
    @csrf_exempt
    def all(self, req):

        if req.method == 'POST':
            return self.create(req)

        def get_items_json():
            items = self.model.objects.all()
            for item in items:
                is_readable = item.__is_readable__(req)
                if not isinstance(is_readable, HttpResponse):
                    yield self.item_to_JSON(item)

        json_data = {}
        json_data[self.plural_name] = [ i for i in get_items_json() ]

        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

    # METHOD /`model`/`pk`/
    @csrf_exempt
    def one(self, req, pk):

        if req.method == 'PUT':
            return self.update(req, pk)
        elif req.method == 'DELETE':
            return self.remove(req, pk)
        else:
            return self.find(req, pk)

    # GET /`model`/`pk`/
    def find(self, req, pk):
        item = self.model.objects.get(pk=pk)
        is_readable = item.__is_readable__(req)
        if isinstance(is_readable, HttpResponse):
            res = is_readable
            return res
        json_data = {}
        json_data[self.name] = self.item_to_JSON(item)
        return HttpResponse(
            json.dumps(json_data), content_type='application/json'
        )

    # POST /`model`/
    def create(self, req):

        item = self.model()
        self.__update__(req, item)
        
        # note, __is_creatable__ should override any set attributes
        is_creatable = item.__is_creatable__(req)
        if isinstance(is_creatable, HttpResponse):
            res = is_creatable
            return res

        item.save()

        return self.find(req, item.pk)

    # PUT /`model`/`pk`/
    def update(self, req, pk):
        
        item = self.model.objects.get(pk=pk)
        self.__update__(req, item)

        is_updatable = item.__is_updatable__(req)
        if isinstance(is_updatable, HttpResponse):
            res = is_updatable
            return res

        item.save()

        return self.find(req, pk)

    # DELETE /`model`/`pk`/
    def remove(self, req, pk):
        return HttpResponse(json.dumps('{}'))


    def __update__(self, req, item):

        data = json.loads(req.body)[self.name]

        for field in self.field_list:

            if isinstance(field.field, ForeignKey):
                pk = data[field.belongs_to_name]
                model = field.field.rel.to
                value = model.objects.get(pk=pk)
            else:
                value = data[field.underscored_name]
            
            setattr(item, field.name, value)

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
