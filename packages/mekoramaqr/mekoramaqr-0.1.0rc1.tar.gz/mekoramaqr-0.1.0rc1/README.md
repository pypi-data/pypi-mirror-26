# MekoramaQR #

MekoramaQR allows managing Mekorama level QR Codes, including reading, modifying and writing. It is a Python 2.7 project as it relies on zbar library (not available from Python 3). Everything still in progress and needs to be improved.

### Usage ###

It is to be used as a console only program (CLI). From the repo, and once all dependencies are satisfied, run the mekoramaqr module:

~~~~
$ python2 -m mekoramaqr -h
usage: qrstart.py [-h] [-j JSON] [-r RAW] [-c CODE] [--qr QR] qrimage

Decode Mekorama levels

positional arguments:
  qrimage               Image file containing a QR Code for a level

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Output json description
  -r RAW, --raw RAW     Output compressed QR data
  -c CODE, --code CODE  Output uncompressed level data
  --qr QR               Re-write level data to QR Code
~~~~

### Installation ###

Depending on you're using virtualenv or not things could be different. the `requirements.txt` file is an indication on what is needed but not sufficient for some dependencies. I assume that you are using a Linux system such as Ubuntu/Debian. From Windows things are possible but more difficult. In such a case it would be quite interesting to activate the new Linux Subsystem if on Windows 10.

Here is the prerequisite installation for some specific modules:

- Installing numpy
~~~~
$ sudo apt install python-dev
$ pip install numpy
~~~~

- Installing zbar
~~~~
$ sudo apt-get install libzbar-dev
$ pip install zbar
~~~~

  - Note that on Mac OSX, the following patched version of zbar is required:
~~~~
$ pip install git+https://github.com/npinchot/zbar.git
~~~~

When basic dependencies are installed it is time to complete them with
~~~~
$ pip install -r requirements.txt
~~~~
