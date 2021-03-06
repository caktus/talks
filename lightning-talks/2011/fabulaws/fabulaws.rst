FabulAWS
========

Tobias McNulty

August 19, 2011

----


Project Overview
-----------------------------------

**What's so fabulous about FabulAWS?**

FabulAWS lets you provision new servers from scratch, automatically,
with minimal changes to your existing fab files.

----


Break #1: Never do a live demo
------------------------------

* Kicking things off

----

Motivation
-----------------------------------

* Doing it by hand is bad
* Not thrilled with other tools
* Declarative syntax is pretty

----


How does it work?
-----------------

* Provides templates for barebones servers
* Pick a template and extend it
* Instantiate the template in your fab file

----


Break #2: A sample template
---------------------------

* The template itself
* local_settings.py
* Sysadmin user keys

----


What does it do?
----------------

* Boto for communicating with AWS
* Destroys temporary key
* Installs packages
* Creates users

----


Break #3: Fab file changes
--------------------------

* Logging
* A ``new_instance`` environment
* Do everything through ``sudo()``
* SSH Agent forwarding

----


Gotchas along the way
---------------------

* Where to install Fabric
* Detecting when the SSH connection's ready
* Fabric context
* Permissions and SSH agent forwarding
* Where to get the database and media
* Passwords for sysadmin users (or password-less sudo)

----


Other tools
-----------

* Puppet - http://www.puppetlabs.com/
* Chef - http://www.opscode.com/chef/

----


Next steps
----------------------------------

* Documentation
* More sites

----


Thanks!
-------

* Grab the code at https://github.com/caktus/fabulaws
