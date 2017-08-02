I am assuming you are running Ubuntu with python installed. Python 2 and 3 are supported.

Prerequisite:
*****************
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-tk

Additional Steps (Optional)
***************************
Install CUDA and CuDnn for GPU support --> http://www.pyimagesearch.com/2016/07/04/how-to-install-cuda-toolkit-and-cudnn-for-deep-learning/

Install MxNet --> http://mxnet.io/get_started/install.html

Keras uses Theano as default backend. If you would like to use tensorflow or cntk, please follow the steps in the links provided to install and change the backend as per keras documentation:

1) Tensorflow --> https://www.tensorflow.org/install/
2) CNTK --> https://docs.microsoft.com/en-us/cognitive-toolkit/Setup-Linux-Python
3) Change keras backend --> https://keras.io/backend/

Steps to install and configure:
*******************************

1. Clone the repo with command: git clone https://github.com/deepakkumar1984/ml-api.git

2. cd ml-api

3. sudo pip install -r requirements.txt

4. python runserver.py

If it's successful, it will show the URL which needs to be used for the API calls "Running on http://localhost:5555/ (Press CTRL+C to quit)"
