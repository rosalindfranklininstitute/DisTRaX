Quick Start Guide for MPI!
==========================

This guide expects you to have read the  :doc:`/user/tutorials/quickstart`.

This guide goes through how to use DisTRaX to create a multinode storage cluster using the MPI version.

This tutorial uses OpenMPI and a slurm cluster.

Example Config
--------------

We will use the following configuration file to create a two node ceph cluster using the *eth0* interface, 1GB of RAM with 1 OSD and a pool.

.. code-block::
   :caption: Config example: distrax.cfg

    [setup]
    backend = ceph
    folder = my_ceph
    interface = eth0
    number_of_hosts = 2
    service = pool

    [ram]
    type = brd
    number = 1
    size_in_gb = 1


Slurm Setup Walk Through
------------------------


Slurm Setup
~~~~~~~~~~~

To build the cluster, we would use

.. code-block::
   :caption: Slurm Setup example

    #! /bin/bash
    #SBATCH --job-name=test
    #SBATCH --nodes=2
    #SBATCH --ntasks-per-node=2
    #SBATCH --cpus-per-task=1
    #SBATCH --time=10:00

    hostnames=`scontrol show hostnames| sed -n -e 'H;${x;s/\n/,/g;s/^,//;p;}'` # Get hostnames
    number_of_hosts=`scontrol show hostnames | wc -l` # Get number of hosts


Running distrax_mpi
~~~~~~~~~~~~~~~~~~~

To create the storage cluster we then would have the following:

.. code-block::
   :caption: Slurm Setup example

    mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a create

Removing distrax_mpi
~~~~~~~~~~~~~~~~~~~~

To remove the cluster, we would use

.. code-block::
   :caption: Config example: distrax.cfg

    mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a remove

.. toctree::
   :hidden:


TL;DR
-----

Slurm
~~~~~

The following is the way to run DisTRaX in a slurm cluster. Preferably the use of DisTRaX will be placed in the Prologue and Epilog for job submission using DisTRaX as this will ensure that the user doesn't forget to place the remove command at the end of the application.

.. code-block::
   :caption: Slurm Setup example

    #! /bin/bash
    #SBATCH --job-name=test
    #SBATCH --nodes=2
    #SBATCH --ntasks-per-node=2
    #SBATCH --cpus-per-task=1
    #SBATCH --time=10:00

    # Get hostnames
    hostnames=`scontrol show hostnames| sed -n -e 'H;${x;s/\n/,/g;s/^,//;p;}'`

    # Get number of hosts
    number_of_hosts=`scontrol show hostnames | wc -l`

    # Create Storage System
    mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a create

    # Run Application

    # Remove Storage System
    mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a remove
