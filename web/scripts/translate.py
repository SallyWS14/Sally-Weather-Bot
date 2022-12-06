#pip install googletrans==3.1.0a0

import googletrans
from googletrans import *
import json

translator = Translator()



#Ask sally: could you translate this to {Language}? 
def translateInput(input):

    inputList = input.split("?")    
    translateThis = inputList[1]
    
    #Save languages as a string
    languages = googletrans.LANGUAGES
    languagesString = json.dumps(languages)
    translateTo = ""
    
    #Check which language user gave us 
    for word in inputList[0].split(" "):
        if (word in languagesString) & (word != 'to'):
            translateTo = word
    
    if(translateTo == ""):
        return "Sorry I don't recognize that language, try another one"
    
    # translate 
    result = translator.translate(translateThis, dest=translateTo)
    return result.text

print(translateInput("Translate to french? Hello my name is maya"))
print(translateInput("Translate to uuiuh? Hello my name is maya"))

#Sally can we talk in spanish?
def checkLanguage(input):
    removeQ = input.replace("?", "")
    inputList = removeQ.split(" ")
    
    #Save languages as a string
    languages = googletrans.LANGUAGES
    languagesString = json.dumps(languages)
    translateTo = ""
        
    #Check which language user gave us 
    for word in inputList:
        if (word in languagesString):
            translateTo = word
    
    if(translateTo == ""):
        return "Sorry I don't recognize that language, try another one"
    
    return translateTo
print(checkLanguage("Sally can we talk in spanish?"))

#Translate messages after user asks to change languageus
def sallyTranslate(userInput, language):
    result = translator.translate(userInput, dest=language)
    return result.text
    
print(sallyTranslate("Sally can we talk in spanish?", "Spanish"))    

#Check which language user is speaking in 
def detectLanguage(input):
    userTranslate = input.split("?")
    translateThis = userTranslate[1]
    code = translator.detect(translateThis).lang
    language = googletrans.LANGUAGES[code]
    return language
print(detectLanguage("Detect? Hola"))
