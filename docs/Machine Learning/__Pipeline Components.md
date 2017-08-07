Common to all pipeline element:

* **name**: Unique name of the module
* **module**: Actual module (data_loadcsv)

##data_loadcsv
Load the csv file to a dataframe. Following are the json parameters

###input
* **filename**: (string) input filename to be used for evaluating or training

###options
* **column_header**: (boolean) Weather the csv file have header column
* **delim_whitespace**: (boolean) Specifies whether or not whitespace (e.g. ' ' or '    ') will be used as the seperator for columns in csv

###output
**dataframe**: [Pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)

###Example
```
{
    "name": "data_loadcsv",
    "module": "data_loadcsv",
    "input": {
      "filename": "train.csv"
    },
    "options": {
      "column_header": true,
      "delim_whitespace": false
    }
  }
```

##data_loadsample
Load sample dataset for tutorials

###options
**dataset_name**: (string) Sample dataset name to be loaded - cifar10, cifar100, imdb, reuters, mnist, boston_housing

###output
* **X_train**
* ** Y_train**
* **X_test**
* **Y_test**

Read more about this dataset here in the [keras documetation](https://keras.io/datasets/)

###Example
```
{
    "name": "data_loadsample",
    "module": "data_loadsample",
    "options": {
      "dataset_name": "mnist"
    }
  }
```

##data_getxy
Split the dataframe to X and Y required for training the model.

###input
**dataframe**: input dataframe which will be split to X and Y

###options
* **xcols**: Colummns which will act as features, usually terms as X values
* **ycols**: The actual predictions for the X values will be used for training the model.

###Example
```
{
    "name": "data_getxy",
    "module": "data_getxy",
    "input": {
      "dataframe": "output->data_loadcsv"
    },
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
  }
```

##data_handlemissing
By “missing” we simply mean null or “not present for whatever reason”. Many data sets simply arrive with missing data, either because it exists and was not collected or it never existed.
We can use this module to handle those records simply using the following parameters

###input
**dataframe**: input dataframe which will be manipulated

###options
* **type**: dropcolumns | droprows | fillmissing
* **thresh**: (number) required when type is dropcolumns or droprows. Possible values are: -1, 0 or some positive value

-1: drop when all values are null, 

 0: drop if any value is null, 

Positive number: If the value is more than certain threshold number then the value will be dropped

* **strategy**: required when type is fillmissing. Use one of the following value:

“mean”: replace missing values using the mean along the axis.

“median”: replace missing values using the median along the axis.

“most_frequent”: replace missing using the most frequent value along the axis.

 
 ###Example
 