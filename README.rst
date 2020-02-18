kescher
========

.. image:: https://circleci.com/gh/westnetz/kescher.svg?style=svg
    :target: https://circleci.com/gh/westnetz/kescher
    :alt: CircleCI Status
.. image:: https://readthedocs.org/projects/kescher/badge/?version=latest
    :target: https://kescher.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://codecov.io/gh/westnetz/kescher/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/westnetz/kescher
    :alt: Coverage

**kescher** is a simple accounting tool. 

You can load in your bank statement, connect each booking
to a virtual account, load in invoices and attach documents
to each booking.

It is currently und heavy development and not recommended for
production use.

**kescher** is not a double accounting tool. If you need that,
have a look at (h)ledger or gnucash.

.. image:: assets/kescher_promo.png

Installation
------------

Clone this repository to your machine:

.. code:: zsh

        $ git clone https://github.com/westnetz/kescher


Install poetry

.. code:: zsh
        
        $ pip install poetry

Install **kescher**

.. code:: zsh
        
        $ poetry install

Development
-----------

Run the tests

.. code:: zsh
        
        $ make test 

Copyright
---------

* Florian Rämisch, 2019

License
-------

GNU General Public License v3
