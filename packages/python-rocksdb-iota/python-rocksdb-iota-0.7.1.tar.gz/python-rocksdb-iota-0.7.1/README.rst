Note
=========
The original pyrocksdb (https://pypi.python.org/pypi/pyrocksdb/0.4) has not been updated for long time.
[twmht update pyrocksdb](https://github.com/twmht/python-rocksdb) to support the latest rocksdb.

This is a pyrocksdb for IOTA, Please open issues in github if you have any problem.

The main different is:

* Fix column family problem and test cases
* Using StringAppendOperator as column family merge operator default
* Rename package from `rocksdb` to `rocksdb_iota`

pyrocksdb
=========

Python bindings for RocksDB with IOTA modification.
See http://python-rocksdb.readthedocs.io/en/latest/ for a more comprehensive install and usage description.


Quick Install
-------------

Quick install for debian/ubuntu like linux distributions.

.. code-block:: bash

    $ apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev
    $ git clone https://github.com/facebook/rocksdb.git
    $ cd rocksdb
    $ mkdir build && cd build
    $ cmake ..
    $ make
    $ export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:`pwd`/../include
    $ export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:`pwd`
    $ export LIBRARY_PATH=${LIBRARY_PATH}:`pwd`

    $ cd ../
    $ apt-get install python-virtualenv python-dev
    $ virtualenv pyrocks_test
    $ cd pyrocks_test
    $ . bin/active
    $ pip install python-rocksdb-iota


Quick Usage Guide
-----------------

.. code-block:: pycon

    >>> import rocksdb_iota
    >>> db = rocksdb_iota.DB("test.db", rocksdb.Options(create_if_missing=True))
    >>> db.put(b'a', b'data')
    >>> print db.get(b'a')
    b'data'
