===========
File Deuper
===========
Copyright (c) 2014, Christopher Speck 

This application is subject to the revised 3-clause BSD license, as set out in
the LICENSE  file found in the top-level directory of this distribution. USE AT
YOUR OWN RISK AND ONLY AFTER TAKING A BACKUP. RUNNING IN DEDUPE MODE MAY ERASE
NON-SELECTED FILES.

This was built in Arch on Python 3.4, but should work in any version from 3.2
upwards. Runtime requirements are listed in setup.py and dev/test requirements
are in requirement-dev.txt

A much more primative version of this was originally used to deduplicate a
large photo collection, but it could be used for any similar mass of files
(e.g. music collection from different sources etc, if the files are identical).

Installing & Running
--------------------

I suggest using a virtual environment so that you do not have to install this
using sudo and so it and its requirements do not conflict with any system
packages. See `Virtual Environments
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ for details.

Setup::

 mkvirtualenv deduper
 pip install -e .

It needs to scan files and will store the information in a database (by
default, an sqlite database in pwd called 'files.db'). To scan::

 deduper -s

To remove files::

 deduper -d graphical (will display images)
 deduper -d cli (will give you a cursors dialog)
 deduper -d auto (will choose for you)

This will by default hardlink duplicates to the selected keeper file.

Run without arguements to see all options (including specifying delete mode
and changing the working database).

Running the tests
-----------------

Check out the repo then::

 pip install -r requirements-dev.txt
 py.test
