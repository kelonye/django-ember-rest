from models import Tag, User, Post, Comment
from lib import Api, Apis
import allow


class TagApi(Api):
    model = Tag
    fields = (
        'name',
        'post',
        'user',
    )

    __is_creatable__ = allow.owner
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.owner
    __is_removable__ = allow.superuser


class UserApi(Api):
    model = User
    fields = (
        'username',
    )

    __is_creatable__ = allow.none
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.none
    __is_removable__ = allow.superuser

class PostApi(Api):
    model = Post
    fields = (
        'title',
        'content',
        'user',
        'image'
    )

    __is_creatable__ = allow.superuser
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.superuser
    __is_removable__ = allow.superuser

class CommentApi(Api):
    model = Comment
    fields = (
        'content',
        'post',
        'user',
    )

    __is_creatable__ = allow.owner
    __is_readable__ = allow.anyone
    __is_updatable__ = allow.owner
    __is_removable__ = allow.superuser


urls = Apis(
    TagApi,
    UserApi,
    PostApi,
    CommentApi
)