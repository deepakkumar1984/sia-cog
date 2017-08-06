from libml import pipeline

if __name__ == '__main__':
    pipeline.init(pipeline, 'imgcls', "imagenet")
    #Pipeline.Run()
    #result = Pipeline.Output('data_featureselection->2', to_json=True)
    #print(result)
    Y = pipeline.Predict('dog.jpg', True)
    print(Y)

    