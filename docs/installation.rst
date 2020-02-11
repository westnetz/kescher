Installation
============

Currently this package is not available on the PythonPackageIndex (PyPI). 

.. note::

   *kescher* is still under heavy development. Even the stable versions are not fit for
   production use yet!

*kescher* is developed with and for Python3.8. It might work in older versions. Incompatibility
with Python versions <3.8 will not be fixed and not considered bugs!

Prerequisites
-------------

Install Python3.8 with your favourite package manager. It is recommended to use a virtual 
environment helper such as virtualenv.

.. code:: zsh

   $ mkvirtualenv kescher

Installation with *poetry* is desired. Therefore you have to install it via pip.

.. code:: zsh

   $ pip install poetry


Stable Version
--------------

The latest stable version can be optained by using the *releases* tab on github. Fetch the latest
zip file and extract it. 


Latest Version
--------------

Obtain the latest version from github, by cloning the repository:

.. code:: zsh

   $ git clone https://github.com/westnetz/kescher


Installation
------------

After cloning the repository change your directory to it and install *kescher*:

.. code:: zsh

   $ poetry install
