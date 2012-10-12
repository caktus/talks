Talks and Presentations
=======================

Caktus Consulting Group, LLC

Setup
-----

    mkvirtualenv --distribute talks
    pip install -r requirements.txt
    
Landslide
---------

Default Configuration
*********************

* Create a new directory for your slides. Slides should have the ``.rst``
  extension.

* Build your slides with::

    fab landslide:path/to/directory

* Add your slides to git and push up to GitHub::

    git add path/to/directory
    git commit
    git push

* Visit http://talks.caktusgroup.com/path/to/directory
