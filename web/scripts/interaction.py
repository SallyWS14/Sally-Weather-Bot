# interaction class to gets a message from the client html, guages the intent with nltk and the training data, then runs a script based on the intent to get weather data, history data, stormwatch data, location data, and dresssense recmmendataions, and sends the data back to the client html
import nltk
import json
import numpy as np
import random

from nltk_utils import bag_of_words, tokenize

class interaction:
    def __init__(self, message):
        self.message = message
        self.currentIntent = None
        self.all_words = []
        self.tags = []
        self.xy = []
        self.ignore_words = ['?', '.', '!']  
        with open('../intents.json', 'r') as f:
            self.intents = json.load(f)
        
    def guageIntent(self):
        """Guages the intent of the message and confidence level and retusn it"""
        # loop through each sentence in our intents patterns
        for intent in self.intents['intents']:
            tag = intent['tag']
            # add to tag list
            self.tags.append(tag)
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = tokenize(pattern)
                # add to our words list
                self.all_words.extend(w)
                # add to xy pair
                self.xy.append((w, tag))
    
    def respond(self, response, embed=False):
        if embed:
            return {
                "title": response.title,
                "data": response.data, # json data
                "message": response.message,
            }
        else:
            return response
            
            
        