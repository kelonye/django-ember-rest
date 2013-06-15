import unittest
from django.test import TestCase
from django.test.client import Client


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

    def test_get_all(self):
        uri = reverse('rest:posts')
        res = self.client.get(uri)
        self.assertEqual(res.status_code, 200)
