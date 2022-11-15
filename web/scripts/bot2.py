# Using python. first import required libraries
# Using the spacy library, tokenize the sentence
# Determine a time period in the sentence and calculate it in reference to the current date, for example, if the user is searching for the 'weather'  [x periods ago], x being any number, periods being [months, years, weeks, days, etc]
# Determine the tense of the sentence
# Determine the context [dressSense, weather, location, history, stormwatch]
# If the user's IP matches an IP in the ./storage/location.json file, use that location as the default unless specified in the sentence
# if the sentence contains anything related to clothes or asking for a recommendation
# - get the weather information and return a recommendation based on the weather data
# if the sentence contains anything related to the weather
# - if the tense is past, return the weather history data for that day
# - if the tense is future, return the forecast data
# - if present, return the current weather data
# if the user specifies a location, save the location to the ../storage/location.json using the following format:
# {"ip": user_ip, "location": locationFromSentence, "lat": latitudeFromLocation, "lng": longitudeFromLocation}
# if the user already has a location saved, update the location information
# if the user requests stopwatch information, return the Stormwatch information
# Use openweatherapi to get the current weather information
# Use weatherapi to get the history or future weather data
# return the response as a JSON file using the following format:
# {"context": context, "response": response, data: weatherData}
# Use Cleverbot for conversation if context is not found
# Import required libraries
# Please write the code as optimal as possible and not too bulky
# Use whatever libraries you wish to use
# Please write the code in an organised and structured manner
# Please write comments on the sections of code
# Please use git branches and pull requests

import os
import json
import datetime
import openweathermapy.core as owm
import weatherapi as w
# import cleverbotfree as c
import cleverbotfreeapi as c
import spacy


# Initialize the libraries
# Define the default locations

timePeriod = ""

# Define the default locations
cleverbot = c
nlp = spacy.load('en_core_web_sm')
defaultLocation = {
    'ip': '',
    'location': '',
    'lat': '',
    'lng': ''
}

with (open('./config.json', 'r')) as file:
    config = json.load(file)

apiKey = config["weatherapikey"]
oapiKey = config["API_KEY"]
config = {"units": "metric", "lang": "en"}
# Get the current date

# Get the current date
currentDate = datetime.datetime.now().date()

def get_weather_data(lat, long):
    try:
        weather_data = owm.get_current(coords=(lat, long), **config)
        return weather_data
    except Exception:
        return None

def get_weather_history(lat, long):
    try:
        weather_data = w.get_history(apiKey, lat, long)
        return weather_data
    except Exception:
        return None

def get_weather_forecast(lat, long):
    try:
        weather_data = w.get_forecast(apiKey, lat, long)
        return weather_data
    except Exception:
        return None

def get_stormwatch_info(lat, long):
    try:
        weather_data = w.get_stormwatch(apiKey, lat, long)
        return weather_data
    except Exception:
        return None
def write_location(lat, long, location):
    defaultLocation['ip'] = '127.0.0.1'
    defaultLocation['location'] = location
    defaultLocation['lat'] = lat
    defaultLocation['lng'] = long
    with open('./storage/location.json', 'w') as file:
        json.dump(defaultLocation, file)
def read_location():
    with open('./storage/location.json', 'r') as file:
        data = json.load(file)
    return data

def check_if_location_is_saved():
    try:
        data = read_location()
        if data['ip'] != '':
            return True
        else:
            return False
    except Exception:
        return False

def get_lat_long(location):
    try:
        lat = w.get_lat(location)
        lng = w.get_lng(location)
        return lat, lng
    except Exception:
        return None

def calculate_time_period(timePeriod):
    if timePeriod == 'days':
        return 1
    elif timePeriod == 'weeks':
        return 7
    elif timePeriod == 'months':
        return 30
    elif timePeriod == 'years':
        return 365
    else:
        return None
def calculate_diff_in_days(startDate, endDate):
    diffInDays = (endDate - startDate).days
    return diffInDays


def get_response_from_weatherapi(lat, long, date, timePeriod):
    diffInDays = calculate_diff_in_days(currentDate, date)
    if diffInDays < 0:
        return get_weather_history(lat, long)
    elif diffInDays > 0:
        return get_weather_forecast(lat, long)
    else:
        return get_weather_data(lat, long)

def get_response_from_openweathermap(lat, long, context):
    if context == 'dressSense':
        return get_weather_data(lat, long)
    else:
        return None


def get_response(lat, long, date, timePeriod, context):
    if context not in ['dressSense', 'weather', 'location', 'history', 'stormWatch']:
        # return cleverbot.single_exchange(context)
        # return cleverbot.speak(context, one_shot=True)
        return cleverbot.cleverbot(context, session="Sally")
    else:
        if context == 'dressSense':
            return get_response_from_openweathermap(lat, long, context)
        elif context == 'stormWatch':
            return get_stormwatch_info(lat, long)
        else:
            return get_response_from_weatherapi(lat, long, date, timePeriod)

def get_date(sentence):
    timePeriod = None
    tense = None
    for token in sentence:
        if token.text.lower() == 'yesterday':
            return w.get_history()
        if token.text.lower() in ['today', 'now', 'present']:
            return currentDate
        if token.text.lower() == 'tomorrow':
            return w.get_forcast()
        if token.text.lower() in ['days', 'weeks', 'months', 'years']:
            timePeriod = token.text.lower()
        if token.text.lower() in ['ago']:
            tense = 'past'
        if token.text.lower() in ['in']:
            tense = 'future'
    if tense == 'past':
        return w.get_past(calculate_time_period(timePeriod))
    elif tense == 'future':
        return w.get_future(calculate_time_period(timePeriod))
    else:
        return None


# This function checks if the user has a saved location
# It returns true if the user has a saved location, and false if the user does not have a saved location
def check_if_user_has_location():
    try:
        data = read_location()
        if data['ip'] != '':
            return True
        else:
            return False
    except Exception:
        return False


# This function checks if a location is specified in the sentence
# It accepts the tokenized sentence as an argument
# It returns true if a location is specified in the sentence, and false if a location is not specified in the sentence
def check_if_location_is_specified(sentence, keyword):
    for token in sentence:
        if token.text.lower() == keyword:
            return True
    return False


def get_context(sentence):
    context = ''
    for token in sentence:
        if token.text.lower() in ['dress', 'clothes', 'recommendation', 'recommendations', 'dress sense', 'outfit']:
            return 'dressSense'
        elif token.text.lower() in ['weather', 'weathers', 'forecast']:
            return 'weather'
        elif token.text.lower() in ['location', 'locations']:
            return 'location'
        elif token.text.lower() in ['history']:
            return 'history'
        elif token.text.lower() in ['stormwatch']:
            return 'stormWatch'
    return context

def get_location(sentence):
    location = ''
    for token in sentence:
        if token.text.lower() in ['in']:
            i = sentence.index(token)
            if i < len(sentence) - 2:
                return sentence[i + 1].text.lower()
    return location

def check_if_time_period_is_specified(sentence):
    for token in sentence:
        if token.text.lower() in ['days', 'weeks', 'months', 'years']:
            return True
    return False

def check_if_stopwatch_is_specified(sentence):
    for token in sentence:
        if token.text.lower() in ['stormwatch']:
            return True
    return False

def get_location_response(lat, long):
    return {'context': 'location', 'response': 'You location is set to {}'.format(defaultLocation['location']),
            'data': {'lat': lat, 'lng': long}}

def get_history_response(lat, long, timePeriod):
    response = get_response_from_weatherapi(lat, long, w.get_past(calculate_time_period(timePeriod)), timePeriod)
    return {'context': 'history', 'response': 'The weather {} was {}'.format(timePeriod, response),
            'data': {'lat': lat, 'lng': long}}

def get_stormwatch_response(lat, long):
    response = get_response_from_weatherapi(lat, long, currentDate, 'stormWatch')
    return {'context': 'stormWatch', 'response': 'The stormwatch information {} is {}'.format(timePeriod, response),
            'data': {'lat': lat, 'lng': long}}

def get_weather_response(lat, long, date, timePeriod):
    response = get_response_from_weatherapi(lat, long, date, timePeriod)
    return {'context': 'weather', 'response': 'The weather {} was {}'.format(timePeriod, response),
            'data': {'lat': lat, 'lng': long}}

def get_dress_sense_response(lat, long, context):
    response = get_response_from_openweathermap(lat, long, context)
    return {'context': 'dressSense', 'response': 'The weather {} was {}'.format(timePeriod, response),
            'data': {'lat': lat, 'lng': long}}

def get_user_input(userInput):
    sentence = nlp(userInput)
    token = sentence[0]
    keyword = token.text.lower()
    context = get_context(sentence)
    if context == 'location':
        location = get_location(sentence)
        lat, long = get_lat_long(location)
        if check_if_user_has_location() is False:
            write_location(lat, long, location)
        else:
            update_location(lat, long, location)
        return get_location_response(lat, long)
    elif context == 'history':
        if check_if_time_period_is_specified(sentence) is False:
            return {'context': context, 'response': 'Please specify a time period'}
        else:
            timePeriod = get_time_period(sentence)
            lat, long = get_lat_long(defaultLocation['location'])
            return get_history_response(lat, long, timePeriod)
    elif context == 'stormWatch':
        lat, long = get_lat_long(defaultLocation['location'])
        return get_stormwatch_response(lat, long)
    elif context == 'weather':
        date = get_date(sentence)
        if date is None:
            return {'context': context, 'response': 'Please specify a date'}
        elif check_if_time_period_is_specified(sentence) is False:
            return {'context': context, 'response': 'Please specify a time period'}
        else:
            timePeriod = get_time_period(sentence)
            lat, long = get_lat_long(defaultLocation['location'])
            return get_weather_response(lat, long, date, timePeriod)
    elif context == 'dressSense':
        lat, long = get_lat_long(defaultLocation['location'])
        return get_dress_sense_response(lat, long, context)
    else:
        # return {'context': context, 'response': cleverbot.single_exchange(keyword)}
        # return {'context': context, 'response': cleverbot.speak(context, one_shot=True)}
        return {'context': context, 'response': cleverbot.cleverbot(context, session="Sally")}


# # This function checks if the user has a saved location
# # It returns true if the user has a saved location, and false if the user does not have a saved location
# def check_if_user_has_location():
#     try:
#         data = read_location()
#         if data['ip'] != '':
#             return True
#         else:
#             return False
#     except Exception:
#         return False


# # This function gets the latitude and longitude of the user's location
# # It accepts an argument, the user's location
# # It returns the latitude and longitude of the user's location
# def get_lat_long(location):
#     try:
#         lat = w.get_lat(location)
#         lng = w.get_lng(location)
#         return lat, lng
#     except Exception:
#         return None


# This function updates the user's location
# It accepts latitude, longitude and the user's location as arguments
# it updates the user's location in the ../storage/location.json file
def update_location(lat, long, location):
    defaultLocation['ip'] = '127.0.0.1'
    defaultLocation['location'] = location
    defaultLocation['lat'] = lat
    defaultLocation['lng'] = long
    with open('./storage/location.json', 'w') as file:
        json.dump(defaultLocation, file)


# This function gets the time period for the weather information
# It accepts the tokenized sentence as an argument
# It returns the time period for the weather information
def get_time_period(sentence):
    for token in sentence:
        if token.text.lower() in ['days', 'weeks', 'months', 'years']:
            return token.text.lower()


def main(message):
    print(get_user_input(message))


# main()