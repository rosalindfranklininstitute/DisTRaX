
``distrax.mdss`` module
=======================

.. currentmodule:: distrax.mdss

An MDS is the cluster filesystem daemon, this is required for a filesystem to be created. It is used to manage the file system namespace and coordinating access to the storage for read and write.

Methods
-------

.. automodule:: distrax.mdss

.. autosummary::
  :toctree: _autosummary

    AVAILABLE
    set_mds
    get_mds

Classes
-------

.. toctree::
    :maxdepth: 1

    distrax.mdss.abstract_mds
    distrax.mdss.ceph_mds
