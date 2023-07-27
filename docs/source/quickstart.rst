DisTRaX's Quick Start Guide!
===================================

This guide will get you up and running with deploying and removing a storage cluster using DisTRaX. We will go over the commands that DisTRaX uses along with the configuration. We will show how to create the pool, a gateway and a filesystem clusters.

This guide will focus on deploying a ceph cluster. To see more information about ceph, please read to docs: `https://docs.ceph.com/ <https://docs.ceph.com/>`_

Commands
========

DisTRaX takes three arguments.

* -a/--action: `create` or `remove`
* -c/--config-file: Path to the config file
* -log/--log-level: `info` or `debug`

The action defines what you would like DisTRaX to do, whether to build, aka `create` or destroy, aka `remove` a storage cluster.

Config
======
DisTRaX uses a config file to hold all the options of the cluster. The file consists of two main parts SETUP, RAM:


Setup
------

The Setup section has four required inputs and is used to configure the storage cluster:

* backend: The storage system being used.
* folder: The folder to store system details (must exist on all hosts)
* Interface: This is the network interface the cluster will communicate over (must exist on all hosts)
* number_of_hosts: The number of nodes used to form the cluster.
* service: This can either be pool, gateway or filesystem

.. code-block::
   :caption: Setup section config example with pool service: distrax.cfg

    [setup]
    backend = ceph
    folder = my_ceph
    interface = lo
    number_of_hosts = 1
    service = pool

Service
-------

This system supports three services, `Pool`, `Gateway` or `Filesystem`.

Pool
~~~~
A pool is the simplest way to store objects and has the least overhead of all the services as it talks directly to the object storage device.
To read more, see the ceph docs `https://docs.ceph.com/en/latest/rados/operations/pools/ <https://docs.ceph.com/en/latest/rados/operations/pools/>`_


.. code-block::
   :caption: Pool section config example: distrax.cfg

    service=pool

This will create a cluster with pool name of distrax.

Gateway
~~~~~~~

The gateway creates a Restful S3 API-accessible object-store. To read more about S3 see `https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_


.. code-block::
   :caption: Gateway section config example: distrax.cfg

    service = gateway

The gateway will create a user named distrax along with a credentials file inside the specified folder which will contain, the username, access_key, secret_key and endpoint information

.. code-block::
   :caption: credentials file example

    [default]
    user = distrax
    access_key = 8TSNGCP3P1376H2USM12
    secret_key = YvNtEBAhiOB4AfczjXHZKPvPHCXECckMRE32rDBy
    endpoint = http://127.0.0.1:7480/

Filesystem
~~~~~~~~~~

This creates and mounts a filesystem at a /mnt/distrax.

.. code-block::
   :caption: Filesystem section config example: distrax.cfg

    service = filesystem

Ram
---
The Ram section has three required inputs used as OSD for the storage cluster.

* Type: The Ram kernel module to use
* size_in_gb: The size of the Ram Block in GB.
* Number: The number of Ram Blocks

Please note that if you have the following setup, it will create 10 OSDs, each one 1GB in size.

.. code-block::
   :caption: Ram section config example: distrax.cfg

    [ram]
    type = brd
    size_in_gb = 1
    number = 10

Whereas this creates 1 OSD with a size of 10GB

.. code-block::
   :caption: Ram section config example: distrax.cfg

    [ram]
    type = brd
    size_in_gb = 10
    number = 1


Device
------

This outlines which Block devices to use.

.. note::

   This is currently being developed.


Examples
========

We would use the following configuration file to create a ceph cluster on our local system using 1GB of RAM with 1 OSD and a pool.

.. code-block::
   :caption: Config example: distrax.cfg

    [setup]
    backend = ceph
    folder = my_ceph
    interface = lo
    number_of_hosts = 1
    service = pool

    [ram]
    type = brd
    number = 1
    size_in_gb = 1


To build the cluster, we would use

.. code-block::
   :caption: Config example: distrax.cfg

    distrax -c distrax.cfg -a create

To remove the cluster, we would use

.. code-block::
   :caption: Config example: distrax.cfg

    distrax -c distrax.cfg -a remove

.. toctree::
   :hidden:
