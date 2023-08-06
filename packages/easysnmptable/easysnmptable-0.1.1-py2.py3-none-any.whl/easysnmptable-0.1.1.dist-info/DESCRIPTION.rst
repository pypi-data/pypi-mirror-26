|PyPI| |Build Status| |codecov| |Code Health| |Requirements Status|

easysnmptable
=============

An extension to
`easysnmp <https://github.com/kamakazikamikaze/easysnmp>`__ providing: -
SNMP Table handling - Context manager support

Installation
------------

.. code:: bash

    $ pip install easysnmptable

Usage
-----

.. code:: python

    from easysnmptable import Session

    with Session(hostname='localhost', community='public', version=2) as session:
      iftable = session.gettable('ifTable')

    for index, row in table.rows.items():
      print("index: {}".format(index))
      for key, value in row.items():
        print("{}: {}".format(key, value))

.. |PyPI| image:: https://img.shields.io/pypi/v/easysnmptable.svg
   :target: https://pypi.python.org/pypi/easysnmptable
.. |Build Status| image:: https://travis-ci.org/wolcomm/easysnmptable.svg?branch=master
   :target: https://travis-ci.org/wolcomm/easysnmptable
.. |codecov| image:: https://codecov.io/gh/wolcomm/easysnmptable/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/wolcomm/easysnmptable
.. |Code Health| image:: https://landscape.io/github/wolcomm/easysnmptable/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wolcomm/easysnmptable/master
.. |Requirements Status| image:: https://requires.io/github/wolcomm/easysnmptable/requirements.svg?branch=master
   :target: https://requires.io/github/wolcomm/easysnmptable/requirements/?branch=master


