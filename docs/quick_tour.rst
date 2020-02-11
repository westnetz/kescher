Quick Tour
==========

Let's take the quick tour. We will use the samples and fixtures from 
the automated software tests to play around a bit with the tool.

The test data is not shipped with the program, therefore you have to
get it from the repository on github. Navigate to *kescher/tests/fixtures*
and download:

- accounts.yaml
- journal.csv

Create a new directory, and put the files there

.. code:: bash

        $ mkdir kescher_quick_tour
        $ cd kescher_quick_tour
        $ cp ~/Downloads/accounts.yaml .
        $ cp ~/Downloads/journal.csv

Now it's time to initialize the *kescher*:

.. code:: zsh

        $ kescher init

If that fails: Check if you have installed the tool. Have a look at the *Installation* section to find out how to do that. 

If everything worked, your directory should look like this now:

.. code:: zsh

        $ ls -w 0
        accounts.yaml
        journal.csv
        kescher.db
        kescher.log

Have a look at the default accounts chart in the *accounts.yaml* file to see how we will structure our accounts. After you did that, it's time to import it into the *kescher*.

.. code:: zsh

        $ kescher import-accounts accounts.yaml

Also import the journal. In the real world, this is your bank statement.

.. code:: zsh

        $ kescher import-journal journal.csv
