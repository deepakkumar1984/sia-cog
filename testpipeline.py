from Interface import utility, Pipeline

if __name__ == '__main__':
    Pipeline.init(Pipeline, 'imgcls', "imagenet")
    Pipeline.Run()
    #result = Pipeline.Output('data_featureselection->2', to_json=True)
    #print(result)
    Y = Pipeline.Predict('dog.jpg', True)
    print(Y)

    