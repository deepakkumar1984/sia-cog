#!/usr/bin/env bash
sudo apt-get update && apt-get install -y python-setuptools python-pip python-dev git cmake build-essential wget unzip
sudo apt-get install -y libopencv-dev libssl-dev libffi-dev libfann-dev swig tesseract-ocr python-tk openmpi-bin

python -m pip install --upgrade pip
sudo pip install setuptools Flask Cython Keras tensorflow mxnet-cu80 sklearn pandas matplotlib h5py pillow requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot urllib3 easydict padatious seaborn mpld3 psutil nvidia-ml-py flask_cors passlib flask-sqlalchemy
sudo pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
sudo apt-get -y install openmpi-bin
sudo pip install https://cntk.ai/PythonWheel/GPU/cntk-2.1-cp27-cp27mu-linux_x86_64.whl
sudo apt-get clean
sudo apt-get autoremove -y
