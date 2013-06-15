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
    model = Post
    fields = (
        'title',
        'content',
        'user',
    )

class CommentApi:
    model = Comment
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