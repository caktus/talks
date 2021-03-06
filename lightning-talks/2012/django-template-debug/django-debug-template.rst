Django Template Debug
================================================

Caleb Smith

August 23, 2012

----


Talk Overview
------------------------------------------------

* What is django-template-debug
* Motivation?
* How does it work?

----


Project Overview
-----------------------------------------------

Django-Template-Debug is a Django app for instrospecting templates as
they render.

----


Motivation
------------------------------------------------

* Template writers largely have two questions: What are the available variables and what are their attributes?

----

Motivation
------------------------------------------------

* Template writers largely have two questions: What are the available variables and what are their attributes?
* Django debug toolbar gets us most of the way there, but doesn't offer a way to interact with the objects in the context.

----

Motivation
------------------------------------------------

* Once a view returns, there is no convienient place to add a breakpoint.

----

Motivation
------------------------------------------------

* Once a view returns, there is no convienient place to add a breakpoint.
* ...and stepping through from the end of the view is tedious.

----

Motivation
------------------------------------------------

* Once a view returns, there is no convienient place to add a breakpoint.
* ...and stepping through from the end of the view is tedious.
* Debugging usually happens in models and views, but what if you inherit a project with TONS of template logic?

----

Motivation
------------------------------------------------

* Once a view returns, there is no convienient place to add a breakpoint.
* ...and stepping through from the end of the view is tedious.
* Debugging usually happens in models and views, but what if you inherit a project with TONS of template logic?
* Django is for designers too.

----

Installation
------------------------------------------------

* pip install django-template-debug
* Add 'template-debug' to INSTALLED_APPS in your local settings.

----

Installation
------------------------------------------------

* pip install django-template-debug
* Add 'template-debug' to INSTALLED_APPS in your local settings.

----

Installation
------------------------------------------------

* pip install django-template-debug
* Add 'template-debug' to INSTALLED_APPS in your local settings.
* Add {% load debug_tags %} in your template

----

Tags
------------------------------------------------

Django-Template-Debug offers three template tags:

* set_trace
* variables
* details

----

{% set_trace %}
------------------------------------------------

* Starts a set_trace while the template is being rendered. ipdb is used if available; otherwise the tag falls back to pdb.
* The context is available inside of the set_trace as the variable 'context'.
* The user can type 'availables' to see a list of variables inside of the context.

----

{% set_trace %}
------------------------------------------------
The variables available inside of the context are available in the local scope as <variable_name> (e.g. If a variable 'items' is in the context, it is available in the set trace as the variable 'items')

----

{% variables %}
------------------------------------------------
Prints the variables available in the current context in the terminal where runserver is running

----

{% details <variable_name> %}
------------------------------------------------
* Prints a dictionary in the pattern {attribute: value} of the variable provided, for any attribute's value that can be obtained without raising an exception or making a method call.

----

Live Demos Always Fail But ....
------------------------------------------------
Maybe it won't this time?

----

Questions?
------------------------------------------------

* Code: https://github.com/calebsmith/django-template-debug
* Documentation: https://github.com/calebsmith/django-template-debug/blob/master/README.rst
