import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from lib import json
from models import Tag, User, Post, Comment


FIXTURES = (
      'tags'
    , 'users'
    , 'posts'
    , 'comments'
)

class T(TestCase):

    fixtures = FIXTURES


class PersmissionT(T):

    def test_create(self):

        self.client = Client()
        self.client.login(username='jd', password='test')

        data = {'post': {
            'title': 'New Book',
            'content': ' ',
            'user_id': '1'
        }}
        uri = reverse('apis:posts')
        res = self.client.post(uri, json.dumps(data), 'application/json')
        self.assertEqual(res.status_code, 403)
        posts = Post.objects.all()
        # assert no new post was created
        self.assertEqual(posts.count(), 3)


class FieldT(T):

    def setUp(self):
        self.client = Client()
        self.client.login(username='tj', password='test')

    def test_foreign(self):
        post = Post.objects.all()[0]
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post_data = data['post']
        self.assertEqual(post_data['id'], post.pk)
        self.assertEqual(post_data['user_id'], post.user.pk)

    def test_image(self):
        post = Post.objects.get(pk=1)
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post_data = data['post']
        self.assertEqual(post_data['id'], post.pk)
        self.assertEqual(post_data['image'], '/media/posts/image.png')

        post = Post.objects.get(pk=2)
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post_data = data['post']
        self.assertEqual(post_data['id'], post.pk)
        self.assertEqual(post_data['image'], '')


class ApiT(T):

    def setUp(self):
        self.client = Client()
        self.client.login(username='tj', password='test')

    def test_all(self):
        uri = reverse('apis:posts')
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data.keys()[0], 'posts')
        self.assertEqual(len(data['posts']), 3)

    def test_create(self):
        data = {'post': {
            'title': 'New Book',
            'content': '',
            'user_id': '1'
        }}
        uri = reverse('apis:posts')
        res = self.client.post(uri, json.dumps(data), 'application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post = Post.objects.latest('pk')
        self.assertEqual(post.pk, data['post']['id'])
        self.assertEqual(post.title, data['post']['title'])
        self.assertEqual(post.content, data['post']['content'])
        self.assertEqual(post.user.pk, data['post']['user_id'])

    def test_one(self):
        post = Post.objects.all()[0]
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data.keys()[0], 'post')
        post_data = data['post']
        self.assertEqual(post_data['id'], post.pk)
        self.assertEqual(post_data['title'], post.title)
        self.assertEqual(post_data['content'], post.content)
        self.assertEqual(post_data['user_id'], post.user.pk)

    def test_update(self):
        post = Post.objects.all()[0]
        data = {'post': {
            'title': 'New Book',
            'content': '',
            'user_id': '1'
        }}
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.put(uri, json.dumps(data), 'application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post = Post.objects.get(pk=post.pk)
        self.assertEqual(post.pk, data['post']['id'])
        self.assertEqual(post.title, data['post']['title'])
        self.assertEqual(post.content, data['post']['content'])
        self.assertEqual(post.user.pk, data['post']['user_id'])

    def test_remove(self):
        post = Post.objects.all()[0]
        uri = reverse('apis:post', kwargs={
            'pk': post.pk
        })
        res = self.client.delete(uri)
        self.assertEqual(res.status_code, 200)
        try:
            post = Post.objects.get(pk=post.pk)
        except Post.DoesNotExist:
            pass
        else:
            raise Exception('record still exists')


class QueryT(T):

    uri = reverse('apis:posts')

    def test_filter(self):
        data = {
            'query': {
                'filter': {
                    'user__pk': 1
                }
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        # assert returns 2/3 matched posts
        self.assertEqual(len(data['posts']), 2)

    def test_exclude(self):
        data = {
            'query': {
                'exclude': {
                    'user__pk': 1
                }
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        # assert returns 1/3 matched posts
        self.assertEqual(len(data['posts']), 1)

    def test_order_by(self):
        data = {
            'query': {
                'order_by': '-title'
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        posts = data['posts']
        self.assertEqual(posts[0]['title'], 'c')
        self.assertEqual(posts[1]['title'], 'b')
        self.assertEqual(posts[2]['title'], 'a')

        data = {
            'query': {
                'order_by': 'title'
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        posts = data['posts']
        self.assertEqual(posts[0]['title'], 'a')
        self.assertEqual(posts[1]['title'], 'b')
        self.assertEqual(posts[2]['title'], 'c')

    def test_limit(self):
        data = {
            'query': {
                'limit': [0, 1]
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        # assert returns 1/3 matched posts
        self.assertEqual(len(data['posts']), 1)

        data = {
            'query': {
                'limit': [0, 2]
            }
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        # assert returns 2/3 matched posts
        self.assertEqual(len(data['posts']), 2)

    def test_count(self):
        data = {
            'query': 'count'
        }
        res = self.client.post(
            self.uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Post.objects.count(), int(res.content))

        uri = reverse('apis:comments')
        data = {
            'query': 'count'
        }
        res = self.client.post(
            uri, json.dumps(data), 'application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Comment.objects.count(), int(res.content))

class RelationsT(T):

    def setUp(self):
        self.client = Client()
        self.client.login(username='tj', password='test')

    def test_has_many_fields_are_added_to_json_outputs(self):
        user = User.objects.get(pk=1)
        uri = reverse('apis:user', kwargs={
            'pk': user.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        user_data = data['user']
        self.assertEqual(user_data['id'], user.pk)

        user = User.objects.get(pk=2)
        uri = reverse('apis:user', kwargs={
            'pk': user.pk
        })
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        user_data = data['user']
        self.assertEqual(user_data['id'], user.pk)

    def test_dependant_records_are_deleted_on_delete(self):
        user = User.objects.get(pk=1)
        uri = reverse('apis:user', kwargs={
            'pk': user.pk
        })
        res = self.client.delete(uri)
        self.assertEqual(res.status_code, 200)

        # assert no post exists
        self.assertEqual(Post.objects.all().count(), 1)
        # assert non dependencies are not affected
        self.assertEqual(Tag.objects.all().count(), 2)
        self.assertEqual(Comment.objects.all().count(), 2)
