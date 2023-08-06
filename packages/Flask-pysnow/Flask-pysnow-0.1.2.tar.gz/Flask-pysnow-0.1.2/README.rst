.. image:: https://travis-ci.org/rbw0/flask-pysnow.svg?branch=master
    :target: https://travis-ci.org/rbw0/flask-pysnow
.. image:: https://badge.fury.io/py/flask-pysnow.svg
    :target: https://pypi.python.org/pypi/flask-pysnow

Installation
------------
$ pip install flask-pysnow

Configuration
-------------
=======================  ==============  ================
Name                     Default value   Description
=======================  ==============  ================
PYSNOW_INSTANCE          None            Instance name
PYSNOW_HOST              None            FQDN (instead of instance)
PYSNOW_USER              None            
PYSNOW_PASSWORD          None            
PYSNOW_OAUTH             None            Oauth config (if not using user/pass credentials)
PYSNOW_REQUEST_PARAMS    {}              Request params to pass along to the pysnow client
PYSNOW_ENABLE_LOGGING    True            Logs information about requests
PYSNOW_USE_SSL           True
PYSNOW_RAISE_ON_EMPTY    False           Raise exception on empty result sets
=======================  ==============  ================

The Flask-pysnow extension expects `PYSNOW_OAUTH` to contain a dict of `client_id` and `client_secret`


Documentation
-------------
The full documentation is available `here <http://flask-pysnow.readthedocs.org/>`_


Compatibility
-------------
Python 2 and 3. Tested: Python 2.6+ and Python 3.3+


Author
------
Created by Robert Wikman <rbw@vault13.org> in 2017

