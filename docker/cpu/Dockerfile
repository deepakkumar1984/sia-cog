FROM ubuntu:16.04

RUN echo 'building CPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / CPU version"

RUN ln -sf /dev/stdout /var/log/siacog.log
RUN ln -sf /dev/stderr /var/log/siacog.log

RUN useradd -ms /bin/bash sia

RUN apt-get update && apt-get install -y git cmake build-essential libopencv-dev libcurl4-openssl-dev libhdf5-dev libprotobuf-dev wget unzip
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev python-tk
RUN apt-get install -y libfann-dev swig
RUN apt-get install -y tesseract-ocr
RUN pip install setuptools Flask Cython Keras sklearn pandas matplotlib h5py pillow tinydb requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot

WORKDIR /opt
RUN git clone https://github.com/deepakkumar1984/sia-cog.git
WORKDIR /opt/sia-cog/vis/rcnn
make

WORKON /opt/sia-cog
VOLUME ["/data"]

WORKDIR /opt/sia-cog/data/__vision
RUN mkdir weights
WORKDIR /opt/sia-cog/data/__vision/weights

RUN chown -R sia:sia /opt/sia-cog

USER sia
WORKDIR /opt/sia-cog
CMD python runserver.py
EXPOSE 5555

