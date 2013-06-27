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

* Monthly scans by Orvant
* Whitelist false-positives
* Respond appropriately when new issues are flagged
* Useful regression discovery

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

Client Documentation: PCI Standards
------------------------------------------------

* What: Payment Card Industry
* The PCI Standard: pcistandards.org
* Certification vs. Compliance

Presenter Notes
---------------

* What: If your site provides access to a financial transaction this is for you
* 6 core steps to assess your compliance
* processing $500k plus annually requires 3rd party annual audit ($$$$) for certification

----

Common PCI mistakes in Django apps
------------------------------------------------

* 1. storing credit card info in plain text (see tokenization)
* 2. default passwords not changed
* 3. poor code: SQL injection vulnerabilities, for instance
* 4. lack of monitoring or logging
* 5. not using SSL for payment page
* 6. logging payment information into log files
* 7. missing security patches
* SOURCE: http://www.youtube.com/watch?v=9ZIPNWqjIEI

Presenter Notes
---------------

* 1. Third party tokenization services are cheaper than an annual audit
* 6. especially when there is an error (django error emails)
* Source: Djangocon 2012, Ken Cochrane, dotCloud, "Building PCI Compliant Django Applications"

----

What this means for Caktus
------------------------------------------------

* New project with PCI requirement should be made compliant
* Inherited projects with PCI maybe request bringing site up to compliance as prerequisite

Presenter Notes
---------------

* At bare minimum, tokenization and monitoring (core part of PCI compliance should be a requirement
* hosting on AWS (PCI certified secure network)

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
