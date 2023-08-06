.. image:: https://img.shields.io/github/release/dslackw/alarm.svg
    :target: https://github.com/dslackw/alarm/releases
.. image:: https://travis-ci.org/dslackw/alarm.svg?branch=master
    :target: https://travis-ci.org/dslackw/alarm
.. image:: https://landscape.io/github/dslackw/alarm/master/landscape.png
    :target: https://landscape.io/github/dslackw/alarm/master
.. image:: https://img.shields.io/codacy/22fbb1e64acc45a78de3c86233d88d9a.svg
    :target: https://www.codacy.com/public/dzlatanidis/alarm/dashboard
.. image:: https://img.shields.io/pypi/dm/alarm.svg
    :target: https://pypi.python.org/pypi/alarm
.. image:: https://img.shields.io/badge/license-GPLv3-blue.svg
    :target: https://github.com/dslackw/alarm
.. image:: https://img.shields.io/github/stars/dslackw/alarm.svg
    :target: https://github.com/dslackw/alarm
.. image:: https://img.shields.io/github/forks/dslackw/alarm.svg
    :target: https://github.com/dslackw/alarm
.. image:: https://img.shields.io/github/issues/dslackw/alarm.svg
    :target: https://github.com/dslackw/alarm/issues

.. contents:: Table of Contents:

CLI Alarm Clock
===============

.. image:: https://raw.githubusercontent.com/dslackw/images/master/alarm/alarm-clock-icon.png
    :target: https://github.com/dslackw/alarm

Alarm is command line alarm clock utility written in Python language.

How works
---------

When the date and time coincides with the current the alarm starts 
playing the sound is selected for five consecutive times. You can 
pause the alarm by pressing 'p' or 'space' is an attempt to cancel the 
'q' or 'ESC'. Change the volume of the alarm by pressing '*' or '/'.

You can create a list and use it as an alarm sound:

.. code-block:: bash
    
    $ cat *.mp3 > playlist.m3u
    $ alarm -s 17 07:05 ~/Music/playlist.m3u

You will find some sounds in folder alarm/sounds
only GitHub tar archive `alarm-2.1.tar.gz <https://github.com/dslackw/alarm/archive/v2.1.tar.gz>`_ or
zip archive `alarm-2.1.zip <https://github.com/dslackw/alarm/archive/v2.1.zip>`_.
Some will make you laugh, have fun !!!
    
Requirements
------------

.. code-block:: bash

    - Python 2 or 3
    - Mplayer

Installation
------------

Using `pip <https://pip.pypa.io/en/latest/>`_ :

.. code-block:: bash

    $ pip install alarm --upgrade

    uninstall:

    $ pip uninstall alarm
   

Get the source 'git clone https://github.com/dslackw/alarm.git'

.. code-block:: bash
    
    $ python setup.py install


Command Line Tool Usage
-----------------------

.. code-block:: bash

    usage: alarm [-h] [-v]
                 [-s] <day> <alarm time> <song>

    optional arguments
      -h, --help       show this help message and exit
      -v, --version    print version and exit
      -s, --set        set alarm day, time and sound
    
      --config         use config file

    example: alarm -s 21 06:00 /path/to/song.mp3

Example:

.. code-block:: bash
   
    $ alarm -s 18 22:05 ~/alarm/sounds/wake_up.mp3

    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file : ~/alarm/sounds/wake_up.mp3                                      |
    | Time : 21:06:41                                                              |
    +==============================================================================+
    Press 'Ctrl + c' to cancel alarm ...


    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 22:05                                               |
    | Sound file :  ~/alarm/sounds/wake_up.mp3                                     |
    | Time : 22:05 Wake Up !                                                       |
    +==============================================================================+
    Press 'Ctrl + c' to cancel alarm ...
    __        __    _          _   _         _ 
    \ \      / /_ _| | _____  | | | |_ __   | |
     \ \ /\ / / _` | |/ / _ \ | | | | '_ \  | |
      \ V  V / (_| |   <  __/ | |_| | |_) | |_|
       \_/\_/ \__,_|_|\_\___|  \___/| .__/  (_)
                                    |_|
    
    Press 'SPACE' to pause alarm ...                                    
    
    Attempt 1

    Attempt 2

Use config file in $HOME/.alarm/config:

.. code-block:: bash

    $ alarm --config

    +==============================================================================+
    |                              CLI Alarm Clock                                 |
    +==============================================================================+
    | Alarm set at : Wednesday 07:00                                               |
    | Sound file : /home/user/alarm/sounds/funny.mp3                               |
    | Time : 00:09:22                                                              |
    +==============================================================================+
    Press 'Ctrl + c' to cancel alarm ...
