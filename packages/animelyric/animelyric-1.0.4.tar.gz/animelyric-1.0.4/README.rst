# animelyric
-------------

Description
~~~~~~~~~~~

Animelyrics is a python library for retrieving lyrics for anime songs
from animelyrics dot com.

Table of Contents
~~~~~~~~~~~~~~~~~

-  Requirements
-  Installation
-  Usage
-  Examples
-  Contact

Requirements
~~~~~~~~~~~~

-  urllib.request
-  bs4
-  requests
-  google
-  urllib.parse

Install
~~~~~~~

Using pip

::

    pip install animelyric

or clone and install: 
::

    git clone https://github.com/emily-yu/animelyrics.git
    cd animelyric
    python setup.py

Usage
~~~~~

::

    from animelyrics import AnimeLyrics
    al = AnimeLyrics('[keyword-to-search]')

+------------+------------------------------------+
| Function   | Parameter                          |
+============+====================================+
| init       | keyword-to-search                  |
+------------+------------------------------------+
| lyrics     | lang (en: English, jp: Japanese)   |
+------------+------------------------------------+
