from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import pickle
import os
import shutil
import simplejson as json

def getBot(name, ):
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
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': botjson["threshold"],
                'default_response': botjson["defaultResponse"]
            },
            {
                'import_path': 'chatterbot.logic.BestMatch',
                "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                "response_selection_method": "chatterbot.response_selection.get_first_response"
            }
        ]
    )

    return bot

def create(name, threshold=0.65, defaultResponse="I am sorry, but I do not understand."):
    botfolder = "./data/__chatbot/" + name
    if os.path.exists(botfolder):
        raise Exception("Chat bot already exists!")

    os.mkdir(botfolder)

    botjson = {"name": name, "threshold": threshold, "defaultResponse": defaultResponse}
    with open(botfolder + "/bot.json", "wb") as f:
        json.dump(botjson, f)

def update(name, threshold=0.65, defaultResponse="I am sorry, but I do not understand."):
    botfolder = "./data/__chatbot/" + name
    if not os.path.exists(botfolder):
        raise Exception("Chat bot does not exists!")

    botjson = {"name": name, "threshold": threshold, "defaultResponse": defaultResponse}
    with open(botfolder + "/bot.json", "wb") as f:
        json.dump(botjson, f)

def delete(name):
    botfolder = "./data/__chatbot/" + name
    if os.path.exists(botfolder):
        shutil.rmtree(botfolder)

def corpustrain(name, list):
    bot = getBot(name)
    bot.set_trainer(ChatterBotCorpusTrainer)
    for l in list:
        if l is None:
            continue
        corpus = "chatterbot.corpus.english." + l
        bot.train(corpus)

def train(name, data):
    bot = getBot(name)
    bot.set_trainer(ListTrainer)
    bot.train(data)

def predict(name, text):
    bot = getBot(name)
    response = bot.get_response(text.tolower())
    return response