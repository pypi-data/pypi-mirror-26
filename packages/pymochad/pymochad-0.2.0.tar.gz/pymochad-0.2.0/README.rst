========
pymochad
========
A python library for sending commands to the mochad TCP gateway daemon for
the X10 CMA15A controller:

https://sourceforge.net/projects/mochad/

Complete documentation is here: http://pymochad.readthedocs.io/en/latest/

Usage
=====

Using PyMochad is pretty straightforward you just need to init a PyMochad object
and then issue commands to it. For example:

.. code-block:: python

  from pymochad import controller

  mochad = remote.PyMochad()
  print(mochad.status())

will connect to a running mochad instance (running on your localhost) and print
the device status.

You can also send a command directly to a device using a device class. For
example:

.. code-block:: python

  from pymochad import controller
  from pymochad import device

  mochad = controller.PyMochad()
  light_switch = device.Device(mochad, 'a1')
  light_switch.send_cmd('on')

will connect to a running a mochad instance and send the *on* command to the
light switch device at address *a1* on the power line interface.

For a complete API documentation see: :ref:`pymochad_api`.
