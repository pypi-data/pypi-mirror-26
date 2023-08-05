BACKEND = 'postgres'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pivot',
    }
}

INSTALLED_APPS = (
    'tests.pivot',
)

SITE_ID=1,

SECRET_KEY='secret'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)