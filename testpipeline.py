from Interface import utility, Pipeline

if __name__ == '__main__':
    Pipeline.init(Pipeline, 'dl1')
    Pipeline.Run()
    #result = Pipeline.Output('model_train')
    #print(result)
    Y = Pipeline.Predict('test.csv', True)

    print(Y)

    