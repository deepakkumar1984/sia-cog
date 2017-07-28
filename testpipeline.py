from Interface import utility, Pipeline

if __name__ == '__main__':
    Pipeline.init(Pipeline, 'housing')
    Pipeline.Run()
    result = Pipeline.Output('data_featureselection')
    print(result)
    Y = Pipeline.Predict('test.csv', True)

    print(Y)

    