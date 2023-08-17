
``distrax.mons`` module
========================

.. currentmodule:: distrax.mons

A MON is the cluster monitor daemon, this is often used to maintain cluster health, and make sure that all the parts of the cluster can communicate to one another.

Methods
-------

.. automodule:: distrax.mons

.. autosummary::
  :toctree: _autosummary

    AVAILABLE
    set_mon
    get_mon

Classes
-------

.. toctree::
    :maxdepth: 1

    distrax.mons.abstract_mon
    distrax.mons.ceph_mon
