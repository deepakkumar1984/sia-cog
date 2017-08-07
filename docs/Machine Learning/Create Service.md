Once the server is up and running, please note the base URL which will be something like http://localhost:5555. We are going to use this URL and call various API to create and deploy your machine learning algorithm and expose them as services.

To run the tutorial, I am making use of Postman tool which is an easy to use API calling interface. You are happy to choose any tool you want or run the API call programmatically using any programming language

###Create a service
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
    