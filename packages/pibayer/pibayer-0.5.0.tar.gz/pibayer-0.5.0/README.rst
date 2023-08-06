.. image:: https://api.codeclimate.com/v1/badges/66560126d66fb438a9d4/maintainability
   :target: https://codeclimate.com/github/scivision/raspicam-raw-bayer/maintainability
   :alt: Maintainability

======================
raspicam-raw-bayer
======================
Acquire RAW Bayer-masked images with Raspberry Pi camera (before demosaicking).

* writes HDF5 or TIFF compressed image stacks.

:author: Michael Hirsch, Ph.D.

.. contents::

setup
=======
This is meant to be installed directly on the Raspberry Pi::

    apt install python3-numpy python3-matplotlib python3-picamera

    python3 setup.py develop --user

Examples
========

RAW live video display
----------------------
::

    ./getrawimage.py -a
    
Dump image stack to disk
------------------------
HDF5::

    ./getrawimage.py output.h5
    
TIFF::

    ./getrawimage.py output.tif


Command-Line Options
====================

-a            GPU-based preview, for aiming camera (fast)
-p            use Matplotlib for slow, live (10 seconds per frame) display
-e exp_sec    manually set exposure time, up to one second (TODO there are still some auto-set gains)
-8            output 8-bit array instead of default 10-bit array

Reference
========

`Constraints on exposure time <http://picamera.readthedocs.io/en/latest/fov.html#camera-modes>`_


