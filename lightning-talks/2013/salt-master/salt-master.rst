Managing your computers with a Salt Master and Git
==================================================

Dan Poirier

Lightning Lunch Talk

November 22, 2013

Presenter Notes
---------------

* I've been moving toward using Salt to manage some of my personal systems,
  and recently added a Salt Master and put my data into Git.

* I'm going to share some of how I'm doing this and how it's working.

* Consider this talk anecdotal, not authoritative.

----

Salt Master
===========

Why?  A master serves two roles:

* Server
* Controller

Presenter Notes
---------------

* Server for states and pillar data, so you don't have to sync your
  state and pillar files to all your minions some other way
* One place where you can kick off updates to many systems at once
  (if you want)

Even with a master, you can still kick off updates on each minion anytime
you want.

----

Git
===

Recent versions of Salt have added Git integration.

Presenter Notes
---------------

* Not just storing state and pillar files in git, and checking them out
  on the master
* The Master actively checks the git upstream for changes and pulls them
  before updating systems.
* The minion does not have that ability, so we need a master to take advantage
* **Note** though that the git support still seems a bit buggy, not quite
  production-ready in 0.17.1

----

Setting up a master
===================

* A VM
* Ubuntu

Presenter Notes
---------------

* A small VM on Digital Ocean ($5/month)
* Ubuntu 13.04 64bit

----

Installing Salt Master
======================

I use the bootstrap script and specify a particular version::

    curl --insecure -L http://bootstrap.saltstack.org \
    | sh -s -- -M -N git v0.17.1

(https://github.com/saltstack/salt-bootstrap)

* The default is to just install the minion.
* ``-M`` adds the master
* ``-N`` skips the minion.
* ``git`` get the code from github
* ``v0.17.1.`` look for a tag or branch v0.17.1

Presenter Notes
---------------

* Both PyPI and their Ubuntu PPA tend to lag releases, so if you want the latest,
  this seems to be the best way to get it, straight from github.
* This particular invocation installs the master without the minion.

----

State files from git
====================

In ``/etc/salt/master``, comment out the config related to getting
the state files from the local file system::

    # fileserver_backend:
    #  - roots
    # file_roots:
    #  base:
    #    - /srv/salt

Enable the ``git`` fileserver backend::

    fileserver_backend:
      - git

And give it one or more git repos to look at::

    gitfs_remotes:
      - git://github.com/saltstack/salt-states.git


----

Private git repos
=================

If the repo is private, you need to access it using ssh::

    gitfs_remotes:
      - git+ssh://git@prius.poirier.us/salt-states.git

And put a passwordless private ssh key in ~/.ssh/id_rsa under the
user that salt master is running as

Presenter Notes
---------------

* (You can probably arrange for
  ssh connectivity any way ssh supports, but that's what the Salt docs
  say.)

----

Pillar from git
===============

For no apparent reason, configuring git as a source of pillar files
is rather different from how to configure git as a source of
state files::

    ext_pillar:
       - git: master git+ssh://git@prius.poirier.us/salt-pillar.git


Presenter Notes
---------------

* Don't comment out the default pillar_roots, just don't put any files there, or
  set base to an empty dictionary -
* There's a bug in 0.17.1 that breaks Salt if the default pillar config is removed.

----

Misc. other master settings
===========================

More compact output::

    state_output: mixed

Run as non-root::

    user: salt-master

Presenter Notes
---------------

* state_output: mixed gives one-line output for successful states, more verbose for ones that fail
* You can run salt-master pretty easily as non-root because it just talks to minions and git over
  the network, it doesn't apply changes to machines.

----


Installing Salt Minion
======================

Bootstrap script again, don't need any extra options this time though, just
``git`` to get salt from github, and the version::

    curl --insecure -L http://bootstrap.saltstack.org \
    | sh -s -- git v0.17.1

----

Configuring Salt Minion
=======================

Not much needed. In ``/etc/salt/minion``::

    master: <full hostname of master>
    id: <shorthostname of minion>
    state_output: mixed

Presenter Notes
---------------

All the minion needs is a name and how to find the master, and you
can skip the name if you're happy with just using the hostname.

----

Start the minion
================

Might need to start the minion::

    sudo service salt-minion start

----

Accept the minion's key on the master
=====================================

The master won't talk to any minion unless you say it's okay::

    # salt-key -a <minion ID>

Presenter Notes
---------------

* When the minion starts, it'll connect to the master and offer its key (randomly generated
  the first time it starts)
* The master will refuse to talk to it, though, until you tell the master to accept that key.

----

What am I doing with Salt?
==========================

* Personal preferences - user account, Emacs, .bashrc
* Personal services - dropbox
* Connectivity - ssh keys, email aliases
* Development - useful packages
* System config - obscure things I always forget to do and then have to look up

----

Useful packages
===============

Install packages I want everywhere::

    packages:
      pkg.latest:
        - name: screen
        - name: sqlite3

or just Ubuntu::

    {% if grains['os'] == 'Ubuntu' %}
    {% for pkg in 'tasksel', 'python-software-properties' %}
    {{ pkg }}:
      pkg.latest
    {% endfor %}
    {% endif %}

----

Emacs
=====

PPA for latest version::

    {% if grains['os'] == 'Ubuntu' %}
    ppa-emacs:
      pkgrepo.managed:
        # Emacs
        - ppa: cassou/emacs
        - require_in:
          - pkg: emacs24
    {% endif %}

Install packages with latest version::

    {% for name in ['emacs24', 'emacs24-el'] %}
    {{ name }}:
      pkg.latest:
      {% if grains['os'] == 'Ubuntu' %}
        - require:
          - pkgrepo: ppa-emacs
      {% endif %}
    {% endfor %}

----

Pillar data
===========

A sample of what I have in pillar::

    {% if 'caktus' in grains['domain'] %}
    myusername: dpoirier
    mygroupname: dpoirier
    myemail: dpoirier@caktusgroup.com
    myhomedir: /home/dpoirier
    {% else %}
    myusername: poirier
    myemail: dan@poirier.us
    ...
    {% endif %}

You get the idea.

Presenter Notes
---------------

* I could use a different username on every system if I want, and wouldn't have
  to change a single state file.

----

Access to Git repos using a deploy key
======================================

bitbucket.sls::

    bitbucket_deploy_key:
      file.managed:
        - name: {{ pillar['myhomedir'] }}/.ssh/id_bitbucket
        - contents_pillar: bitbucket:deploy_key
        - user: {{ pillar['myuid'] }}
        - group: {{ pillar['mygid'] }}
        - mode: 400

In pillar::

    bitbucket:
      deploy_key: |
        -----BEGIN RSA PRIVATE KEY-----
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ....

----

Emacs config files from Git
===========================

I keep my ~/.emacs.d directory in git, and this state keeps it up to date on all my systems::

    git@bitbucket.org:poirier/emacs.d.git:
      git.latest:
        - rev: master
        - target: {{ pillar['myhomedir'] }}/.emacs.d
        - user: {{ pillar['myusername'] }}
        - group: {{ pillar['mygid'] }}
        - identity: {{ pillar['myhomedir'] }}/.ssh/id_bitbucket
        - require:
            - user: {{ pillar['myusername'] }}
            - file: bitbucket_deploy_key

----

Tell Debian I want to use Emacs as my default editor
====================================================

alternatives.sls::

    editor:
      alternatives.install:
        - name: editor
        - link: /usr/bin/editor
        - path: /usr/bin/emacs
        - priority: 100

----

Cron job to update nightly
==========================

Use salt to set up the cron job to run salt between 2 and 2:59 am each day::

    /usr/bin/salt-call -l quiet state.highstate:
      cron.present:
        - user: root
        - minute: random
        - hour: 2

----

Sysctl Settings
===============

PyCharm and Crashplan both want you to increase the kernel setting for how many files
they can monitor for changes. This is the kind of thing I always used to forget to
do when I set up a new machine, but not anymore::

    fs.inotify.max_user_watches:
      sysctl.present:
        - value: 1048576

----

Dropbox
=======

Getting dropbox installed and connected under my account isn't fully automated yet,
but once that's done, I use Salt to reliably have Supervisor keep dropbox running::

    # dropbox.sls
    dropbox:
      supervisord.running:
        - restart: True
        - watch:
          - file: /etc/supervisor/conf.d/dropbox.conf
        - require:
          - pkg: supervisor
          - file: /etc/supervisor/conf.d/dropbox.conf

    /etc/supervisor/conf.d/dropbox.conf:
        file.managed:
          - source: salt://dropbox/dropbox_supervisor.conf
          - user: root
          - group: root
          - template: jinja

    extend:
      supervisor:
        service:
          - watch:
              - file: /etc/supervisor/conf.d/dropbox.conf

----

Dropbox (cont)
==============

Here's the template for the supervisor config file for dropbox::

    # dropbox_supervisor.conf
    [program:dropbox]
    command=/home/{{ pillar['myusername'] }}/.dropbox-dist/dropboxd
    numprocs=1
    directory=/home/{{ pillar['myusername'] }}
    user={{ pillar['myusername'] }}
    redirect_stderr=true

----

Java
====

Installing Java on Ubuntu is a pain, but Salt can handle it::

    accept-java-license:
      debconf.set:
        - name: oracle-java8-installer
        - data:
            shared/accepted-oracle-license-v1-1: {'type': boolean, 'value': true}
        - require:
            - pkg: debconf-utils

    ppa-java:
      pkgrepo.managed:
        # Java
        - ppa: webupd8team/java
        - require_in:
          - pkg: java

    java:
      pkg.latest:
        - name: oracle-java8-installer
        - require:
          - debconf: accept-java-license

----

TODO list
=========

Some things I'd still like to do:

* Set up automatic backups
* Configure postfix for email
* Make my states public (once I'm sure there's no personal data in there)

----

More information
================

* Salt bootstrap `<https://salt.readthedocs.org/en/latest/topics/tutorials/salt_bootstrap.html>`
* Salt master config `<https://salt.readthedocs.org/en/latest/ref/configuration/master.html>`
* Keeping stuff in git `<https://salt.readthedocs.org/en/latest/topics/tutorials/gitfs.html>`
* List of salt states `<https://salt.readthedocs.org/en/latest/ref/states/all/>`
