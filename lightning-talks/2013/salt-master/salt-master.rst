Managing your computers with a Salt Master and Git
==================================================

Dan Poirier

Lightning Lunch Talk

November 22, 2013

----

What's this about?
==================

I've been moving toward using Salt to manage some of my personal systems,
and recently added a Salt Master and put my data into Git.

I'm going to share some of how I'm doing this.

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

Integrates nicely with Salt.

Presenter Notes
---------------

* Not just storing state and pillar files in git, and checking them out
  on the master
* The Master actively checks the git upstream for changes and pulls them
  before updating systems.

----

Setting up a master
===================

* A VM
* Ubuntu
* Salt

Presenter Notes
---------------

* A small VM on Digital Ocean ($5/month)
* Ubuntu 13.04 64bit
* Salt of course

----

Installing Salt Master
======================

I use the bootstrap script and specify a particular version::

    curl --insecure -L http://bootstrap.saltstack.org | sh -s -- -M -N git v0.17.1

(https://github.com/saltstack/salt-bootstrap)

Presenter Notes
---------------

* Both PyPI and their Ubuntu PPA tend to lag releases, so if you want the latest,
  this seems to be the best way to get it, straight from github.
* This particular invocation installs the master without the minion.
