The below installation instruction are for Ubuntu 16.04 and Python 2.

###Clone the repo
```
git clone https://github.com/deepakkumar1984/sia-cog.git
```

###Install dependencies
```
cd sia-cog
```

```
sudo sh installdeb.sh
```

###Additional Steps
***************************
1. Install CUDA and CuDnn for GPU support (Optional): [Follow steps here] (http://www.pyimagesearch.com/2016/07/04/how-to-install-cuda-toolkit-and-cudnn-for-deep-learning)

2. Install MxNet (GPU or CPU) (Required): [Follow steps here] (http://mxnet.io/get_started/install.html)

3. Keras uses Theano as default backend. If you would like to use tensorflow or cntk, please follow the steps in the links provided to install and change the backend as per keras documentation:


  a. Tensorflow --> https://www.tensorflow.org/install/

  b. CNTK --> https://docs.microsoft.com/en-us/cognitive-toolkit/Setup-Linux-Python

  c. Change keras backend --> https://keras.io/backend/
  


###Run the server

```
python runserver.py
```

If it's successful, it will show the URL which needs to be used for the API calls "Running on http://localhost:5555/ (Press CTRL+C to quit)"
