###Introduction to Celery

Caleb Smith
@@

## About Me
I work at Caktus Consulting Group LLC in Carrboro, NC

I mostly program Python and JavaScript

Sometimes C and Scheme.

I enjoy music theory and teaching

github: calebsmith

gitlab: csmith

twitter: @calebsmithnc
@@

## What is Celery
A distributed system for processing messages on a task queue with a focus on real-time processing and support for task scheduling.

This talk will give a high-level overview of Celery uses, setup choices, and early stumbling blocks

I will end with prescriptions
@@

### Major Features

Allows out of band processing, started periodically or trigged by web requests

Communicates with a message broker and distributes work

Can act as a cron job replacement

Can help ensure requests are timely

Reasonably good at distributed computing and high availability

Notes: Satisfies a common need reasonably well. Aims for the 90% case
@@

### Project History

Celery was initially released in 2009 with version 0.1

* 1.0 in 2010 Brings several important improvements

* 2.0 in 2010 Celery is no longer Django only. Lots of tools added

* 3.0 in 2012 Performance improvements and simplified API.
* 3.1 in 2013 Pickle serialization is deprecated. CLI programs are under the celery umbrella

Notes: Upgrading involves API changes, but they are well documented in "What's New" docs. 3.1 features will make more sense later
@@

### Boilerplate

```python
#project/celery.py
from celery import Celery
from django.conf import settings

app = Celery('appname', broker=settings.BROKER_URL)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
```

```bash
celery -A appname worker
```
@@

```python
from django.db import models

from thumbnail_utils import make_thumb

class UserPost(models.Model):
    THUMBNAIL_SIZES = [
        (100, 100),
    ]

    image = models.ImageField(upload_to='posts/')

    def save(self, *args, **kwargs):
        super(UserPost, self).save(*args, **kwargs)
        for size in self.THUMBNAIL_SIZES:
            make_thumb(self.image.path, size)
```
@@

```python
from django.db import models

from thumbnail_utils import make_thumb

class UserPost(models.Model):
    THUMBNAIL_SIZES = [
        (600, 400),
        (100, 100),
        (200, 200),
        (300, 300),
        (10, 10),
        (5, 5),
    ]

    ...
```
@@

```python
from django.db import models

from project.thumbnail_tasks import generate_thumbnails_task

class UserPost(models.Model):
    THUMBNAIL_SIZES = [
        ...
    ]

    image = models.ImageField(upload_to='posts/')

    def save(self, *args, **kwargs):
        super(UserPost, self).save(*args, **kwargs)
        generate_thumbnails_task.delay(self.image.path, sizes)
```
@@

```python
#thumbnail_tasks.py

from project.celery import app

from thumbnail_utils import make_thumb

@app.task
def generate_thumbnails_task(image_path, sizes):
    for size in sizes:
        make_thumb(image_path, size)
```
@@

### You Might Need Celery For

* Generating assets after upload
* Notifying a set of users when an event happens.
* Keeping a search index up to date
* Replacing cronjobs (backups, cleanup)
@@

## Many Setup Choices

* Uses a "Message Broker"
* Uses a "Result Backend" (or no result backend)
* Uses a concurrency solution (Multiprocessing or green threads)
@@

## The Role of the Message Broker and Choosing One
@@

##What is a Message Broker?

Stores tasks on queues. Allows workers on different processes/machines to produce and consume tasks

The broker stores data that answers the question "What work remains to be done?"
@@

### Celery Broker Support

Several brokers are supported. Mainly RabbitMQ and Redis.

RabbitMQ is the most robust solution

Notes: Some experimental ones include Beanstalk, MongoDB, CouchDB, AmazonSQS.
A project might already have Redis for other roles, but RabbitMQ has no caveats
@@

![Worker and Broker Interaction Diagram](images/broker.jpeg)

Notes:
There are some minor simplifications for the sake of clarity. Default settings are assumed
1. A task is put on the queue by a "producer" (celerybeat, a worker, or web process). It is on the queue in a "Ready" state
2. A celery "consumer" process takes the task from this queue. The consumer holds the task until a worker in the "worker pool" is free and it passes the task along. By default, a consumer holds 4 tasks in this buffer. At this point, the task is "PENDING"
If the celery consumer process stops unexpectidly, the consumer's tasks stay on the broker as unacknowledged messages and are retried when celery is available again
3. When a worker pool thread or process is ready, the consumer "acknowleges" the message by sending a request to the broker. The broker now knows the task is being run and removes it from the set of "unacknowledged" messages. As the task runs in the worker, it is "PENDING"
4. The task executes and enters a SUCCESS, FAILURE, or RETRY status after it finishes

Additional: There are also settings that can change many of these details.

More than one task can be put in the consumer's buffer if configured to do so with CELERY_PREFETCH_MULTIPLIER. The default is 4.

CELERY_ACKS_LATE means acknowledgement happens after task completion rather than when it enteres "STARTED"
@@

### RabbitMQ

Celery was created with RabbitMQ in mind.

RabbitMQ implements AMQP.

It tracks message acknowledgement.

Gross oversimplification: RabbitMQ is the PostgreSQL of message brokers

Notes:
If a consumer dies unexpectidly, unacknowledged messages are re-sent in their original order.

@@

###Redis Broker

Redis uses its pubsub capabilities with "ack emulation"
@@

###Redis Broker Caveats

If a consumer shuts down **gracefully**, messages are returned to redis as unacknowledged. Otherwise they are **gone forever**

Redis uses a timeout to determine successful delivery to a worker. This is called the "default visibility timeout"
@@

###Redis Broker Configuration

* Configure default visibility timeout carefully.
* Configure redis to avoid key eviction
@@

###Essence of the Redis Broker Distilled

You might process a task:

1. Correctly
2. Several hours late, in the wrong order
3. Twice or more
4. Never
@@

###Firetruck Contingency Plan

Multiple RabbitMQ nodes in a cluster with high availability queues for leader/follower replication

This offers redundancy but the cluster is not load balanced for performance
@@

### Broker Example
```python
#celery.py
app = Celery(broker=settings.BROKER_URL)

#settings.py
BROKER_URL = 'amqp://user:password@hostname:port/virtual_host'
#or for redis
BROKER_URL = 'redis://:password@hostname:port/db_number'
```
@@

##Choosing a Result Backend
@@

## What is a Result Backend

To track the state of a task and its return values when execution is finished a "result backend" is used.

Stores a mapping of: task id -> result

Each result backend has strengths, weaknesses, and caveats.
@@

### Result Backend In Action

```python
from project.celery import app

@app.task
def add(a, b):
    return a + b

>>> result = add.delay(2, 3)
>>> print(result.id)
'be1131cc-6537-4738-8aa0-ce8ca1b07fc9'
>>> print(result.state)
'SUCCESS'
>>> value = result.get(timeout=3)
>>> print(value)
5
```
@@

### Are you not impressed?
@@

### Database Backends

* django-celery comes with a DB backend. Also SQLAlchemy backend

* The database backends do offer a quick and simple "monitoring" solution and the periodic tasks are configurable in the DB

* Database backends can make tasks with high granularity very heavy

Notes: These offer monitoring solutions for simple cases and are useful in development, but Flower and other projects offer robust monitoring.
* Many other choices if needed: Riak, MongoDB, Cassandra, IronCache
@@

### AMQP Backend

AMQP backend spawns an Erlang process and a queue for each task, which is *very* expensive
@@

## Cache Result Backends

A key/value store is well suited as a result backend

A database, or RabbitMQ will "work"

A cache is a natural fit.
@@

### Result Backend Setup

```python
#settings.py
CELERY_RESULT_BACKEND = 'redis://:password@host:port/db'
```

@@

## Choosing a Concurrency Solution

Multiprocessing - running several celery worker processes

Green Threads - Running a process in which several workers take turns executing async I/O (event loop)

* prefork pool (multiprocessing)
* eventlet (green threads using epoll or libevent
* gevent (green threads using libev and c-ares)
@@

### Multiprocessing vs Green Threads

Green threads

* Offer some performance advantages, especially if tasks are short and mostly I/O

* Requires monkey patching. Might not work with your existing code and dependencies.

* Tasks must not use blocking I/O or *all* concurrency is lost. One thread "hogs the ball"
@@

### Multiprocessing vs Green Threads
Multiprocessing

* Recommended number of workers is n + 1 workers (n is number of cores)

* Uses more RAM
@@

### Concurrency Setup Example
```bash
celery worker -A appname -c 5
celery worker -A appname -P eventlet -c 1000
celery worker -A appname -P gevent -c 1000
```

Notes:
There are other process pools. Use `celery worker --help` for a list
@@

## Pitfalls

* Parallel Safety
* Poor Task Granularity
* Misguided Optimizations

@@

### Parallel Safety

Write tasks to be parallel safe.

You have no idea when tasks will run. Plan for this.

Trying to disaalow certain tasks from running in parallel is focusing on the wrong problem.

Use database transactions where needed

Don't pass objects as task parameters.
@@

```python
#tasks.py
from datetime import datetime

from project.celery import app
from project.utils import create_pdf_from_html

@app.task
def generate_pdf_report(report_id):
    report = Report.objects.get(id=report_id)
    if report.pdf_last_modified < report.html_last_modified:
        pdf_data = create_pdf_from_html(report.html)
        now = datetime.now()
        Report.objects.filter(id=report_id).update(
            pdf_data=pdf_data, pdf_last_modified=now)
```
@@

### A Note on Pickle

Pickle serialization allows for arbitrary Python objects as task parameters

You want **values**

Use JSON, YAML, or one of the other serialization methods.
@@

### Poor Task Granularity

Choose "right size" tasks.

Too big, task code is hard to read and maintain and takes many seconds, even minutes to run. Harder to scale horizontally. (Little or no concurrency)

Think "single responsibility principle".

Functions != tasks

Design tasks around small units that should execute simultaneously.
@@

### Poor Task Granularity Continued

Don't just "Parallel All the Things". Some problems are like frying an egg, inherently sequential, but more than one egg can fit in the pan.

Each task has a small, but not trivial storage and network cost.

With many tasks and a small worker pool, queues will fill with tasks.

Review CELERY_PREFETCH_MULTIPLIER

Consider building tasks into "chunks" (E.g. A task that writes 5 things to the DB)
@@

### Granularity Problem

```python
#tasks.py

from project.celery import app

from forum.utils import notify_user
from forum.models import ForumPost

@app.task
def notify_forum_users(post_id):
    post = ForumPost.objets.get(post_id)
    users = post.parent_thread.users.all()
    for user in users:
        notify_user(user)
```

@@

### Granularity Solution

```python
#tasks.py

from project.celery import app

from forum.utils import notify_user
from forum.models import ForumPost

@app.task
def notify_forum_users(post_id):
    post = ForumPost.objets.get(id=post_id)
    users = post.parent_thread.users.all()
    for user in users:
        notify_user_task.delay(user.id)

@app.task
def notify_user_task(user_id)
    user = User.objects.get(id=user_id)
    notify_user(user)
```

@@

### Premature Optimizations

Don't just turn the number of workers up without measuring. Too much concurrency and resources become constrained.

Like most code, network and storage I/O tend to be the bottleneck.

Profile code if it is slow. Look for slow DB queries, storage or network intensive work.

Look for configuration changes that offer an "easy win"

Refer to "Task Granularity".
@@

## Complete Example
```python
#tasks.py
from duckling.celery import app
from duckling.outings.models import Outing, Participant

@app.task
def send_announcement_tweet(outing_id):
    """Send a tweet announcing a new outing"""
    outing = Outing.objects.get(id=outing_id)
    message = outing.get_outing_announcement_tweet()
    tweet_task.delay(message)
```
@@

```python
#signals.py
from duckling.outings.tasks import send_announcement_tweet

@receiver(post_save, sender=Outing)
def announce_outing(instance, created, **kwargs):
    """Tweet about newly-created outings."""
    if created:
        send_announcement_tweet.delay(instance.id)
```
@@

```python
#tasks.py
from duckling.celery import app
from duckling.outings.models import Outing, Participant

@app.task
def send_reminder_tweets():
    """Send any unsent reminders to participants for upcoming outings"""
    outings = Outing.upcoming.all()
    for outing in outings.prefetch_related('participants'):
        participants = outing.participants.filter(allow_reminder=True, reminder_sent=False)
        for participant in participants:
            message = participant.get_reminder_tweet()
            tweet_task.delay(message, participant.id)
```
@@

```python
#settings.py
CELERYBEAT_SCHEDULE = {
    'send-outing-reminders': {
        'task': 'duckling.outings.tasks.send_reminders',
        'schedule': timedelta(minutes=5),
    },
}
```
@@

```python
#tasks.py
from duckling.clients.twitter_client import tweet

@app.task
def tweet_task(message, participant_id=None):
    """
    Sends a tweet. Retries sending on failure. Optionally takes a
    `participant_id` and marks reminder_sent on that participant if given
    """
    logger.debug('Sending tweet {0}'.format(message))
    success, response = tweet(message)
    if success:
        Participant.objects.filter(id=participant_id).update(
            reminder_sent=True)
    else:
        logger.debug('Error response {0}'.format(response.text))
        raise tweet_task.retry(countdown=30)
```
@@

## Prescriptions
@@

### Which Broker?

Use RabbitMQ if maintainng task data is important.
@@

### Which Result Backend?

You likely do not need one

Use a cache backend if you know you do.

Database Backends are helpful in development.
@@

###Which Concurrency Solution?

Use multiprocessing unless you know you won't block a thread.
@@

### Pitfalls To Look For

Profile tasks and adjust the major configuration options first.

Otherwise look at task granularity.

Don't Use Pickle

Start Small
@@

#Thank You

github: calebsmith

gitlab: csmith

twitter: @calebsmithnc
