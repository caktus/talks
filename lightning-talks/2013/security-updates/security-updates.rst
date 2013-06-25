Caktus Security Updates
================================================

Ben Riseling, Calvin Spealman, Mark Lavin and Scott Morningstar

Caktus Consulting Group

June 28, 2013

----

Overview
------------------------------------------------

* Motivation
* Project Goals
* Results
* Future Updates

Presenter Notes
---------------

* Nothing here. This is just for an example

----

Motivation
------------------------------------------------

* Wanted clear policies in place security best practices
* Wanted checklists to follow in the case of security breaches

----

Project Goals
------------------------------------------------

* Create documentation for developers on security best practices
* Create documentation for addressing security holes or breaches
* Create documentation for advising clients on security issues
* Ensure our standard project setup is as secure as possible
* Put tools in place to routinely check for issues

----

Results
------------------------------------------------

* Security Scans
* Developer Documentation
* Client Documentation
* Project Template Updates

----

Security Scans
------------------------------------------------

# TODO

----

Developer Documentation
------------------------------------------------

Security Conscious Tips
^^^^^^^^^^^^^^^^^^^^^^^

Keeping the "gotchas" we find from being forgotten

Incident Response Guidelines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Something bad happened! What do we do?

The Security Policy Update Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contribute and Keep Up-to-date

----

Client Documentation
------------------------------------------------

# TODO

----

Project Template Updates
------------------------------------------------

* Salt Provisioning
* Better Defaults
* Documentation

----

Salt Provisioning
------------------------------------------------

* Started on ShipIt Day
* Previously using a collection of Fabric scripts
* Better separation of deployment from provisioning
* Easy and repeatable

Presenter Notes
---------------

* Entire state is sync'd to re-provision (fast enough)
* No more random upload_*_conf commands
* Still using Fabric for the deployment

----

Better Defaults
------------------------------------------------

* No connection as project user
* Tighter file permissions
* Firewall and Fail2Ban by default
* SSL everywhere
* Easy to add basic auth to staging
* Common way to manage secrets

Presenter Notes
---------------

* Unique user connection is a PCI and HIPAA requirement
* Secrets added to OS-environment

----

Documentation
------------------------------------------------

* Overview documentation
* Provisioning detailed
* Adding optional features (Celery)
* Configuration updates
* Testing with vagrant

----

Future Updates
------------------------------------------------

* We are ever vigilant
* We want feedback

Presenter Notes
---------------

* As new issues are brought to light our policies will be updated
