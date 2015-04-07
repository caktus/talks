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

## Requirements

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

Notes:
This is the end of 1-project-setup tag

@@

## HTTP Tester Demo

```bash
(smsdemo) $ python manage.py runserver
```

Go to http://localhost:8000/httptester/

@@

## First SMS App

```bash
(smsdemo) $ python manage.py startapp smsgroups
```

@@

## Group Model

```python
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from rapidsms.models import Contact

@python_2_unicode_compatible
class Group(models.Model):
    """Group of SMS users for broadcasting messages."""

    slug = models.SlugField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Group %s' % self.slug
```


## Member Model

```python
...
@python_2_unicode_compatible
class Member(models.Model):
    """Member of an SMS group."""

    contact = models.ForeignKey(Contact)
    group = models.ForeignKey(Group)
    is_creator = models.BooleanField(default=False, blank=True)
    joined_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s/%s' % (self.group, self.contact)
```

@@

## Migrate Database

Add `'smsgroups'` to  `INSTALLED_APPS`

```bash
(smsdemo) $ python manage.py makemigrations smsgroups
(smsdemo) $ python manage.py migrate smsgroups
```

Notes:
This is the end of 2-data-model tag

@@

## Create Groups via SMS

```python
from __future__ import unicode_literals

from django.db import transaction
from django.utils.crypto import get_random_string

from rapidsms.contrib.handlers import PatternHandler
from rapidsms.models import Contact

from ..models import Group, Member

class CreateHandler(PatternHandler):
    pattern = 'create'

    def handle(self):
        """Create a new group."""
        ...
```


```
def handle(self):
    created = False
    while not created:
        slug = get_random_string(
            length=10, allowed_chars='01234567890')
        with transaction.atomic():
            group, created = Group.objects.get_or_create(slug=slug)
            if created:
                connection = self.msg.connections[0]
                contact = connection.contact
                if not contact:
                    contact = Contact.objects.create(name='')
                    connection.contact = contact
                    connection.save(update_fields=('contact', ))
                Member.objects.create(
                    contact=contact, group=group, is_creator=True)
    reply = (
        'Group "%(slug)s" created! '
        'Use this identifier to SEND msgs or for others to JOIN.'
    ) % {'slug': slug}
    self.respond(reply)
```

Notes:
This is the end of 3-create-groups tag

@@

## Create Group Demo

```bash
(smsdemo) $ python manage.py runserver
```

Go to http://localhost:8000/httptester/

@@

## Join Groups via SMS

```python
from __future__ import unicode_literals

from django.db import transaction

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.models import Contact

from ..models import Group, Member

class JoinHandler(KeywordHandler):
    keyword = 'join'

    def handle(self, text):
        """Join an existing group."""
        ...

    def help(self):
        """Handle message which is missing the slug parameter."""
        ...
```


```python
def help(self):
    self.respond('To join a group, send JOIN <id> for an existing group.')
```


```python
def handle(self, text):
    try:
        group = Group.objects.get(slug=text.strip())
    except Group.DoesNotExist:
        self.respond('Unknown group id "%s"' % text.strip())
    else:
        ...
```


```python
def handle(self, text):
    ...
    else:
        with transaction.atomic():
            connection = self.msg.connections[0]
            contact = connection.contact
            if not contact:
                contact = Contact.objects.create(name='')
                connection.contact = contact
                connection.save(update_fields=('contact', ))
            _, created = Member.objects.get_or_create(
                contact=contact, group=group,
                defaults={'is_creator': False})
            if created:
                reply = 'You are now a member.'
            else:
                reply = 'You are already a member.'
            reply = '%s SEND msgs the group by using the "%s:" prefix.' % (
                reply, group.slug)
            self.respond(reply)
```

Notes:
This is the end of 4-join-groups tag

@@

## Join Group Demo

```bash
(smsdemo) $ python manage.py runserver
```

Go to http://localhost:8000/httptester/

@@
