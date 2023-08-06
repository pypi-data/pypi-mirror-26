This is a plug-in for Thonny which adds BBC micro:bit IO support. In other words, it allows you to use your micro:bit sensors/leds/etc while writing Python programs that run on your host machine (Mac/Windows/Linux). The micro:bit is simply used as a sensor/output device. More info about Thonny: http://thonny.org



Installation
------------

Preparations
~~~~~~~~~~~~~

Mac and Windows 10 users don't have to worry about preparations and can skip this part.

**Windows 8 and earlier Windows versions**

Before you continue with this guide, make sure that you have installed `this mbed serial port driver <https://os.mbed.com/handbook/Windows-serial-configuration>`_ .


**Linux**

Please add yourself to 'dialout' group (required to access serial ports).

``sudo usermod -a -G dialout <your-username>``

Then relogin or reboot your machine.


Installation
~~~~~~~~~~~~~

- `Install Thonny <http://thonny.org/>`_, if you haven't already.
- Open Thonny and go to Tools -> Manage plug-ins....
- Write ``thonny-flash-microbitio`` in the search bar and click search button, then install it (internet connection is required).
- After plug-in installation restart Thonny.

After these steps you should see a button like this |flash_image| in Thonny's user interface. If you do, then plug-in installation was successful!  However, the plug-in is not helpful unless you also install the cs20-microbitio package:

- go to Tools -> Manage packages...
- Write ``cs20-microbitio`` in the search bar and click the search button, then install the package


Usage
~~~~~~

You should now be able to use your microbit as an input/output device with programs running in Thonny. First, flash the microbit with the I/O .hex file by pressing the |flash_image| button. The microbit led grid should now show an IO logo, which means you can now access the microbit using ``import microbit`` in Thonny. A quick example is::

    import microbit
    microbit.display.scroll("Hello")
    microbit.sleep(2000)


For additional ideas on what you can do, check out the demo code given at `the bitio module readme <https://github.com/whaleygeek/bitio>`_, which is what the cs20-microbitio package contains. *The only reason you installed the cs20-microbitio package instead of the referenced bitio module is that bitio is not yet able to be installed via pip, which means you can't easily install it in Thonny (as of Nov 3, 2017).*


.. |flash_image| image:: thonnycontrib/flash-microbitio/res/run.flash_io.gif