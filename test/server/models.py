import pytz
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


def datetime_now_tz():
    return datetime.utcnow().replace(tzinfo = pytz.utc)


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


class Comment(Model):
    content = models.TextField(
    )
    post = models.ForeignKey(
        Post
    )
    user = models.ForeignKey(
        User
    )
