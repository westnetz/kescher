Quickstart
==========

This chapter covers the steps needed in order to set up *kescher* to start accounting.

Initialization
--------------

It is useful to have a directory dedicated to kescher. Documents, bank statements, etc. 
can and should be stored here.

.. note::

	It is not recommended to import documents from outside the kescher directory,
	as this is can cause problems when using exports.

Create the kescher working directory 

.. code:: zsh

	$ mkdir accounting_2020
	$ cd accounting_2020

Next, you initialize the kescher in this directory. This will create the database *kescher.db*
and a log file *kescher.log* here. 

Account Creation
----------------

The easiest way to set up your chart of accounts is by creating a yaml file with the following
structure

.. code:: yaml

	Customers:
	  - "1000"
	  - "1001"
	  - "1002"
	VAT:
	  - VAT_in
	  - VAT_out
	Expenses:
  	  - Internet
	  - Power
  	  - Rent
	  - Phone
	  - Aquisition:
    	    - Hardware
	    - Materials
	Revenue:
	  - Internet_Connections

This will create four base accounts (Customers, VAT, Expenses, Revenue) with child accounts.
The base accounts are not meant to be used to directly assign bookings to, but rather to 
allow for easier balance aggregation.

Invoice Import
--------------

Invoices can be imported directly from a `rechnung <https://github.com/westnetz/rechnung>`_ working
directory. Of course it is possible to import invoices from another invoicing tool, but currently
only the format *rechnung* uses is supported (yaml file for data and a pdf as the real document).

.. code:: zsh

	$ kescher import-invoices --nested ../rechnung_2020/invoices cid total\_gross date

This will import all invoices from rechnung located in the given directory. This will create
virtual bookings for each invoice. These virtual bookings are virtual as they are not the 
basis for tax calculations. Non existing customer accounts will be created (yet, not assigned
to the *Customer* parent account!). The pdf documents are imported as documents, ready to be 
assigned to entries in your journal.

If you want to import invoices from another tool, you can also convert the necessary data to 
the desired data, an store them in a directory and use the *--flat* option for the import. A 
minimal invoice to be imported into *kescher* would look like this:

.. code:: yaml

	cid: "1000"
	total_gross: 24.00
	date: "2020-02-11"

Journal Import
--------------


