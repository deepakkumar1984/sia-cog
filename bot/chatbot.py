from chatterbot import ChatBot
import chatterbot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import pickle
import os
import shutil
import simplejson as json
from datetime import datetime
from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware, Serializer

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

def getBot(name):
    botfolder = "./data/__chatbot/" + name
    if not os.path.exists(botfolder):
        raise Exception("Chat bot does not exists!")

    dbpath = "sqlite:///" + botfolder + "/bot.db"
    with open(botfolder + "/bot.json", "r") as f:
        botjson = json.load(f)

    bot = ChatBot(
        name,
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri=dbpath,
        filters=["chatterbot.filters.RepetitiveResponseFilter"],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace',
            'chatterbot.preprocessors.convert_to_ascii'
        ],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                "statement_comparision_function": "chatterbot.comparisions.levenshtein_distance",
                "response_selection_method": "chatterbot.response_selection.get_first_response"
            }
        ]
    )

    return bot

def create(name, serviceName, threshold=0.65, defaultResponse="I am sorry, but I do not understand."):
    botfolder = "./data/__chatbot/" + serviceName
    if os.path.exists(botfolder):
        raise Exception("Chat bot already exists!")

    os.mkdir(botfolder)

    botjson = {"name": name, "servicename": serviceName, "threshold": threshold, "default_response": defaultResponse}

    with open(botfolder + "/bot.json", "wb") as f:
        json.dump(botjson, f)

def update(name, serviceName, threshold=0.65, defaultResponse="I am sorry, but I do not understand."):
    botfolder = "./data/__chatbot/" + serviceName
    if not os.path.exists(botfolder):
        raise Exception("Chat bot does not exists!")

    botjson = {"name": name, "servicename": serviceName, "threshold": threshold, "default_response": defaultResponse}
    with open(botfolder + "/bot.json", "wb") as f:
        json.dump(botjson, f)

def delete(name):
    botfolder = "./data/__chatbot/" + name
    if os.path.exists(botfolder):
        shutil.rmtree(botfolder)

def corpustrain(name, corpus):
    bot = getBot(name)
    bot.set_trainer(ChatterBotCorpusTrainer)
    corpus = "chatterbot.corpus.english." + corpus
    bot.train(corpus)

def train(name, data):
    bot = getBot(name)
    bot.set_trainer(ListTrainer)
    bot.train(data)

def predict(name, text):
    botfolder = "./data/__chatbot/" + name
    if not os.path.exists(botfolder):
        raise Exception("Chat bot does not exists!")

    with open(botfolder + "/bot.json", "r") as f:
        botjson = json.load(f)

    bot = getBot(name)
    response = bot.get_response(text.lower())
    result = {"confidence": response.confidence, "response_text": response.text}
    if float(response.confidence) < float(botjson["threshold"]):
        result = {"confidence": response.confidence, "response_text": botjson["default_response"]}
    return result

def saveTrainingData(name, corpus, data):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    db = TinyDB('./data/__chatbot/' + name + '/train_db.json', storage=serialization)
    db.insert({"corpus": corpus, "data": data, "train_date": datetime.now()})

def getTrainingData(name):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    db = TinyDB('./data/__chatbot/' + name + '/train_db.json', storage=serialization)
    return db.all()

def resetBot(name):
    botfolder = "./data/__chatbot/" + name
    if not os.path.exists(botfolder):
        raise Exception("Chat bot does not exists!")

    os.remove(botfolder + "/bot.db")
    os.remove(botfolder + "/train_db.json")
