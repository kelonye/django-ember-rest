import pytz
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import allow


def datetime_now_tz():
    return datetime.utcnow().replace(tzinfo = pytz.utc)


User.__is_creatable__ = allow.none
User.__is_readable__ = allow.anyone
User.__is_updatable__ = allow.none
User.__is_removable__ = allow.none


class Model(models.Model):
    date_created = models.DateTimeField(
        default=datetime_now_tz
    )
    date_updated = models.DateTimeField(
        default=datetime_now_tz
    )
    class Meta:
        abstract = True


class Post(Model):
    def generate_upload_path(model_instance, filename):
        return 'posts/%s/%s' % (
            model_instance.id,
            filename
        ) 
    title = models.CharField(
        max_length=10
    )
    content = models.TextField(
    )
    image = models.ImageField(
        upload_to=generate_upload_path,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User
    )
    
    __is_creatable__ = allow.superuser
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.superuser
    __is_removable__ = allow.superuser


class Tag(Model):
    name = models.CharField(
        max_length=10
    )
    post = models.ForeignKey(
        Post
    )
    user = models.ForeignKey(
        User
    )
    __is_creatable__ = allow.owner
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.owner
    __is_removable__ = allow.owner


class Comment(Model):
    content = models.TextField(
    )
    post = models.ForeignKey(
        Post
    )
    user = models.ForeignKey(
        User
    )
    __is_creatable__ = allow.owner
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.owner
    __is_removable__ = allow.owner