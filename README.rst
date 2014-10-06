Caktus Talks and Presentations
==============================

Caktus Consulting Group, LLC

Directory
---------

* PyCon
    * 2013
        * `Designers + Developers: Collaborating on your Python project <http://lanyrd.com/2013/pycon/scdyym/>`_
* OSCON
    * 2013
        * Designers + Developers: Collaborating on your Open Source project
* DjangoCon US
    * 2012
        * `OpenBlock: Overview and Initial Experience <http://talks.caktusgroup.com/djangocon/2012/openblock>`_
        * `Is Django for Designers? <http://lanyrd.com/2012/djangocon-us/sxbyd/>`_
    * 2014
        * `Anatomy of a Django Project <http://talks.caktusgroup.com/djangocon/2014/django-project/>`_
        * `What is the Django admin good for? <http://talks.caktusgroup.com/djangocon/2014/django-admin/>`_
* PyCarolinas
    * 2012
        * `Integrating Designers Into Your Development Cycle <http://talks.caktusgroup.com/pycarolinas/2012/integrating-designers>`_
        * `Maintaining Your Sanity While Maintaining Your Open Source App <http://talks.caktusgroup.com/pycarolinas/2012/maintaining-sanity>`_
        * `Working with Designers <http://lanyrd.com/2012/pycarolinas/syhmt/>`_
* Lightning Talks
    * 2014
        * `Deploying WordPress using best practices <http://talks.caktusgroup.com/lightning-talks/2014/wordpress-deploy>`_
        * `Data Visualization | Tracking Packages with Ona, Celery, and Leaflet <http://talks.caktusgroup.com/lightning-talks/2014/mapping-form-data>`_
    * 2013
        * `Emmet <http://talks.caktusgroup.com/lightning-talks/2013/emmet>`_
        * `Salt with a Master and Git <http://talks.caktusgroup.com/lightning-talks/2013/salt-master>`_
    * 2012
        * `Backbone <http://talks.caktusgroup.com/lightning-talks/2012/backbone>`_
        * `HTML5 Game Development <http://talks.caktusgroup.com/lightning-talks/2012/html5-game-development>`_
        * `django-template-debug <http://talks.caktusgroup.com/lightning-talks/2012/django-template-debug>`_
        * `Anora <http://talks.caktusgroup.com/lightning-talks/2012/anora>`_
        * `Selenium <http://talks.caktusgroup.com/lightning-talks/2012/selenium>`_
        * `KDE <http://talks.caktusgroup.com/lightning-talks/2012/kde>`_
        * `Encryption and Identity <http://talks.caktusgroup.com/lightning-talks/2012/encryption>`_
    * 2011
        * `LESS <http://talks.caktusgroup.com/lightning-talks/2011/less>`_
        * `FabulAWS <http://talks.caktusgroup.com/lightning-talks/2011/fabulaws>`_
        * `Service Page API <http://talks.caktusgroup.com/lightning-talks/2011/service-page-api>`_
        * `django-selectable <http://talks.caktusgroup.com/lightning-talks/2011/django-selectable>`_
        * `PLY <http://talks.caktusgroup.com/lightning-talks/2011/ply>`_
* ShipIt
    * 2013
        * `Haystack Facets <http://talks.caktusgroup.com/shipit/2013/haystack-facets>`_
        * `Trying out Django 1.6 Upgrade <http://talks.caktusgroup.com/shipit/2013/django16-upgrade-experience>`_

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

Add your slide URL to the list in this README.
