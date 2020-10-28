import speech_recognition as sr
from flask import logging, Flask, render_template, request, flash
import azure.cognitiveservices.speech as speechsdk
from utils import *
import random

app = Flask(__name__)
app.secret_key = "VatsalParsaniya"
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

class Sound:
    def __init__(self, event):
        self.event = event
        
mapEventToQuesion = { 'AnyAllergies' : 'AreYouAllergicToAnything',
                     'DescirbePain' : 'CanYouDescribeThePain',
                      'HowFeel':'HowAreYouFeeling',
                      'NameAndBirth' : 'PleaseStateYourNameAndDateOfBirth',
                      'WhatYouNeed' : 'WhatDoYouNeed',
                      'AnyPain' : 'DoYouHaveAnyPain',
                     'The question is not recognized. Please ask again.': 'NotRecognized'
    }
@app.route('/')
def index():
    flash(" Welcome to ConvAI")
    return render_template('index.html')

@app.route('/audio_to_text/')
def audio_to_text():
    flash(" Press Start to start recording audio and press Stop to end recording audio")
    return render_template('audio_to_text.html')

@app.route('/audio', methods=['POST'])
def audio():
    '''
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)
    result = ""
    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='en-IN', show_all=True)
        print(text)
        return_text = " Recognized : <br> "
        try:
            return_text = text['alternative'][0]['transcript']
            result = return_text
            #for num, texts in enumerate(text['alternative']):
            #    return_text += str(num+1) +") " + texts['transcript']  + " <br> "
            #    result += str(num+1) +") " + texts['transcript']
        except:
            return_text = " Sorry!!!! Voice not Detected "
            
    '''
    return_text = " Recognized : <br> "
    region = "eastus"
    subkey = "3f7c2e668a5a4f3ca4923ff200e2db8b"
    speech_config = speechsdk.SpeechConfig(subscription=subkey, region=region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()
    
    print(result.text)
    return_text += result.text + " <br> " 
    
    event = eventRecognized(result.text)
    
    print(event)
    return_text += " <br> Macthed Event : <br> "
    return_text += str(event) + " <br> " 
    
    QDict = getQuestions()
    p = mapEventToQuesion[event]
    print(p)
    #return_text += str(p) + " <br> " 
    print(QDict.keys())
    path = random.choice(QDict[p])[1:]
    #return_text += str(path)
    
    audioElement = '<audio src=' + '"' + path + '"' + ' controls autoplay hidden>' + '   <embed name="GoodEnough"' + 'src=' + '"' + path + '"' + ' loop="false" hidden="true" autostart="true"> <p>If you are reading this, it is because your browser does not support the audio element.</p> </audio>'
    
    songname = Sound(path)

    '''
    region = "eastus"
    subkey = "3f7c2e668a5a4f3ca4923ff200e2db8b"
    speech_config = speechsdk.SpeechConfig(subscription=subkey, region=region)
    audio_input = speechsdk.AudioConfig(filename='/upload/audio.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()

    print(result.text)
    return_text = " Recognized : <br> "
    return_text += result.text + " <br> "
    '''
    return str(return_text) + audioElement

def getFileName():
    return songname.event

if __name__ == "__main__":
    app.run(debug=True)
