from ml import pipeline

if __name__ == '__main__':
    pipeline.init(pipeline, 'housing', "general")
    pipeline.Run()
    result = pipeline.Output('data_featureselection->2', to_json=True)
    print(result)
    #Y = pipeline.Predict('dog.jpg', True)
    #print(Y)

    