.. SpeedMeter documentation master file, created by
   sphinx-quickstart on Sat Aug 24 13:03:08 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SpeedMeter's documentation!
======================================

.. image:: ../../screenshot.png
    :width: 50%
    :align: right

This is the documentation for the my SpeedMeter widget for the `Kivy
<https://kivy.org/>`_ platform.

SpeedMeter is a Kivy widget aimed at representing numerical 'physical'
values in a "clock-face" or dial manner. Minimum and maximum value,
and the start and end angle, notably, are fully configurable. For the
sake of readability, the "labels" (intermediate values represented on
the dial) are integers, but you can override the display function to
represent whatever string fits your needs, as illustrated with PI
fractions in :ref:`demo1`.

SpeedMeter is clickable, so you can click on it, and the widget is
able to compute the corresponding physical value.

All default values are "reasonable", so if you do nothing, you get a
working widget for the range 0..100 (asymmetric, because I think it's
cool).

For now, SpeedMeter has been tested under Linux and Android (with
buildozer).

Speedmeter functionalities were heavily inspired by Andrea Gavana's
SpeedMeter for wxPython.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   demos
   api
   wxpython_differences
   todo
   history


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
