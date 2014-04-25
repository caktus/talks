
Using Docker
=========

Scott Morningstar

Caktus Consulting Group

April 25, 2014

.. image:: ./images/SuperFamous1.jpg
    :align: center
    :height: 300px

`Photo Credit <http://www.flickr.com/photos/superfamous/9027758425/sizes/o/>`_.


Presenter Notes
---------------

- Notes for the intro

----


What is Docker
-----------------------------

* Docker is an open-source project to easily create lightweight, portable, self-sufficient containers from any application. 

Presenter Notes
---------------

- The same container that a developer builds and tests on a laptop can run at scale, in production, on VMs, bare metal, OpenStack clusters, public clouds and more

----

What is Docker Really
---------------------

- Docker is Git for your whole application 

-----



Why Docker
-------------------------------

* Content agnostic
* Hardware agnostic
* Content isolation and interaction
* Automation
* Highly efficient
* Separation of duties

 More Information `Here <http://www.slideshare.net/dotCloud/why-docker>`_.

Presenter Notes
---------------

* Runs Anywhere
* On Anything
* Each part runs in it's own container
* Automation is baked in and easy
* No Hypervisor overhead, Very little IO over head
* The pieces are reusable 

----




Requirements
------------------------------------------------

* Linux with a modern kernel (At least 3.8)
* aufs (optional but recommended) 

Installation instructions `Here <http://docs.docker.io/introduction/get-docker/>`_. 

Presenter Notes
----------------

-  advanced multi layered unification filesystem 

----

Docker Terminology
------------------------------------------------

* Image = Read only snapshot
* Container = Instantiation of an image
* Registry = Storage for repository (Think Pypi)
* Repository = Shareable collection of tagged images that together create the file systems for containers

Presenter Notes
---------------

- Docker uses words different words for the same thing.

----

Basic Commands
------------------------------------------------

.. code-block:: bash

  docker pull <repository> (Pull and image from a registry / repository)
  
  docker images (list local images)
  
  docker ps (list running containers)
  
  docker run -i -t <image> <command> (-i Keep stdin open even if not attached -t Allocate a pseudo-tty )

----

An example
--------------

.. code-block:: bash

  docker pull ubuntu:latest
  
  docker run -i -t ubuntu bash


Presenter Notes
---------------

- Pull a image from a repository and run it

----

Docker Files
--------------

.. code-block:: bash

    # DOCKER-VERISON 0.8.1

    from ubuntu:12.04
    run apt-get update
    run apt-get -y install wget nginx-light
    
    run echo 'daemon off;' >> /etc/nginx/nginx.conf
    
    run cd /tmp && wget http://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone5.tar.gz -O - | tar xzvf -
    run cp -R /tmp/kibana-3.0.0milestone5/* /usr/share/nginx/www
    
    expose 80
    
    cmd /usr/sbin/nginx
    
Presenter Notes
---------------

- Docker files describe commands to run on container instantiation
- This one pulls in Ubuntu 12.04, installs nginx and kibana
- but not elastic search

------

Build and run
--------------------

.. code-block:: bash

  docker build --rm -t caktus/kibana .
  docker run -d  -p 8080:80 caktus/kibana:latest
  docker ps
  
Presenter Notes
---------------

- Kibana running on port 8080
- but no elastic search 

------

Add ElasticSearch
------------------
- Now we need to run another process
- Oh No

Presenter Notes
---------------
- Docker only runs one process in a container
- Docker feels strongly about this
- Other processes we might want in a container sshd, rsyslog

------

Supervisor would be good for this
--------------------

-----

New Dockerfile
--------------

.. code-block:: bash

    # DOCKER-VERISON 0.8.1
    
    from ubuntu:12.04
    
    
    run apt-get update
    run apt-get -y install wget nginx-light openssh-server supervisor
    
    run echo 'daemon off;' >> /etc/nginx/nginx.conf
    
    RUN mkdir -p /var/run/sshd
    RUN mkdir -p /var/log/supervisor
    
    ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
    
    run cd /tmp && wget http://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone5.tar.gz -O - | tar xzvf -
    run cp -R /tmp/kibana-3.0.0milestone5/* /usr/share/nginx/www
    
    expose 80 22
    
    CMD ["/usr/bin/supervisord"]

- docker run -t -i   -p 8080:80 -p 2222:22 caktus/kibana2:latest

Presenter Notes
---------------

- We also add sshd and now we start supervisor

-----

Now for Elastic Search
---------

.. code-block:: bash

    # DOCKER-VERISON 0.8.1
    from ubuntu:12.04
    from dockerfile/java
    
    run apt-get update
    run apt-get -y install wget nginx-light openssh-server supervisor
    
    run echo 'daemon off;' >> /etc/nginx/nginx.conf
    
    RUN mkdir -p /var/run/sshd
    RUN mkdir -p /var/log/supervisor
    
    ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
    
    run cd /tmp && wget http://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone5.tar.gz -O - | tar xzvf -
    run cp -R /tmp/kibana-3.0.0milestone5/* /usr/share/nginx/www
    # Install ElasticSearch.
    RUN wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.tar.gz
    RUN tar xzf elasticsearch-1.1.1.tar.gz
    RUN mv elasticsearch-1.1.1 /opt/elasticsearch
    RUN rm elasticsearch-1.1.1.tar.gz
     
    # Expose ports.
    #   - 9200: HTTP
    #   - 9300: transport
    EXPOSE 9200
    EXPOSE 9300
    EXPOSE 80
    EXPOSE 22
    CMD ["/usr/bin/supervisord"]

Presenter Notes
---------------

- docker run -t -i   -p 8080:80 -p 2222:22 -p 9200:9200 -p 9300:9300 caktus/kibana2:latest

------

Thanks
--------------

-------


Resources
-------------------------------------------------

- Docker: http://docker.io
- Docker on OSX: http://docs.docker.io/installation/mac/
- Docker on Windows: http://docs.docker.io/installation/windows/
- My list of Docker links: https://pinboard.in/search/u:Spigot?query=docker

----

Info
-------------------------------------------------

Slides

- HTML: http://talks.caktusgroup.com/lightning-talks/2014/docker
- Source: https://github.com/caktus/talks

