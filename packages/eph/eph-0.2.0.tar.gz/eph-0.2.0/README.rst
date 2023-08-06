.. image:: https://travis-ci.org/bluephlavio/eph.svg?branch=master
   :target: https://travis-ci.org/bluephlavio/eph

.. image:: https://coveralls.io/repos/github/bluephlavio/eph/badge.svg?branch=master
   :target: https://coveralls.io/github/bluephlavio/eph?branch=master

Readme
======

The ``eph`` package provides some useful functions, classes and tools
to`retrieve`, `parse` and `manipulate` ephemerides.

Basic Usage
-----------

.. code-block:: python

    import eph

    req = eph.JplReq() # create the request
    req.read('.ephrc', 'jplparams') # read parameters from 'jplparams' section in '.ephrc' file
    req.set({
        'COMMAND': 'earth',
        'START_TIME': '2007-11-17',
        'STOP_TIME': '2017-4-22'
        }) # set parameters from dictionary
    res = req.query() # perform the request obtaining a response from Jpl Horizons service
    ephemeris = res.parse() # extract and parse the ephemeris contained in the http response

    print(ephemeris) # print data

or, the one-liner

.. code-block:: python

    import eph

    print(eph.JplReq().read('.ephrc', 'jplparams').set({'COMMAND': '399', 'START_TIME': '2007-11-17', 'STOP_TIME': '2017-04-22'}).query().parse())


The content of :file:`.ephrc` can be something like this
(see ftp://ssd.jpl_process.nasa.gov/pub/ssd/horizons_batch_example.long for a complete description of JPL parameters)

.. code-block:: ini

    [jplparams]
    CENTER='@0'
    OBJ_DATA=NO
    MAKE_EPHEM=YES
    TABLE_TYPE=VECTORS
    VEC_TABLE=1
    REFERENCE_PLANE=ECLIPTIC
    REF_SYSTEM=J2000
    OUT_UNITS=AU-D
    CSV_FORMAT=YES
    VEC_LABEL=NO
    STEP_SIZE=1d


Command line tool
-----------------

``eph`` package also provides a command line tool to retrive ephemerides from services like JPL Horizons.
To use it, open the terminal and type

.. code-block:: bash

    $ eph 2007-11-17 2017-4-22 venus

and you get ephemeris table of Venus starting from 2007-11-17 to 2017-4-22. You can also change the reference frame,
the time-step size, the output etc. through the options provided. Check available options with

.. code-block:: bash

    $ eph --help
