##Create new service
Invoke the service using: http://<host>:<port>/api/ml/create

Example:
```
http://localhost:5555/api/ml/create
```

Since the API need input data in JSON format, here are the various parameters:


* **name**: Display name of the service
* **servicename**: Name of the service used with API. Alpha Numeric without space and special character
* **data_format**: Data format for training and testing. Currently supported format is "csv" and "image"
* **model_type**: model type (general or mlp). General algorithms are linear, logistic, decision tree, SVM etc. MLP refers to deep learning models build with multiple layers of the artificial neural network.

Example of general service with csv data format:

```
{"name": "housing regression", "servicename": "housing", "data_format": "csv", "model_type": "general"}
```

Example of mlp service with image data format:
```
{"name": "Cifar 10 Cls", "servicename": "cifar10", "data_format": "image", "model_type": "mlp"}
```

##Update service
Invoke the service using: http://<host>:<port>/api/ml/update/<servicename>

Example:
```
http://localhost:5555/api/ml/update/housing
```

The input data is same as creating. Please do not change the servicename parameter otherwise the API will throw an error. Other parameters can be modified.

##Delete Service
Invoke the service using: http://<host>:<port>/api/ml/delete/<servicename>

Example:
```
http://localhost:5555/api/ml/delete/housing
```

This will delete all the models and uploaded data.

##Upload Files
Upload training or test data using this api calls. Useful when the service is hosted in another server.

Invoke the service using: http://<host>:<port>/api/ml/upload/<servicename>

Input will be the file in raw format.

Example:
```
http://localhost:5555/api/ml/upload/housing
```

##Deploy Pipeline
Deploy an end-to-end functionality in the form of pipeline. This usually consists of loading of data, split into X and Y, pre-process data and evaluate.

Invoke the service using:  http://<host>:<port>/api/ml/pipeline/<servicename>

Example:
```
http://localhost:5555/api/ml/pipeline/housing
```

##Evaluate Pipleline
Once the pipeline is deployed, now it's time to evaluate the model. 

Invoke the service using:  http://<host>:<port>/api/ml/evaluate/<servicename>

Example:
```
http://localhost:5555/api/ml/evaluate/housing
```

Calling this service triggers a background process since some of the model evaluation like deep learning models takes time to complete the training process. 
The output of the service will be a jobid which you can use to check the status of the job.

##Check Job Status
Some of the evaluation and training processes could take longer. Please use the following service to check the status of the job:

Invoke the service using: http://<host>:<port>/api/ml/jobs/<servicename>?id=<jobid>

Example:
```
http://localhost:5555/api/ml/jobs/housing?id=931ac51b-56e3-43d8-9f21-f1d8928ff78d
```

Example status response:
```
{
      "status": "Completed",
      "end": "2017-08-07 12:39:36.458659",
      "results": {
        "model_build": {
          "normalize": false,
          "n_iter": 300,
          "verbose": false,
          "lambda_2": 1e-06,
          "fit_intercept": true,
          "lambda_1": 1e-06,
          "scores_": [],
          "alpha_": 0.031382,
          "lambda_": 0.143903,
          "alpha_2": 1e-06,
          "tol": 0.001,
          "alpha_1": 1e-06,
          "copy_X": true,
          "_sklearn_version": "0.18.2",
          "coef_": null,
          "intercept_": 16.138925,
          "compute_score": false
        },
        "model_evalute": {
          "std": 76.373538,
          "results": null,
          "mean": -39.400015
        }
      },
      "start": "2017-08-07 12:39:36.238345",
      "id": "931ac51b-56e3-43d8-9f21-f1d8928ff78d"
    }
```

##Traing more epoches
Tha training is applicable to deep learning model (model_type: mlp). The evaluate API call would trigger initial training using the pipeline parameters. But sometimes you would want to train for more iteration using the same model and saved weights. 

Invoke the API using: http://<host>:<port>/api/ml/train/<servicename>

Example:
```
http://localhost:5555/api/ml/train/housing
```

###Input Parameters:

* **epochs**: The number of epochs needs to train more (default: 32)
* **batch_size**: The current training batch size (default: 32)

This is a background process, so you can check the status by calling job status API.