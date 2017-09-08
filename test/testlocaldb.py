from Interface import projectmgr, projectmodels
import simplejson as json

#projectmodels.InitDB()
#i.execute({"model_type": "general", "servicename": "housing1", "name": "Housing test", "data_format": "csv"})
#i.execute({"servicename": "objcls", "model_type": "cls", "name": "objcls", "options": {"target_size_y": 224, "target_size_x": 224, "model": "ResNet50"}})
#projectmgr.UpsertService("housing", "ml", {"model_type": "general", "servicename": "housing", "name": "Housing test 111", "data_format": "csv"})
#projectmgr.UpsertService("housing1", "ml", {"model_type": "general", "servicename": "housing1", "name": "Housing test 111", "data_format": "csv"})

recs = projectmgr.GetServices("ml")
print(json.loads(recs[0].servicedata))
