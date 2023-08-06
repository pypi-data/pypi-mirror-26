pygenderbr
==========

Python library to interface with "Nomes" IBGE API. Further, the tools
can be used to query the persons names from Brazil. The IBGE API is
based on 2010 Census.

Features
--------

-  Query by name(s) gender(s) based on 2010 IBGE Census from Brazil.
   Gender return are 'F' or 'M'. Indefined gender is ''.
-  Query by name(s) ocurrence(s) by gender on Brazil or specific state
-  Query by name(s) occurrence(s) on specific gender or on all
-  Query by names ranking occurrence on Brazil (20's most)

Prerequisites
-------------

-  Python 2 or newer
-  requests
-  Pandas

Site
----

-  https://github.com/alexfurtunatoifrn/pygenderbr

Installation
------------

::

    $ pip3 install pygenderbr

Usage
-----

Class Gender
~~~~~~~~~~~~

::

    >>> from pygenderbr import Gender
    >>> gapi = Gender()
    >>> g = gapi.getgender('joao')
    >>> print(g)
    name
    JOAO    M
    Name: gender, dtype: object
    >>> g = gapi.getgender(['joao','maria'])
    >>> print(g)
    name
    JOAO     M
    MARIA    F
    Name: gender, dtype: object
