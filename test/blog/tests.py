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
