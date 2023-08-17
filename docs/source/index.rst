Welcome to DisTRaX's documentation!
===================================

**DisTRaX** is a Python library to deploy temporary storage mechanisms onto HPC infrastructure in a fast and scalable fashion.

.. note::

   This project is under active development.


.. grid:: 2

    .. grid-item-card:: :material-regular:`library_books;2em` User Guides
      :columns: 12 6 6 4
      :link: user/index
      :link-type: doc
      :class-card: user-docs

    .. grid-item-card:: :material-regular:`laptop_chromebook;2em` Developer Docs
      :columns: 12 6 6 4
      :link: developer/index
      :link-type: doc
      :class-card: developer-docs



Installation
------------

.. tab-set::

    .. tab-item:: Single Host

       .. code-block:: bash

           pip install -e git+https://github.com/rosalindfranklininstitute/DisTRaX.git#egg=distrax

    .. tab-item:: Multi Host

       .. code-block:: bash

           pip install -e git+https://github.com/rosalindfranklininstitute/DisTRaX.git#egg=distrax[mpi]

After pip installing there are a few additional steps that are required to finish the installation process, please see :doc:`/user/tutorials/install`.

.. toctree::
   :hidden:

   Home Page <self>

.. toctree::
   :hidden:
   :maxdepth: 1

   user/index


.. toctree::
   :hidden:
   :maxdepth: 1

   developer/index
