import unittest
import simplejson as json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import Tag, User, Post, Comment


FIXTURES = (
      'tags'
    , 'users'
    , 'posts'
    , 'comments'
)


class MethodT(TestCase):

    fixtures = FIXTURES

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
        self.assertEqual(len(data['posts']), 2)

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

    def test_create(self):
        data = {
            'title': 'New Book',
            'content': ' ',
            'user_id': '1'
        }
        uri = reverse('apis:posts')
        res = self.client.post(uri, data)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        post = Post.objects.latest('pk')
        self.assertEqual(post.pk, data['post']['id'])
        self.assertEqual(post.title, data['post']['title'])
        self.assertEqual(post.content, data['post']['content'])
        self.assertEqual(post.user.pk, data['post']['user_id'])

class PersmissionsT:

    def test_create(self):

        self.client = Client()
        self.client.login(username='jd', password='test')

        data = {
            'title': 'New Book',
            'content': ' ',
            'user_id': '1'
        }
        uri = reverse('apis:posts')
        res = self.client.post(uri, data)
        self.assertEqual(res.status_code, 403)
        posts = Post.objects.all()
        # assert no new post was created
        self.assertEqual(posts.count(), 2)