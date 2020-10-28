import os
import spacy
from spacy.tokens import Token

nlp = spacy.load('en_core_web_lg') #large language model


def what_match(d, matcher):
    matches=matcher(d)
    if matches:
        return d.vocab.strings[matches[0][0]]
    else:
        return 'The question is not recognized. Please ask again.'
    
## Patterns

anyAllergies = [
    {'POS': {"IN": ["AUX","PART"]}},
    {'POS': 'PRON'},
    {'POS': {"IN": ["AUX","PART","DET"]}, 'OP': '*'},
    {'lemma': {"IN": ['allergic','allergy','hypersensitivity']}}  
    ]

DescirbePain = [
    {'POS': {"IN": ['PRON']}},
    {'POS': {"IN": ["AUX","PART","DET"]}, 'OP': '*'},
    {'lemma': {'IN' : ['describe','characterize','explain','identify']}},
    {'POS': {"IN": ["AUX","PART","DET"]}, 'OP': '*'},
    {'lemma': {'IN' : ['pain']}}
    ]

AnyPain = [
    {'POS': {"IN": ['PRON']}},
    {'lemma': {'IN' : ['have','are']}, 'OP': '?'},
    {'POS': {"IN": ["AUX","PART","DET","ADP"]}, 'OP': '*'},
    {'lemma': {'IN' : ['pain']}}
    ]

HowFeel = [
    {'lemma': 'how'},
    {'POS': 'AUX'},
    {'POS': { 'IN' : ['PRON','DET']}},
    {'lemma': {'IN' : ['feel','do','go']}, 'OP' : '?'}
    ]

NameAndBirth = [
    {'lower': 'your'},
    {'lemma': 'name'},
    {'POS': {"IN": ["AUX","PART","DET","ADP","NOUN",'CCONJ','PRON']}, 'OP': '*'},
    {'ORTH': {'IN' : ['birth','birthday','born']}}
    ]

WhatYouNeed = [
    {'lower': 'what'},
    {'lemma': {'IN' : ['do','is']}},
    {'POS': {"IN": ["AUX","PART","DET","ADP","NOUN",'CCONJ','PRON']}, 'OP': '*'},
    {'lemma': {'IN' : ['need','want','require']}}
    ]

from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)

matcher.add('AnyAllergies', None, anyAllergies )
matcher.add('DescirbePain', None, DescirbePain )
matcher.add('AnyPain', None, AnyPain )
matcher.add('HowFeel', None, HowFeel )
matcher.add('NameAndBirth', None, NameAndBirth )
matcher.add('WhatYouNeed', None, WhatYouNeed )

def eventRecognized(string, nlp=nlp, matcher=matcher):
     return what_match(nlp(string),matcher)
    
def getQuestions():
    questions = []
    pathToSoundFiles = []
    answerDict = {}

    #Getting dirs(what is named as the questions) and reponds.wav paths
    for root, dirs, files in os.walk("./static/SoundFilesCAIPrototype", topdown=False):
        for name in dirs:
            questions.append(name)
            answerDict[name] = {} 

        for name in files:
            p = os.path.join(root, name)      
            pathToSoundFiles.append(p)

    #Creating a dict where each question contains the path for the proper responses  
    for k in answerDict.keys():
        k_list = [key for key in pathToSoundFiles if k in key]

        answerDict[k] = k_list
    answerDict['DidNotUnderstand'] = 'Did Not Understand'
    return answerDict