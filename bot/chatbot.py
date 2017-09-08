from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import os
import simplejson as json

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

def resetBot(name):
    botfolder = "./data/__chatbot/" + name
    if not os.path.exists(botfolder):
        raise Exception("Chat bot folder does not exists!")

    os.remove(botfolder + "/bot.db")
