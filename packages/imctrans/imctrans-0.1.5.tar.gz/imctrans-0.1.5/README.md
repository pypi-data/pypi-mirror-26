IMC Bindings Generator
======================

imctrans is a Python 3.x program that translates IMC XML specifications to
source code. Right now only C++ is supported but other languages might be
supported in the future.

Installing from pip
-------------------

```
sudo pip3 install imctrans
```

Installing from source code
-------------------

```
sudo python3 setup.py install
```

Generating C++ Bindings
-----------------------

```
imctrans translate -l cpp -x PATH_TO_IMC_XML -o OUTPUT_FOLDER
```

