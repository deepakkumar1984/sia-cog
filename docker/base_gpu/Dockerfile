FROM nvidia/cuda

RUN echo 'building GPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / GPU version"

RUN useradd -ms /bin/bash sia

RUN echo 'building GPU sia-cog image'
RUN apt-get install -y curl unzip
RUN apt-get update && apt-get install -y python-pip python-dev git cmake build-essential wget unzip
RUN apt-get install -y libopencv-dev libssl-dev libffi-dev libfann-dev swig tesseract-ocr python-tk

CMD python -m pip install --upgrade pip
RUN pip install setuptools Flask Cython Keras tensorflow mxnet sklearn pandas matplotlib h5py pillow requests simplejson opencv-python jsonpickle pytesseract nltk chatterbot urllib3 easydict padatious seaborn mpld3 psutil nvidia-ml-py flask_cors passlib flask-sqlalchemy

RUN pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
RUN apt-get -y install openmpi-bin
RUN wget https://cntk.ai/PythonWheel/GPU/cntk-2.1-cp27-cp27mu-linux_x86_64.whl
RUN pip install cntk-2.1-cp27-cp27mu-linux_x86_64.whl
CMD rm cntk-2.1-cp27-cp27m-win_amd64.whl
ENV KERAS_BACKEND=cntk

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
RUN sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-xenial-prod xenial main" > /etc/apt/sources.list.d/dotnetdev.list'
RUN apt-get update
RUN apt-get install dotnet-sdk-2.0.0

RUN apt-get clean
RUN apt-get autoremove -y