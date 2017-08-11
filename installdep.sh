#!/usr/bin/env bash
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev python-tk
sudo apt-get install -y libfann-dev swig
sudo apt-get install -y tesseract-ocr
sudo pip install setuptools Flask Cython Keras sklearn pandas matplotlib h5py pillow tinydb requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot urllib