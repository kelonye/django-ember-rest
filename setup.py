#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-ember-rest',
    version='0.1.3',
    description='Django Models <> Ember-Data',
    author='Mitchel Kelonye',
    author_email='kelonyemitchel@gmail.com',
    url='https://github.com/kelonye/django-ember-rest',
    requires=['Django (>=1.3.0)'],
    packages=['django_ember_rest',],
    package_dir = {'django_ember_rest': 'lib'},
    license='MIT License',
    zip_safe=True
)