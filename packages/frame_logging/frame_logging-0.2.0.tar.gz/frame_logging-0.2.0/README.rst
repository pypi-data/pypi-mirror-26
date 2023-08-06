=============================
Frame Logging
=============================

.. image:: https://badge.fury.io/py/frame_logging.svg
    :target: https://badge.fury.io/py/frame_logging

.. image:: https://travis-ci.org/ItsfBisounours/frame_logging.svg?branch=master
    :target: https://travis-ci.org/ItsfBisounours/frame_logging

.. image:: https://codecov.io/gh/ItsfBisounours/frame_logging/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ItsfBisounours/frame_logging

Your project description goes here

Documentation
-------------

The full documentation is at https://frame_logging.readthedocs.io.

Quickstart
----------

1. Install Frame Logging::

    pip install frame_logging

2. Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'frame_logging.apps.FrameLoggingConfig',
        ...
    )

3. Create a class to format your extra logging kwargs 

.. code-block:: python

    # 

    class FrameFormatterExample(FrameFormatter):
    
        # format methods
    
        @classmethod
        def get_format_behaviour(cls):
            return OrderedDict([
                ('customer_id', cls.format_customer_id),
            ])
    
        @classmethod
        def format_customer_id(cls, customer_id):
            return "customer_id={}".format(customer_id)
    
        # then if you need to, you can add new method to transform extra kwargs
        # transform methods
    
        @classmethod
        def get_transform_kwargs_methods(cls):
            return   {
                'order': cls.transform_order,
            }
    
        @classmethod
        def transform_order(cls, order, **kwargs):
            kwargs['customer_id'] = order.customer['id']
            return kwargs


4. Configure frame loggin in your settings.py

.. code-block:: python

    # mandatory, if you do not priovide a formatter the app will crash
    FRAME_FORMATTER=FrameFormatterExample()

    # optionnal, default = ' - '
    FRAME_SEPARATOR='+'


5. Use it:

.. code-block:: python

    import frame_logging.log as log

    class Order(object):
        def __init__(self):
            self.customer = {'id': 1}

    log.info('Renewed contract %s', 'test', order=order)
    # 'Renewed contract test - customer_id=1'))



Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
