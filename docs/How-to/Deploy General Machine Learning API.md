Once the server is up and running, please note the base URL which will be something like http://localhost:5555. We are going to use this URL and call various API to create and deploy your machine learning algorithm and expose them as services.

To run the tutorial, I am making use of Postman tool which is an easy to use API calling interface. You are happy to choose any tool you want or run the API call programmatically using any programming language

## Create a service
Let's take an example of Boston housing regression problem and let's work towards setting up a machine learning service to solve this issue and develop a model to predict the test data.

* URL: http://localhost:5555/api/ml/create
* Type: POST
* Body (application\json): 
```
{
  "name": "Housing Regression Problem",
  "servicename": "housing",
  "data_format": "csv",
  "model_type": "general"
}
```

Once created you will get response below:
```
{
    "message": "Success",
    "statuscode": 200
}
```

## Uploading of training and test data

Lets upload the training and test data so that we can configure the service to predict the set of values using trainng data. 

Simple invoke the following service API with file attached, and it will take care of uploading the files to its dataset folder. This API is useful when you have service is not hosted locally.

```
URI: http://localhost:5555/api/ml/upload/housing
```

You can download the train and test file for housing regression problem here:
* [train.csv](https://siastore.blob.core.windows.net/demo/data/housing/train.csv)
* [test.csv](https://siastore.blob.core.windows.net/demo/data/housing/test.csv)

## Develop and deploy model using train data
Developing a model requires knowledge about the various machine learning algorithm which will fit the need to solve a particular problem. I am covering only few algorithms here and will try to provide you a guide on how to use it for this housing problem. You can learn and free to try to other algorithm. 

The API uses scikit tool for general machine learning model for regression and classification problems. I will cover deep learning model using later which uses keras as the backend tool to run the code.

I would suggest to go through the tutorials here to learn more about general machine learning models: [http://scikit-learn.org/stable/tutorial/index.html](http://scikit-learn.org/stable/tutorial/index.html)

We are using pipeline framework to develop the model. These API calls uses json as input data format.
Sample pipeline json with the element from loading the data, pre-proceesing till model buidling.

```
[
  {
    "input": {
      "filename": "train.csv"
    },
    "name": "data_loadcsv",
    "module": "data_loadcsv",
    "options": {
      "delim_whitespace": false,
      "column_header": true
    }
  },
  {
    "input": {
      "dataframe": "output->data_loadcsv"
    },
    "name": "data_getxy",
    "module": "data_getxy",
    "options": {
      "xcols": [
        "crim",
        "zn",
        "indus",
        "chas",
        "nox",
        "rm",
        "age",
        "dis",
        "rad",
        "tax",
        "ptratio"
      ],
      "ycols": [
        "medv"
      ]
    }
  },
  {
    "input": {
      "dataframe": "output->data_getxy->0"
    },
    "name": "data_preprocess",
    "module": "data_preprocess",
    "method": "StandardScaler"
  },
  {
    "name": "model_build",
    "module": "model_build",
    "method": "BayesianRidge"
  },
  {
    "input": {
      "Y": "output->data_getxy->1",
      "X": "output->data_getxy->0",
      "model": "output->model_build"
    },
    "name": "model_evalute",
    "module": "model_evalute",
    "options": {
      "scoring": [
        "neg_mean_squared_error"
      ],
      "kfold": 25
    }
  },
  {
    "input": {
      "module_output": [
        "model_build",
        "model_evalute"
      ]
    },
    "name": "return_result",
    "module": "return_result"
  }
]
```

## Evalute and Predict
Post this JSON data to the API with parameters:

* URL: http://localhost:5555/api/ml/pipeline/housing
* Type: POST

To learn more about what pipeline element means, please go through the Pipeline Components documentation.

Simple call to evaluate will train the model and ready for you to perform prediction.

**Run Evaluate**

* URL: http://localhost:5555/api/ml/evaluate/housing
* Type: POST

Since the evaluation could be long running process, it runs in the background.
The response of this call will have jobid which you can use to query the status of the job.

For ex: http://localhost:5555/api/ml/jobs/housing?id=931ac51b-56e3-43d8-9f21-f1d8928ff78d

Please refer to the usage guide to understand more about the API usage

**Run Prediction**

Now the model is ready, we can now call the predict API to actually predict the unseen data.

* URL: http://localhost:5555/api/ml/predict/housing
* Type: POST
* Body (application\json): 
```
{
  "testfile": "test.csv"
  "save_prediction": true
}
```

The output will be an array of the predicted values for the dataset.

