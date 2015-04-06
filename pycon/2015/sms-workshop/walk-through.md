## Project Repo

https://github.com/caktus/smsdemo

@@

## Fresh Start

```bash
$ mkvirtualenv smsdemo -p `which python2.7`
(smsdemo) $ pip install "Django>=1.7,<1.8"
(smsdemo) $ django-admin startproject smsdemo
(smsdemo) $ cd smsdemo
```

@@

## Additional Requirements

```bash
(smsdemo) $ pip install “rapidsms>=0.19.0,<0.20”
(smsdemo) $ pip install psycopg2 dj_database_url
```

@@

## Settings Updates

```python
...
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',
    '@w0^p@xah19_(o!*$vrvoh^7!)6)@_m=^0(2q&5$a==+b=&q$y')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'SECRET_KEY' not in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(';')
...
```


## Settings Updates (cont.)

```python
import dj_database_url
...
DATABASES = {
    'default': dj_database_url.config(default='postgres:///smsdemo'),
}
...
```


## Settings Updates (cont.)

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
```


## Settings Updates (cont.)

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'selectable',
    'rapidsms',
    'rapidsms.contrib.handlers',
    'rapidsms.contrib.messagelog',
)
...
if DEBUG:
    INSTALLED_APPS += (
        'rapidsms.backends.database',
        'rapidsms.contrib.httptester',
    )
```


## Settings Updates (cont.)

```python
INSTALLED_BACKENDS = {}
...
if DEBUG:
...
    INSTALLED_BACKENDS['message_tester'] = {
        'ENGINE': 'rapidsms.backends.database.DatabaseBackend',
    }
```


## Settings Updates (cont.)

```python
RAPIDSMS_HANDLERS = ()
...
if DEBUG:
...
    RAPIDSMS_HANDLERS += (
        'rapidsms.contrib.echo.handlers.echo.EchoHandler',
        'rapidsms.contrib.echo.handlers.ping.PingHandler',
    )
```

@@

## Updating URLs

```python
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rapidsms.views import dashboard

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', dashboard, name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    url(r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    # Third party URLs
    url(r'^selectable/', include('selectable.urls')),
]
```


## Updating URLs (cont.)

```python
...
if settings.DEBUG:
    urlpatterns += [
        url(r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    ]
```

@@

## Creating the Database

```bash
(smsdemo) $ createdb smsdemo -E UTF-8
(smsdemo) $ python manage.py migrate
(smsdemo) $ python manage.py createsuperuser
```

@@

## HTTP Tester Demo

```bash
(smsdemo) $ python manage.py runserver
```

Go to http://localhost:8000/httptester/
