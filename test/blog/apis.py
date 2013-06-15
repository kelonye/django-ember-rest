from django_ember_rest import Apis
from models import Tag, User, Post, Comment

apis = Apis(
       ( Tag, (
        'name',
        'post',
        'user',
    )),( User, (
        'username',
    )),( Post, (
        'title',
        'user',
    )),( Comment, (
        'content',
        'post',
        'user',
    ))
)