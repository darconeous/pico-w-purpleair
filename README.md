Raspberry Pi Pico W AQI Display
===============================

This project builds a WiFi-based display which can show you the AQI from
a [PurpleAir](https://purpleair.com/) air quality sensor.

This project is a work in progress. The code is ugly and not polished. It's
kind of a mess. Don't consider this an official release or anything.
Really you should just move on and forget you saw this.

Still interested?

Ok, read on.

## Required Hardware ##

* Raspberry Pi Pico W
* [Waveshare Pico-LCD-1.114](https://www.waveshare.com/wiki/Pico-LCD-1.14)
* A [PurpleAir](https://purpleair.com/) air quality sensor
* A 3D printer to print the case (Optional)

## Software ##

The software runs in Micropython. Load the wireless micropython firmware
to the Raspberry Pi Pico W board and then use a tool like Thonny to copy
all of the files in `src` over to the Raspberry Pi Pico W board. Make
sure you edit `settings.py` to include the IP address of your PurpleAir
sensor, as well as your WiFi SSID and password!

## License ##

`main.py` and `settings.py` are released under the MIT license. All other
files are covered by their respective licenses.

