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

## Adding Handlers

```bash
(smsdemo) $ mkdir smsgroups/handlers
(smsdemo) $ touch smsgroups/handlers/__init__.py
```

@@

## Create Groups via SMS

```bash
(smsdemo) $ touch smsgroups/handlers/create_group.py
```


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

@@

## Register Handler

```python
...
RAPIDSMS_HANDLERS = (
    'smsgroups.handlers.create_group.CreateHandler',
)
...
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

```bash
(smsdemo) $ touch smsgroups/handlers/join_group.py
```


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

@@

## Register Handler

```python
...
RAPIDSMS_HANDLERS = (
    'smsgroups.handlers.create_group.CreateHandler',
    'smsgroups.handlers.join_group.JoinHandler',
)
...
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

## Group Messages

```bash
(smsdemo) $ touch smsgroups/handlers/msg_group.py
```


```python
from __future__ import unicode_literals

from rapidsms.contrib.handlers import PatternHandler
from rapidsms.models import Contact, Connection
from rapidsms.router import send

from ..models import Group

class BroadcastHandler(PatternHandler):
    pattern = '^([0-9]{10}):\s?(\S+)'

    def handle(self, slug, text):
        """Broadcast messages to users in a group."""
        ...
```


```
def handle(self, slug, text):
    try:
        group = Group.objects.get(slug=slug)
    except Group.DoesNotExist:
        self.respond('Unknown group id "%s"' % slug.strip())
    else:
        ...
```


```
def handle(self, slug, text):
    ...
    else:
        # Check for membership
        connection = self.msg.connections[0]
        contacts = Contact.objects.filter(member__group=group)
        if not contacts.filter(connection__pk=connection.pk):
            self.respond('You are not a member of this group.')
        else:
            connections = Connection.objects.filter(
                contact__in=contacts, backend=connection.backend,
            ).exclude(pk=connection.pk)
            count = connections.count()
            if count:
                send('From %s: %s' % (slug, text), connections=connections)
            self.respond('Message was sent to %s member%s.' % (
                count, count != 1 and 's' or ''))
```

@@

## Register Handler

```python
...
RAPIDSMS_HANDLERS = (
    'smsgroups.handlers.create_group.CreateHandler',
    'smsgroups.handlers.join_group.JoinHandler',
    'smsgroups.handlers.msg_group.BroadcastHandler',
)
...
```

Notes:
This is the end of 5-group-messages tag

@@

## Message Group Demo

```bash
(smsdemo) $ python manage.py runserver
```

Go to http://localhost:8000/httptester/

@@

## Automated Testing

```bash
(smsdemo) $ mkdir smsgroups/tests
(smsdemo) $ touch smsgroups/tests/__init__.py
(smsdemo) $ mv smsgroups/tests.py smsgroups/tests/test_handlers.py
```


```python
from __future__ import unicode_literals

from django.test import TestCase

from ..handlers.create_group import CreateHandler
from ..models import Group

class CreateHandlerTestCase(TestCase):
    """Create new SMS group."""

    def test_create_group(self):
        """Create a new group with the CREATE command."""

        replies = CreateHandler.test('CREATE')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        group = Group.objects.latest('pk')
        self.assertIn('Group "%s" created!' % group.slug, replies[0])
        self.assertEqual(group.member_set.count(), 1)
```

@@

## PASSED!

```bash
(smsdemo) $ python manage.py test smsgroups
Creating test database for alias 'default'...
.
----------------------------------------------------------------------
Ran 1 test in 0.058s

OK
Destroying test database for alias 'default'...
```

Notes:
This is the end of 6-initial-testing tag

@@

## More Testing

```bash
(smsdemo) $ pip install mock
```


```python
...
class CreateHandlerTestCase(TestCase):
    """Create new SMS group."""
    ...

class JoinHandlerTestCase(TestCase):
    """Join an existing SMS group."""
    ...

@mock.patch('smsgroups.handlers.msg_group.send')
class BroadcastHandlerTestCase(TestCase):
    """Send message to other members of a group."""
    ...
```


```python
class JoinHandlerTestCase(TestCase):

    def setUp(self):
        self.group = Group.objects.create(slug='1234567890')

    def test_join_group(self):
        """Join group with the JOIN command."""

        replies = JoinHandler.test('JOIN %s' % self.group.slug)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertIn('You are now a member.', replies[0])
        self.assertEqual(self.group.member_set.count(), 1)
```


```python
    def test_help(self):
        """If group ID is missing then show the HELP message."""

        replies = JoinHandler.test('JOIN')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual(
            'To join a group, send JOIN <id> for an existing group.',
            replies[0])

    def test_unknown_group(self):
        """Handle invalid group IDs."""

        slug = self.group.slug
        self.group.delete()
        replies = JoinHandler.test('JOIN %s' % self.group.slug)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Unknown group id "%s"' % slug, replies[0])
```


```python
    def test_already_joined(self):
        """Handle a user which has already joined the group."""

        JoinHandler.test('JOIN %s' % self.group.slug, identity='abcxyz')
        replies = JoinHandler.test(
            'JOIN %s' % self.group.slug, identity='abcxyz')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertIn('You are already a member.', replies[0])
        self.assertEqual(self.group.member_set.count(), 1)
```


```python
@mock.patch('smsgroups.handlers.msg_group.send')
class BroadcastHandlerTestCase(TestCase):
    """Send message to other members of a group."""

    def setUp(self):
        self.group = Group.objects.create(slug='1234567890')
        self.backend = Backend.objects.create(name='test_backend')
        self.test_contact = Contact.objects.create(name='test')
        self.test_connection = Connection.objects.create(
            identity='test', backend=self.backend,
            contact=self.test_contact)
        self.test_member = Member.objects.create(
            group=self.group, contact=self.test_contact)
        self.other_contact = Contact.objects.create(name='other')
        self.other_connection = Connection.objects.create(
            identity='other', backend=self.backend,
            contact=self.other_contact)
        self.other_member = Member.objects.create(
            group=self.group, contact=self.other_contact)
        BroadcastHandler._mock_backend = self.backend
```


```python
    def test_send_message(self, mock_send):
        """Send messages to the other user in the group."""

        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug,
            identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Message was sent to 1 member.', replies[0])
        self.assertTrue(mock_send.called)
        args, kwargs = mock_send.call_args
        self.assertEqual(args, ('From %s: hello' % self.group.slug, ))
        recipients = kwargs['connections']
        self.assertItemsEqual(recipients, [self.other_connection, ])
```


```python
    def test_unknown_group(self, mock_send):
        """Handle unknown group."""

        replies = BroadcastHandler.test(
            '0987654321: hello',
            identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Unknown group id "0987654321"', replies[0])
        self.assertFalse(mock_send.called)

    def test_not_a_member(self, mock_send):
        """Handle message from user not in the group."""

        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug, identity='unknown')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('You are not a member of this group.', replies[0])
        self.assertFalse(mock_send.called)
```


```python
    def test_no_other_members(self, mock_send):
        """Handle group with only one memember."""

        self.other_member.delete()
        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug,
            identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Message was sent to 0 members.', replies[0])
        self.assertFalse(mock_send.called)
```

@@

## SUCH TESTING!

```bash
(smsdemo) $ python manage.py test smsgroups
Creating test database for alias 'default'...
.........
----------------------------------------------------------------------
Ran 9 tests in 0.371s

OK
Destroying test database for alias 'default'...
```

Notes:
This is the end of 7-more-testing tag

@@

## Scripted Tests

