import simplejson as json
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine
from Interface import projectmgr, constants
from padatious.intent_container import IntentContainer
import pickle
import jsonpickle
import os

def createDataFolder():
    basefolder = "./data/"
    if not os.path.exists(basefolder + "__vision"):
        os.makedirs(basefolder + "__vision")
    if not os.path.exists(basefolder + "__intent"):
        os.makedirs(basefolder + "__intent")
    if not os.path.exists(basefolder + "__chatbot"):
        os.makedirs(basefolder + "__chatbot")
    if not os.path.exists(basefolder + "__text"):
        os.makedirs(basefolder + "__text")
    if not os.path.exists(basefolder + "__vision/weights"):
        os.makedirs(basefolder + "__vision/weights")

createDataFolder()

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

def saveEntity(entityName, keywords):
    entityName = entityName.lower()

    list = []
    for k in keywords:
        if k == "":
            continue

        if k in list:
            continue

        list.append(k.lower())

    projectmgr.UpsertService(entityName, constants.ServiceTypes.LangEntity, {"name": entityName, "keywords": list})

def saveIntent(intentName, required_entities, optional_entities):
    intentName = intentName.lower()

    rlist = []
    olist = []
    for k in required_entities:
        if k == "":
            continue

        if k in rlist:
            continue

        rlist.append(k.lower())

    for k in optional_entities:
        if k == "":
            continue

        if k in olist:
            continue

        if k in rlist:
            continue

        olist.append(k.lower())

    projectmgr.UpsertService(intentName, constants.ServiceTypes.LangIntent, {"name": intentName, "required_entities": rlist, "optional_entities": olist})

def saveUtter(intetName, utter):
    utterpath = "./data/__intent/utter/" + intetName + ".intent"
    if not os.path.exists("./data/__intent/utter/"):
        os.makedirs("./data/__intent/utter")

    with open(utterpath, "w") as f:
        f.writelines(utter)

def getUtter(intetName):
    res = []
    utterpath = "./data/__intent/utter/" + intetName + ".intent"
    if os.path.exists(utterpath):
        with open(utterpath, "r") as f:
            res = f.readlines()
    return res

def getEntityRecords(name = "all"):
    name = name.lower()
    result = []
    if name == "all":
        services = projectmgr.GetServices(constants.ServiceTypes.LangEntity)
        for s in services:
            result.append(json.loads(s.servicedata))
    else:
        service = projectmgr.GetService(name, constants.ServiceTypes.LangEntity)
        result = json.loads(service.servicedata)

    return result

def getIntentRecords(name=""):
    name = name.lower()
    result = []
    if name == "all":
        services = projectmgr.GetServices(constants.ServiceTypes.LangIntent)
        for s in services:
            result.append(json.loads(s.servicedata))
    else:
        service = projectmgr.GetService(name, constants.ServiceTypes.LangIntent)
        result = json.loads(service.servicedata)

    return result

def deleteEntity(name):
    name = name.lower()
    projectmgr.DeleteService(name, constants.ServiceTypes.LangEntity)

def deleteIntent(name):
    name = name.lower()
    projectmgr.DeleteService(name, constants.ServiceTypes.LangIntent)

def buildEntity(engine, entityName, keywords):
    for k in keywords:
        engine.register_entity(k, entityName)
    return engine

def buildIntent(engine, intentName, requiredentities, optionalentities):
    intentBuilder = IntentBuilder(intentName)
    for e in requiredentities:
        intentBuilder.require(e)

    for e in optionalentities:
        intentBuilder.optionally(e)

    intent = intentBuilder.build()
    engine.register_intent_parser(intent)
    return engine

def train():
    id = projectmgr.StartJob("intent", constants.ServiceTypes.LangIntent, 0)
    try:
        engine = IntentDeterminationEngine()
        entities = getEntityRecords()
        container = IntentContainer('intent_cache')

        for e in entities:
            engine = buildEntity(engine, e["name"], e["keywords"])

        intents = getIntentRecords()
        for i in intents:
            engine = buildIntent(engine, i["name"], i["required_entities"], i["optional_entities"])
            utterpath = "./data/__intent/utter/" + i["name"] + ".intent"
            if os.path.exists(utterpath):
                container.load_file(i["name"], utterpath)

        with open("./data/__intent/model.out", "wb") as f:
            pickle.dump(engine, f)

        container.train()
        with open("./data/__intent/container.json", "wb") as f:
            jpicked = jsonpickle.encode(container)
            json.dump(jpicked, f)

        projectmgr.EndJob(id, "Completed", "Completed")
    except Exception as e:
        projectmgr.EndJob(id, "Error", str(e))

def predict(text, confidence=0.1):
    modelpath = "./data/__intent/model.out"
    container = IntentContainer('intent_cache')
    if not os.path.exists(modelpath):
        raise Exception("Please train the model")

    with open(modelpath, "rb") as f:
        trainedEngine = pickle.load(f)

    intents = getIntentRecords()
    for i in intents:
        utterpath = "./data/__intent/utter/" + i["name"] + ".intent"
        if os.path.exists(utterpath):
            container.load_file(i["name"], utterpath)

    foundIntent = False
    intentResult = trainedEngine.determine_intent(text.lower())
    result = []
    try:
        for intent in intentResult:
            if intent and intent.get('confidence') > confidence:
                result.append(intent)
                foundIntent = True
    except Exception as e:
        foundIntent = False

    if not foundIntent:
        data = container.calc_intents(text)
        for n in data:
            if n.conf > confidence:
                result.append({"intent_type": n.name, "confidence": n.conf})

    return result



