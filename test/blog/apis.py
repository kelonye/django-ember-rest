from django_ember_rest import Apis
from models import Tag, User, Post, Comment

class TagApi:
    model = Tag
    fields = (
        'name',
        'post',
        'user',
    )


class UserApi:
    model = User
    fields = (
        'username',
    )

class PostApi:
    model = User
    fields = (
        'title',
        'content',
        'user',
    )

class CommentApi:
    model = User
    fields = (
        'content',
        'post',
        'user',
    )

apis = Apis(
    TagApi,
    UserApi,
    PostApi,
    CommentApi
)

# apis = Apis()
# apis.append(TagApi)
# apis.append(UserApi)
# apis.append(PostApi)
# apis.append(CommentApi)