Caktus Talks and Presentations
==============================

Caktus Consulting Group, LLC

Directory
---------

* DjangoCon
    * `OpenBlock: Overview and Initial Experience <http://talks.caktusgroup.com/djangocon/2012/openblock>`_
* Lightning Talks
    * 2012
        * `Backbone <http://talks.caktusgroup.com/lightning-talks/2012/backbone>`_
        * `HTML5 Game Development <http://talks.caktusgroup.com/lightning-talks/2012/html5-game-development>`_
        * `django-template-debug <http://talks.caktusgroup.com/lightning-talks/2012/django-template-debug>`_
        * `Selenium <http://talks.caktusgroup.com/lightning-talks/2012/selenium>`_
        * `KDE <http://talks.caktusgroup.com/lightning-talks/2012/kde>`_
    * 2011
        * `LESS <http://talks.caktusgroup.com/lightning-talks/2011/less>`_
        * `FabulAWS <http://talks.caktusgroup.com/lightning-talks/2011/fabulaws>`_
        * `Service Page API <http://talks.caktusgroup.com/lightning-talks/2011/service-page-api>`_
        * `django-selectable <http://talks.caktusgroup.com/lightning-talks/2011/django-selectable>`_
        * `PLY <http://talks.caktusgroup.com/lightning-talks/2011/ply>`_
* PyCarolinas
    * 2012
        * `Integrating Designers Into Your Development Cycle <http://talks.caktusgroup.com/pycarolinas/2012/integrating_designers_into_dev_cycle>`_
        * `Maintaining Your Sanity While Maintaining Your Open Source App <http://talks.caktusgroup.com/pycarolinas/2012/maintaining-sanity>`_

Setup
-----

Create a new virtualenv and install the requirements::

    mkvirtualenv --distribute talks
    pip install -r conf/requirements.txt

Landslide
---------

Default configuration
*********************

Create a new directory for your slides. Slides should have the ``.rst``
extension.

Build your slides with::

    fab landslide:path/to/directory

Custom configuration
********************

Add a new configuration section to ``conf/slides.cfg``, like::

    [djangocon-openblock]
    source = djangocon/2012/openblock
    theme = conf/themes/new-caktus-theme

You can specify the standard landslide configuration options here.

Build your slides with::

    fab landslide:name=djangocon-openblock

RevealJS
--------

Create a new slide template with this command::

    fab revealjs:path/to/new/directory

This will create the new directories and add a fresh ``index.html`` file.

Publishing your slides
----------------------

Add your slides to git and push up to GitHub::

    git add path/to/directory
    git commit
    git push

Visit http://talks.caktusgroup.com/path/to/directory

Add your slide URL to the list in this README.
