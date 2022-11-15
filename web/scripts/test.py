# import nltk
# nltk.download('all')

# text = input("Enter a sentence: ")

# tokens = nltk.word_tokenize(text)

# tagged_sent = nltk.pos_tag(tokens)

# print(tagged_sent)
import nltk.tokenize
import spacy
import re
import nltk
from spacy import displacy
from geotext import GeoText
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltkj import word_tokenize, pos_tag
# from web.scripts.test import examinations

sp = spacy.load('en_core_web_sm')

# Write a python script that does the following:
# Determine the tense of the text using the NLTK library
# - If in the past, run a getWeatherHistory() function with weatherapi and return the weather for that day at the current time
# - - If the user specifies a location, use that location
# - If in the future, run a getWeatherForecast() function with weatherapi and return the weather for that day at the current time
# - If in the present, run a getWeather() function with weatherapi and return the weather for that day at the current time
# Determine the location of the user and save the location with an identifying browser cookie to a json file
# use the location as a default unless the user specifies a different location
# Determine if the user is requesting dress recommendations based on the current weather using openweatherapi and return a dress recommendation
# Determine if the user is requesting a stormwatch alert and return a stormwatch alert if there is one
# store the result in a json file and return it with material ui card components

import sys
import nltk
import os, shutil
import re

# open file, read contents, close
# txt = open('text.txt', 'r').read()
txt = input("Enter a sentence: ")
txt = txt.lower()

# split text into sentences
sentences = nltk.sent_tokenize(txt)

# split sentences into words
words = [nltk.word_tokenize(sentence) for sentence in sentences]

# tag words/sentences/text
text_tokens = nltk.pos_tag(words)

# save tagged text to a text file
with open('text_tokens.txt', 'w') as f:
    for (word, tag) in text_tokens:
        f.write(str((word, tag)) + '\n')

# save tagged text to a text file
with open('text_tokens.txt', 'w') as f:
    for (word, tag) in text_tokens:
        f.write(str((word, tag)) + '\n')

# split tagged text into lists of (word, tag) tuples
words, tags = zip(*text_tokens)

# save tagged text to a text file
with open('words.txt', 'w') as f:
    for word in words:
        f.write(word + '\n')

# save tagged text to a text file
with open('tags.txt', 'w') as f:
    for tag in tags:
        f.write(tag + '\n')

# tag text as past/present/future
tense = 'None'
if 'VBD' in tags:
    tense = 'past'
elif 'VBP' in tags or 'VBZ' in tags:
    tense = 'present'
elif 'MD' in tags:
    tense = 'future'

# save tense to a text file
with open('tense.txt', 'w') as f:
    f.write(tense)

# getWeather()
# if tense is present, return the weather for that day at the current time
# if tense is past, return the weather for that day at the current time
# if tense is future, return the weather for that day at the current time
def getWeather(tense, location):
    # TODO
    return None

# getWeatherForecast()
# if tense is present, return the weather for that day at the current time
# if tense is past, return the weather for that day at the current time
# if tense is future, return the weather for that day at the current time
def getWeatherForecast(tense, location):
    # TODO
    return None

# getWeatherHistory()
# if tense is present, return the weather for that day at the current time
# if tense is past, return the weather for that day at the current time
# if tense is future, return the weather for that day at the current time
def getWeatherHistory(tense, location):
    # TODO
    return None

# getLocation()
# determine the location of the user and save the location with an identifying browser cookie to a json file
# use the location as a default unless the user specifies a different location
def getLocation():
    # TODO
    return None

# getDressRecommendations()
# determine if the user is requesting dress recommendations based on the current weather using openweatherapi and return a dress recommendation
def getDressRecommendations(weather):
    # TODO
    return None

# getStormWatch()
# determine if the user is requesting a stormwatch alert and return a stormwatch alert if there is one
def getStormWatch(weather):
    # TODO
    return None

# save result to a json file
def saveResult(result):
    # TODO
    return None

# main
def main():
    # TODO
    return None

main()

# Determine the tense of the sentence
# Determine the context [dressSense, weather, location, history, stormwatch]
# If the user's ip matches an ip in the ../storage/location.json file, use that location as the default unless specified in the sentence
# if sentence contains anything related to clothes or asking for a recommendation
# - get the weather information and return a recommendation based on the weather data
# if sentence contains anything related to weather
# - if the tense is past, return the weather history data for that day
# - if the tense is future, return the forecast data
# - if present, return the current weather data
# if the user specifies a location, save the location to the ../storage/location.json using the following format:
# {"ip": user_ip, "location": locationFromSentence, "lat": latitudeFromLocation, "lng": longitudeFromLocation}
# if the user already has a location saved, updated the location information
# if the user requests stomwatch information, return the stormwatch information
# Use openweatherapi to get the current weather information
# Use weatherapi to get the history, or future weather data
# return the response as a json file using the following format:
# {"context": context, "response": messageOrRecommendation, data: weatherData}