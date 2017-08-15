from nltk.corpus import wordnet, stopwords
import simplejson as json
import jsonpickle
import nltk

def download():
    nltk.download()

def tokenize(data, language="english", filterStopWords = False, tagging = False):
    result = {}
    tags = []
    filterChars = [",", ".", "?", ";", ":", "'", "!", "@", "#", "$", "%", "&", "*", "(", ")", "+", "{", "}", "[", "]", "\\", "|"]
    sent_token = nltk.tokenize.sent_tokenize(data, language)
    word_token = nltk.tokenize.word_tokenize(data, language)
    word_token = [w for w in word_token if not w in filterChars]
    if filterStopWords is True:
        stop_words = set(stopwords.words(language))
        word_token = [w for w in word_token if not w in stop_words]

    if tagging is True:
        tags = nltk.pos_tag(word_token)

    result = {"sent_token": sent_token, "word_token": word_token, "pos_tag": tags}
    return json.loads(jsonpickle.encode(result, unpicklable=False))

def synset(data):
    result = {}
    syns = wordnet.synsets(data)
    list = []
    for s in syns:
        r = {}
        r["name"] = s.name()
        r["lemma"] = s.lemmas()[0].name()
        r["definition"] = s.definition()
        r["examples"] = s.examples()
        list.append(r)

    result["list"] = list
    synonyms = []
    antonyms = []
    for syn in syns:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    result["synonyms"] = synonyms
    result["antonyms"] = antonyms
    return json.loads(jsonpickle.encode(result, unpicklable=False))