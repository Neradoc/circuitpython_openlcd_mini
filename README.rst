Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-openlcd-mini/badge/?version=latest
    :target: https://circuitpython-openlcd-mini.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/Neradoc/CircuitPython_openlcd_mini/workflows/Build%20CI/badge.svg
    :target: https://github.com/Neradoc/CircuitPython_openlcd_mini/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Small driver for Sparkfun OpenLCD/SerLCD for Circuitpython


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install openlcd_mini

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python
    import time
    import board
    import openlcd_mini

    lcd = openlcd_mini.OpenLCD(board.I2C())
    lcd.write("Hello World !")

    lcd.backlight = 0xFFFF00

    for x in range(0,13):
        lcd.move(x,2)
        lcd.write("Hi")
        time.sleep(.5)


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-openlcd-mini.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/Neradoc/CircuitPython_openlcd_mini/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
