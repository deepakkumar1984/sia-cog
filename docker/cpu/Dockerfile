FROM ubuntu:16.04

RUN echo 'building CPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / CPU version"

RUN ln -sf /dev/stdout /var/log/siacog.log
RUN ln -sf /dev/stderr /var/log/siacog.log

RUN useradd -ms /bin/bash sia

RUN apt-get update && apt-get install -y python-pip python-dev git cmake build-essential wget unzip
RUN apt-get install -y libopencv-dev libssl-dev libffi-dev libfann-dev swig tesseract-ocr python-tk openmpi-bin
RUN pip install setuptools Flask Cython Keras mxnet sklearn pandas matplotlib h5py pillow tinydb requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot tensorflow urllib

ENV KERAS_BACKEND=tensorflow

WORKDIR /opt
RUN git clone https://github.com/deepakkumar1984/sia-cog.git
WORKDIR /opt/sia-cog/vis
RUN make

WORKDIR /opt/sia-cog/data
VOLUME ["/data"]

WORKDIR /opt/sia-cog/data/__vision
RUN mkdir weights

RUN chown -R sia:sia /opt/sia-cog

USER sia
WORKDIR /opt/sia-cog
CMD python runserver.py
EXPOSE 5555

