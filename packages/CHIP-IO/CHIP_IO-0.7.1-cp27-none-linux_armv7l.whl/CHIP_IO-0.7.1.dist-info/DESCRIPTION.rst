CHIP_IO
============================
A CHIP GPIO library

Debian File Installation:

There are now pre-compiled binary deb files for the CHIP that do not require any build tools on a CHIP/CHIP Pro.

Go to this page: https://github.com/xtacocorex/CHIP_IO/releases/latest
Or
Go to this page: https://xtacocorex.github.io/chip_io_releases/index.html

Download the .deb file for the version of Python you are running.
Then install with dpkg, like the following example:

    sudo dpkg -i python-chip-io_0.5.9-1_armhf.deb

Manual Installation::

For Python2.7::

    sudo apt-get update
    sudo apt-get install git build-essential python-dev python-pip flex bison chip-dt-overlays -y
    git clone git://github.com/xtacocorex/CHIP_IO.git
    cd CHIP_IO
    sudo python setup.py install
    cd ..

For Python3::

    sudo apt-get update
    sudo apt-get install git build-essential python3-dev python3-pip flex bison chip-dt-overlays -y
    git clone git://github.com/xtacocorex/CHIP_IO.git
    cd CHIP_IO
    sudo python3 setup.py install
    cd ..

PyPi Installation::

For Python2.7::

    sudo apt-get update
    sudo apt-get install git build-essential python-dev python-pip flex bison chip-dt-overlays -y
    sudo pip install CHIP-IO

For Python3::

    sudo apt-get update
    sudo apt-get install git build-essential python3-dev python3-pip flex bison chip-dt-overlays -y
    sudo pip3 install CHIP-IO

**Usage**

Using the library is very similar to the excellent RPi.GPIO library used on the Raspberry Pi. Below are some examples.

All scripts that require GPIO, PWM (HW and/or SW), and Overlay Manager need to be run with super user permissions!

**Allowable Pin Names for the Library**

The following "table" is the allowable pin names that are able to be used by the library. The Name column is the normal name used on the CHIP Headers, the Alt Name column is the value used by the PocketCHIP header (if it's broken out), and the Key is the Header and Pin Number the the Pin is physically located.  Either of these 3 means is able to specify a pin in CHIP_IO.

  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CHIP (Main Name) | PocketCHIP/CHIP Pro Name | Key (Alt Name) | HW Support      | Edge Detect     |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | TWI1-SDA         | KPD-I2C-SDA              | U13_9          | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | TWI1-SCK         | KPD-I2C-SCL              | U13_11         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D2           | UART2-TX                 | U13_17         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | PWM0             | PWM0                     | U13_18         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | PWM1             | PWM1                     | EINT13         | CHIP PRO        | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D4           | UART2-CTS                | U13_19         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D3           | UART2-RX                 | U13_20         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D6           | LCD-D6                   | U13_21         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D5           | UART2-RTS                | U13_22         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D10          | LCD-D10                  | U13_23         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D7           | LCD-D7                   | U13_24         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D12          | LCD-D12                  | U13_25         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D11          | LCD-D11                  | U13_26         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D14          | LCD-D14                  | U13_27         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D13          | LCD-D13                  | U13_28         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D18          | LCD-D18                  | U13_29         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D15          | LCD-D15                  | U13_30         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D20          | LCD-D20                  | U13_31         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D19          | LCD-D19                  | U13_32         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D22          | LCD-D22                  | U13_33         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D21          | LCD-D21                  | U13_34         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-CLK          | LCD-CLK                  | U13_35         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-D23          | LCD-D23                  | U13_36         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-VSYNC        | LCD-VSYNC                | U13_37         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-HSYNC        | LCD-HSYNC                | U13_38         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LCD-DE           | LCD-DE                   | U13_40         | CHIP            | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | UART1-TX         | UART-TX                  | U14_3          | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | UART1-RX         | UART-RX                  | U14_5          | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | LRADC            | ADC                      | U14_11         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P0           | XIO-P0                   | U14_13         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P1           | XIO-P1                   | U14_14         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P2           | GPIO1                    | U14_15         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P3           | GPIO2                    | U14_16         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P4           | GPIO3                    | U14_17         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P5           | GPIO4                    | U14_18         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P6           | GPIO5                    | U14_19         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | XIO-P7           | GPIO6                    | U14_20         | CHIP            | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | AP-EINT1         | KPD-INT                  | U14_23         | CHIP/CHIP PRO   | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | AP-EINT3         | AP-INT3                  | U14_24         | CHIP/CHIP PRO   | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | TWI2-SDA         | I2C-SDA                  | U14_25         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | TWI2-SCK         | I2C-SCL                  | U14_26         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSIPCK           | SPI-SEL                  | U14_27         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSICK            | SPI-CLK                  | U14_28         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSIHSYNC         | SPI-MOSI                 | U14_29         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSIVSYNC         | SPI-MISO                 | U14_30         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID0            | D0                       | U14_31         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID1            | D1                       | U14_32         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID2            | D2                       | U14_33         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID3            | D3                       | U14_34         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID4            | D4                       | U14_35         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID5            | D5                       | U14_36         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID6            | D6                       | U14_37         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | CSID7            | D7                       | U14_38         | CHIP/CHIP PRO   | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | I2S-MCLK         | EINT19                   | 21             | CHIP PRO        | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | I2S-BCLK         | I2S-BCLK                 | 22             | CHIP PRO        | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | I2S-LCLK         | I2S-LCLK                 | 23             | CHIP PRO        | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | I2S-DO           | EINT19                   | 24             | CHIP PRO        | NO              |
  +------------------+--------------------------+----------------+-----------------+-----------------+
  | I2S-DI           | EINT24                   | 25             | CHIP PRO        | YES             |
  +------------------+--------------------------+----------------+-----------------+-----------------+

**GPIO Setup**

Import the library, and setup as GPIO.OUT or GPIO.IN::

    import CHIP_IO.GPIO as GPIO
    GPIO.setup("CSID0", GPIO.OUT)

You can also refer to the pin number::

    GPIO.setup("U14_31", GPIO.OUT)

You can also refer to the bin based upon its alternate name::

    GPIO.setup("GPIO1", GPIO.IN)

**GPIO Miscellaneous**

Debug can be enabled/disabled by the following command::

    # Enable Debug
    GPIO.toggle_debug()

You can determine if the hardware is a CHIP/CHIP Pro using the following::

    # Determine hardware
    # 0 For CHIP
    # 1 For CHIP Pro
    GPIO.is_chip_pro()

**GPIO Output**

Setup the pin for output, and write GPIO.HIGH or GPIO.LOW. Or you can use 1 or 0.::

    import CHIP_IO.GPIO as GPIO
    GPIO.setup("CSID0", GPIO.OUT)
    GPIO.output("CSID0", GPIO.HIGH)

**GPIO Input**

Inputs work similarly to outputs.::

    import CHIP_IO.GPIO as GPIO
    GPIO.setup("CSID0", GPIO.IN)

Other options when setting up pins::

    # Specify pull up/pull down settings on a pin
    GPIO.setup("CSID0", GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Specify initial value for an output
    GPIO.setup("CSID0", GPIO.OUT, initial=1)

Pull Up/Down values are only for pins that are provided by the R8, the XIO are not capable of this.  The allowable values are: PUD_OFF, PUD_UP, and PUD_DOWN.

Polling inputs::

    if GPIO.input("CSID0"):
        print("HIGH")
    else:
        print("LOW")

Read lots of data::

    # Get 8 bits of data in one shot
    mybyte = GPIO.read_byte("LCD-D3")

    # Get 16 bits of data in one shot
    myword = GPIO.read_word("XIO-P4")

This code was initially added by brettcvz and I cleaned it up and expanded it.

You can quickly change a pins direction::

    GPIO.direction("XIO-P3", GPIO.OUT)
    GPIO.direction("XIO-P3", GPIO.IN)

You can also re-setup a pin in order to change direction, note that this is a slower operation::

    GPIO.setup("XIO-P3", GPIO.OUT)
    GPIO.setup("XIO-P3", GPIO.IN)

The edge detection code below only works for the AP-EINT1, AP-EINT3, and XPO Pins on the CHIP.

Waiting for an edge (GPIO.RISING, GPIO.FALLING, or GPIO.BOTH::

    GPIO.wait_for_edge(channel, GPIO.RISING)

Detecting events::

    GPIO.setup("XIO-P0", GPIO.IN)
    GPIO.add_event_detect("XIO-P0", GPIO.FALLING)
    #your amazing code here

    #detect wherever:
    if GPIO.event_detected("XIO-P0"):
        print "event detected!"

CHIP_IO can also handle adding callback functions on any pin that supports edge detection.  Note that only one callback function can be specified per Pin, if you try to set more, an exception will be thrown.::

    def mycallback(channel):
        print("we hit the edge we want")

    GPIO.setup("GPIO3", GPIO.IN)

    # Add Event Detect and Callback Separately for Falling Edge
    GPIO.add_event_detect("GPIO3", GPIO.FALLING)
    GPIO.add_event_callback("GPIO3", mycallback)

    # Add Event Detect and Callback Separately for Rising Edge
    GPIO.add_event_detect("GPIO3", GPIO.RISING)
    GPIO.add_event_callback("GPIO3", mycallback)

    # Add Callback for Both Edges using the add_event_detect() method
    GPIO.add_event_detect("GPIO3", GPIO.BOTH, mycallback)

    # Remove callback with the following
    GPIO.remove_event_detect("GPIO3")

    # bouncetime is also able to be set for both GPIO.add_event_detect() and GPIO.add_event_callback()
    GPIO.add_event_detect("GPIO3", GPIO.FALLING, bouncetime=300)
    GPIO.add_event_callback("GPIO3", GPIO.RISING, mycallback, bouncetime=300)

**GPIO Cleanup**

To clean up the GPIO when done, do the following::

    # Clean up every exported GPIO Pin
    GPIO.cleanup()

    # Clean up a single pin (keeping everything else intact)
    GPIO.cleanup("XIO-P0")

**PWM**::

Hardware PWM requires a DTB Overlay loaded on the CHIP to allow the kernel to know there is a PWM device available to use.
::
    import CHIP_IO.PWM as PWM
    # Determine hardware
    # 0 For CHIP
    # 1 For CHIP Pro
    PWM.is_chip_pro()

    # Enable/Disable Debug
    PWM.toggle_debug()

    #PWM.start(channel, duty, freq=2000, polarity=0)
    #duty values are valid 0 (off) to 100 (on)
    PWM.start("PWM0", 50)
    PWM.set_duty_cycle("PWM0", 25.5)
    PWM.set_frequency("PWM0", 10)

    # To stop PWM
    PWM.stop("PWM0")
    PWM.cleanup()

    #For specific polarity: this example sets polarity to 1 on start:
    PWM.start("PWM0", 50, 2000, 1)

**SOFTPWM**::

    import CHIP_IO.SOFTPWM as SPWM
    # Determine hardware
    # 0 For CHIP
    # 1 For CHIP Pro
    SPWM.is_chip_pro()

    # Enable/Disable Debug
    SPWM.toggle_debug()

    #SPWM.start(channel, duty, freq=2000, polarity=0)
    #duty values are valid 0 (off) to 100 (on)
    #you can choose any pin
    SPWM.start("XIO-P7", 50)
    SPWM.set_duty_cycle("XIO-P7", 25.5)
    SPWM.set_frequency("XIO-P7", 10)

    # To Stop SPWM
    SPWM.stop("XIO-P7")

    # Cleanup
    SPWM.cleanup()

    #For specific polarity: this example sets polarity to 1 on start:
    SPWM.start("XIO-P7", 50, 2000, 1)

Use SOFTPWM at low speeds (hundreds of Hz) for the best results. Do not use for anything that needs high precision or reliability.

If using SOFTPWM and PWM at the same time, import CHIP_IO.SOFTPWM as SPWM or something different than PWM as to not confuse the library.

**SERVO**::

    import CHIP_IO.SERVO as SERVO
    # Determine hardware
    # 0 For CHIP
    # 1 For CHIP Pro
    SERVO.is_chip_pro()

    # Enable/Disable Debug
    SERVO.toggle_debug()

    #SPWM.start(channel, angle=0, range=180)
    #angle values are between +/- range/2)
    #you can choose any pin except the XIO's
    SERVO.start("CSID4", 50)
    SERVO.set_angle("CSID4", 25.5)
    SERVO.set_range("CSID4", 90)

    # To Stop Servo
    SERVO.stop("CSID4")

    # Cleanup
    SERVO.cleanup()

The Software Servo control only works on the LCD and CSI pins.  The XIO is too slow to control.

**LRADC**::

The LRADC was enabled in the 4.4.13-ntc-mlc.  This is a 6 bit ADC that is 2 Volt tolerant.
Sample code below details how to talk to the LRADC.::

    import CHIP_IO.LRADC as ADC
    # Enable/Disable Debug
    ADC.toggle_debug()

    # Check to see if the LRADC Device exists
    # Returns True/False
    ADC.get_device_exists()

    # Setup the LRADC
    # Specify a sampling rate if needed
    ADC.setup(rate)

    # Get the Scale Factor
    factor = ADC.get_scale_factor()

    # Get the allowable Sampling Rates
    sampleratestuple = ADC.get_allowable_sample_rates()

    # Set the sampling rate
    ADC.set_sample_rate(rate)

    # Get the current sampling rate
    currentrate = ADC.get_sample_rate()

    # Get the Raw Channel 0 or 1 data
    raw = ADC.get_chan0_raw()
    raw = ADC.get_chan1_raw()

    # Get the factored ADC Channel data
    fulldata = ADC.get_chan0()
    fulldata = ADC.get_chan1()

**SPI**::

SPI requires a DTB Overlay to access.  CHIP_IO does not contain any SPI specific code as the Python spidev module works when it can see the SPI bus.

**Overlay Manager**::

The Overlay Manager enables you to quickly load simple Device Tree Overlays.  The options for loading are:
PWM0, SPI2, CUST.  The Overlay Manager is smart enough to determine if you are trying to load PWM on a CHIP Pro and will fail due to the base DTB for the CHIP Pro supporting PWM0/1 out of the box.

Only one of each type of overlay can be loaded at a time, but all three options can be loaded simultaneously.  So you can have SPI2 without PWM0, but you cannot have SPI2 loaded twice.
::
    import CHIP_IO.OverlayManager as OM
    # The toggle_debug() function turns on/off debug printing
    OM.toggle_debug()

    # To load an overlay, feed in the name to load()
    OM.load("PWM0")

    # To verify the overlay was properly loaded, the get_ functions return booleans
    OM.get_pwm_loaded()
    OM.get_spi_loaded()

    # To unload an overlay, feed in the name to unload()
    OM.unload("PWM0")

To use a custom overlay, you must build and compile it properly per the DIP Docs: http://docs.getchip.com/dip.html#development-by-example
There is no verification that the Custom Overlay is setup properly, it's fire and forget
::
    import CHIP_IO.OverlayManager as OM
    # The full path to the dtbo file needs to be specified
    OM.load("CUST","/home/chip/projects/myfunproject/overlays/mycustomoverlay.dtbo")

    # You can check for loading like above, but it's really just there for sameness
    OM.get_custom_loaded()

    # To unload, just call unload()
    OM.unload("CUST")

**OverlayManager requires a 4.4 kernel with the CONFIG_OF_CONFIGFS option enabled in the kernel config.**

**Utilties**::

CHIP_IO now supports the ability to enable and disable the 1.8V port on U13.  This voltage rail isn't enabled during boot.

To use the utilities, here is sample code::

    import CHIP_IO.Utilities as UT
    # Enable/Disable Debug
    UT.toggle_debug()

    # Enable 1.8V Output
    UT.enable_1v8_pin()

    # Set 2.0V Output
    UT.set_1v8_pin_voltage(2.0)

    # Set 2.6V Output
    UT.set_1v8_pin_voltage(2.6)

    # Set 3.3V Output
    UT.set_1v8_pin_voltage(3.3)

    # Disable 1.8V Output
    UT.disable_1v8_pin()

    # Get currently-configured voltage (returns False if the pin is not enabled as output)
    UT.get_1v8_pin_voltage()

    # Unexport Everything
    UT.unexport_all()

    # Determine if you are running a CHIP/CHIP Pro
    # This returns True if the computer is a CHIP Pro and False if it is a CHIP
    UT.is_chip_pro()

**Running tests**

Install py.test to run the tests. You'll also need the python compiler package for py.test.::

    # Python 2.7
    sudo apt-get install python-pytest
    # Python 3
    sudo apt-get install python3-pytest

To run the tests, do the following.::

    # If only one version of Python is installed
    # Python 2
    sudo make pytest2
    # Python 3
    sudo make pytest3
    # If more than one version of Python, run through both
    sudo make test

**Credits**

The CHIP IO Python library was originally forked from the Adafruit Beaglebone IO Python Library.
The BeagleBone IO Python library was originally forked from the excellent MIT Licensed [RPi.GPIO](https://code.google.com/p/raspberry-gpio-python) library written by Ben Croston.

**License**

CHIP IO port by Robert Wolterman, released under the MIT License.
Beaglebone IO Library Written by Justin Cooper, Adafruit Industries. BeagleBone IO Python library is released under the MIT License.
0.7.1
---
* Merged in PR #79
* Merged in PR #80
* Added message notifying user of the gpio set direction retry

0.7.0
---
* Added ability to specify GPIO only as a number, this doesn't work for PWM/SPWM/LRADC/SERVO

0.6.2
---
* Implementation for #77 - ability to push up binary pypi
* Implementation for #75 - wait_for_edge timeout

0.6.1
---
* Fixing implementation for #76

0.6
---
* Random comment cleanup
* Implement fix for #76
* API documentation added
* Closing #74

0.5.9
---
* Merged PR#70 to enable the underlying C code to be used properly in C based code
* Updated README to add missing pins on the CHIP Pro that are available as GPIO
* Updated README to denote pins that are available for Edge Detection

0.5.8
---
* Added 3 pins for the CHIP Pro as allowable for setting callbacks and edge detection to close out Issue #68

0.5.7
---
* Added the I2S pins on the CHIP Pro as GPIO capable
* Added per PWM/SoftPWM cleanup per Issue #64

0.5.6
---
* Fix for Issue #63 where re-setting up a pin wasn't lining up with RPi.GPIO standards. Calling setup after the first time will now update direction.
* README updates to point out the direction() function since that was missing

0.5.5
---
* Fix for Issue #62 where using alternate name of an XIO would cause a segfault due to trying to set pull up/down resistor setting

0.5.4
---
* Re-enabled the polarity setting for PWM based upon Issue #61
* Fixed a 1 letter bug was trying to write inverted to polarity when it wants inversed (such facepalm)
* Cleaned up the polarity setting code to work when PWM is not enabled
* Fixed the unit test for pwm to verify we can set polarity

0.5.3
---
* Fixes to the PWM pytest
* Added pytest for LRADC and Utilities
* Makefile updates for all the things

0.5.2
---
* Updating Utilties to determine CHIP Pro better
* Updating the README to fix things

0.5.0
---
* CHIP Pro Support
* README Updates

0.4.0
---
* Software Servo code added
  - Only works on the LCD and CSI pins
* Fixed cleanup() for the SOFTPWM and SERVO
  - The per pin cleanup for SOFTPWM doesn't work as stop() clears up the memory for the pin used
  - SERVO code was based on SOFTPWM, so it inherited this issue

0.3.5
---
* Merged in brettcvz's code to read a byte of data from the GPIO
  - Cleaned the code up and expanded it (in the low level C code) to read up to 32 bits of data
  - Presented 8 bit and 16 bits of data functions to the Python interface with brettcvz's read_byte() and my read_word()
* I think I finally fixed the GPIO.cleanup() code one and for all

0.3.4.1
---
* Quick fix as I borked XIO setup as inputs with the latest change that enabled PUD

0.3.4
---
* Pull Up/Pull Down resistor setting now available for the R8 GPIO.
* Some general cleanup

0.3.3
----
* Added Debug printing for all the capabilities with the toggle_debug() function
* Added 2 functions from @streamnsight for PWM that allow for setting the period of the PWM and the Pulse Width, both in nanoseconds
* Fixed the SPI2 overlay stuff by using the NTC overlay instead of mine.

0.3.2
----
* Fixing issue #53 to handle the return values of the set functions in pwm_enable.
* Start of whole library debug for #55

0.3.1
----
* Fixing issue #50 where I broke GPIO.cleanup() and SOFTPWM.cleanup() when no input is specified.

0.3.0
----
* Added setmode() function for GPIO to maintain compatibility with Raspberry Pi scripts, this function literally does nothing
* Added per pin cleanup functionality for GPIO and SoftPWM so you can unexport a pin without unexporting every pin
* Updated README to make edge detection wording a little better and to add the per pin cleanup code
* Version update since I blasted through 3 issues on github and feel like we need a nice bump to 0.3

0.2.7
----
* Fix to the Enable 1.8V Pin code as it wasn't working due to bit shifting isn't allowed on a float.
* Updated README to denote the PocketCHIP Pin names better

0.2.6
----
* Fix to keep the GPIO value file open until the pin is unexported (issue #34)

0.2.5
----
* Updates to the pytest code for HWPWM and SoftPWM
* Removed the i2c-1 load/unload support in OverlayManager as CHIP Kernel 4.4.13 has that bus brought back by default

0.2.4
----
* HW PWM Fixed
  - Start/Stop/Duty Cycle/Frequency settings work
  - Polarity cannot be changed, so don't bother setting it to 1 in start()
* Added the unexport_all() function to Utilites

0.2.3
----
* LRADC Support
* Added Utilities
  - Enable/Disable the 1.8V Pin
  - Change 1.8V Pin to output either 2.0V, 2.6V, or 3.3V
    (Current limited to 50mA)

0.2.2
----
* Fixes for Issue #16
  - Pass SoftPWM setup errors to Python layer (aninternetof)
  - Updated spwmtest.py to test for this issue

0.2.1
----
* Pull request #12 fixes:
 - Fixed indent in the i2c-1 dts
 - Removed import dependencies in the SPI and PWM overlays
 - Re-enabled building of the dtbo on setup.py install

0.2.0
----
* Added the ability to load DTB Overlays from within CHIP_IO
 - Support for PWM0, SPI2, and I2C-1 (which comes back as i2c-3 on the 4.4 CHIP
 - Support for a custom DTB Overlay
* Fixes to the pwm unit test, all but 2 now pass :)

0.1.2
----
* SoftPWM Fix by aninternetof
* Added a verification test for SoftPWM

0.1.1
----
* Some refactoring of the edge detection code, made it function better
* Added Rising and Both edge detection tests to gptest.py
  - Small issue with both edge triggering double pumping on first callback hit

0.1.0
----
* Fixed edge detection code, will trigger proper for callbacks now

0.0.9
----
* Fixed SoftPWM segfault
* Added Alternate Names for the GPIOs

0.0.8
----
* Updates to handle the 4.4 kernel CHIPs.  Numerous fixes to fix code issues.
* Added ability to get the XIO base into Python.
* Still need a proper overlay for Hardware PWM and SPI.

0.0.7
----
* GPIO edge detection expanded to include AP-EINT1 and AP-EINT3 as those are the only other pins that support edge detection

0.0.6
----
* Initial PWM
* GPIO edge detection and callback for XIO-P0 to XIO-P7 working

0.0.4
____
* Initial Commit
* GPIO working - untested callback and edge detection
* Initial GPIO unit tests




