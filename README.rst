Talks and Presentations
=======================

Caktus Consulting Group, LLC

Setup
-----

Create a new virtualenv and install the requirements::

    mkvirtualenv --distribute talks
    pip install -r requirements.txt
    
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

Publishing your slides
----------------------

Add your slides to git and push up to GitHub::

    git add path/to/directory
    git commit
    git push

Visit http://talks.caktusgroup.com/path/to/directory
