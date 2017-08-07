###Uploading of training and test data

Lets upload the training and test data so that we can configure the service to predict the set of values using trainng data. 

Simple invoke the following service API with file attached, and it will take care of uploading the files to its dataset folder. This API is useful when you have service is not hosted locally.

```
URI: http://localhost:5555/api/ml/upload/housing
```

You can download the train and test file for housing regression problem here:
* [train.csv](https://siastore.blob.core.windows.net/demo/data/housing/train.csv)
* [test.csv](https://siastore.blob.core.windows.net/demo/data/housing/test.csv)