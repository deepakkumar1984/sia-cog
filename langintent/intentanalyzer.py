import simplejson as json
from tinydb import TinyDB, Query
from tinydb.operations import delete
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine
from Interface import utility
import pickle
import os

entity_db =  TinyDB("./data/__intent/entity_db.json")
intent_db = TinyDB("./data/__intent/intent_db.json")

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

def saveEntity(entityName, keywords):
    q = Query()
    entityName = entityName.lower()

    list = []
    for k in keywords:
        if k == "":
            continue

        if k in list:
            continue

        list.append(k.lower())

    entity_db.update({"keywords": list}, q.name == entityName)

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

    q = Query()
    entity_db.update({"required_entities": rlist, "optional_entities": olist}, q.name == intentName)
def getEntityRecords(name = ""):
    name = name.lower()
    Entity = Query()

    if name == "all":
        result = entity_db.all()
    else:
        result = entity_db.get(Entity.name == name)

    return result

def getIntentRecords(name=""):
    name = name.lower()
    Intent = Query()

    if name == "all":
        result = intent_db.all()
    else:
        result = intent_db.get(Intent.name == name)

    return result

def deleteEntity(name):
    name = name.lower()
    Entity = Query()
    el = entity_db.get(Entity.name == name)
    if not el is None:
        entity_db.remove(eids = [el.eid])

def deleteIntent(name):
    name = name.lower()
    Intent = Query()
    el = intent_db.get(Intent.name == name)
    if not el is None:
        intent_db.remove(eids=[el.eid])

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
    engine = IntentDeterminationEngine()
    entities = entity_db.all()

    for e in entities:
        engine = buildEntity(engine, e["name"], e["keywords"])

    intents = intent_db.all()
    for i in intents:
        engine = buildIntent(engine, i["name"], i["required_entities"], i["optional_entities"])

    with open("./data/__intent/model.out", "wb") as f:
        pickle.dump(engine, f)

def predict(text, confidence=0.1):
    modelpath = "./data/__intent/model.out"
    if not os.path.exists(modelpath):
        raise Exception("Please train the model")

    with open(modelpath, "rb") as f:
        trainedEngine = pickle.load(f)

    intents = trainedEngine.determine_intent(text.lower())
    result = []
    for intent in intents:
        if intent and intent.get('confidence') > confidence:
            result.append(intent)

    return result



