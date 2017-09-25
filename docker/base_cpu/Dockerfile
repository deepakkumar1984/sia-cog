FROM ubuntu:16.04

RUN echo 'building CPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / CPU version"

RUN ln -sf /dev/stdout /var/log/siacog.log
RUN ln -sf /dev/stderr /var/log/siacog.log

RUN useradd -ms /bin/bash sia

RUN echo 'building CPU sia-cog image'
RUN apt-get update && apt-get install -y python-setuptools python-pip python-dev git cmake build-essential wget unzip
RUN apt-get install -y libopencv-dev libssl-dev libffi-dev libfann-dev swig tesseract-ocr python-tk openmpi-bin

CMD python -m pip install --upgrade pip
RUN pip install setuptools Flask Cython Keras tensorflow mxnet sklearn pandas matplotlib h5py pillow requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot urllib3 easydict padatious seaborn mpld3 psutil nvidia-ml-py flask_cors passlib flask-sqlalchemy

RUN pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
RUN apt-get -y install openmpi-bin
RUN pip install https://cntk.ai/PythonWheel/CPU-Only/cntk-2.1-cp27-cp27mu-linux_x86_64.whl
ENV KERAS_BACKEND=cntk

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

ENV DOTNET_VERSION 2.0.0
ENV DOTNET_DOWNLOAD_URL https://dotnetcli.blob.core.windows.net/dotnet/Runtime/$DOTNET_VERSION/dotnet-runtime-$DOTNET_VERSION-linux-x64.tar.gz
ENV DOTNET_DOWNLOAD_SHA 2D4A3F8CB275C6F98EC7BE36BEF93A3B4E51CC85C418B9F6A5EEF7C4E0DE53B36587AF5CE23A56BC6584B1DE9265C67C0C3136430E02F47F44F9CFE194219178
RUN curl -SL $DOTNET_DOWNLOAD_URL --output dotnet.tar.gz \
    && echo "$DOTNET_DOWNLOAD_SHA dotnet.tar.gz" | sha512sum -c - \
    && mkdir -p /usr/share/dotnet \
    && tar -zxf dotnet.tar.gz -C /usr/share/dotnet \
    && rm dotnet.tar.gz \
    && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet

RUN apt-get clean
RUN apt-get autoremove -y