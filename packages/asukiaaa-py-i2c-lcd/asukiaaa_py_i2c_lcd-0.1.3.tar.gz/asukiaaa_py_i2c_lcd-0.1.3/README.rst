asukiaaa_py_i2c_lcd
===================

An i2c driver to control lcd from raspberry pi with python.

Useage
======

Install
-------

.. code-block:: shell

   sudo apt install smbus python-pip
   sudo pip install asukiaaa_py_i2c_lcd

Activate I2C of raspberry pi
----------------------------

.. code-block:: shell

   sudo raspi-config

Interface Options -> I2C -> Yes

Connect
-------

+--------------+-----------+
| Raspberry pi | I2C Relay |
+==============+===========+
| 3.3v         | VCC       |
+--------------+-----------+
| 2 (SDA)      | SDA0      |
+--------------+-----------+
| 3 (SCL)      | SCL0      |
+--------------+-----------+
| GND          | GND       |
+--------------+-----------+

+------------+-----+
| I2C Relay  | LCD |
+============+=====+
| VCC (3.3v) | VCC |
+------------+-----+
| SDA1       | SDA |
+------------+-----+
| SCL1       | SCL |
+------------+-----+
| GND        | GND |
+------------+-----+

Run
---

Execute the following command.

.. code-block:: python

   from asukiaaa_py_i2c_lcd.core import I2cLcd, AQM1602_ADDR

   I2C_BUS_NUM = 1

   lcd = I2cLcd(I2C_BUS_NUM, AQM1602_ADDR)
   lcd.setCursor(0,0)
   lcd.write("Hello")
   lcd.setCursor(3,1)
   lcd.write("World")

References
==========

* `raspberry piでLCD（AQM1602）を使い、IPを表示する方法 <http://asukiaaa.blogspot.jp/2016/09/raspberry-pilcdaqm1602ip.html>`_
* `ストロベリー・リナックス/秋月電子のI2C液晶/OLEDほかをArduinoで使う <http://n.mtng.org/ele/arduino/i2c.html>`_
