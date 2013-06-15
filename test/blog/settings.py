import os

APPLICATION = os.environ.get('DJANGO_APPLICATION_NAME')

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')
)

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s.sqlite3' % APPLICATION,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    ('test', 'test@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

TIME_ZONE = 'Africa/Nairobi'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = '%s/public/media/' % PROJECT_ROOT

MEDIA_URL = '/media/'

STATIC_ROOT = '%s/public/static/' % PROJECT_ROOT

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'test secret'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    '%s/%s/templates/' % (PROJECT_ROOT, APPLICATION)
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = '%s.urls' % APPLICATION

WSGI_APPLICATION = '%s.wsgi.application' % APPLICATION

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
)
