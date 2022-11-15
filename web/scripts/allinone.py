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
import datetime
import json
import os
import pickle
import re

import nltk
import nltk.data
import numpy as np
import requests
from flask import jsonify
from nltk import sent_tokenize, word_tokenize


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except (Exception) as e:
        print(e)
        ip = ""
    return ip

def index(request):
    message = request.form["message"]
    ip = get_ip(request)
    location = {}
    log_data = {"ip": ip, "message": message}

    if not message:
        return jsonify({"message": "Please send a message."})
    # load the tokenizer
    # tokenizer = pickle.load(open("../storage/tokenizer.pkl", "rb"))
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    # load the saved model
    # model = load_model("../storage/model.h5")
    # transform the message so that it can be processed
    message = message.lower()
    message = message.replace("'", "")
    message = message.replace("'s", "")
    message = message.replace("’", "")
    message = message.replace("’s", "")
    message = message.replace("“", "")
    message = message.replace("”", "")
    message = message.replace("\n", " ")
    message = message.replace("\r", " ")
    message = message.replace(".", " . ")
    message = message.replace(",", " , ")
    message = message.replace("!", " ! ")
    message = message.replace("?", " ? ")
    message = message.replace("  ", " ")
    message = message.strip()
    # prepare the data for the model
    sentence = [message]
    # sentence = tokenizer.texts_to_sequences(sentence)
    sentence = tokenizer.tokenize(message)
    sentence = pad_sequences(sentence, maxlen=24, dtype="int32", padding="post", truncating="post")
    # predict the context of the message
    prediction = model.predict(sentence)[0]
    context_index = np.argmax(prediction)
    context = ["dressSense", "weather", "location", "history", "stormwatch"][context_index]
    message = message.split(" ")
    message_tense = get_tense(message)

    # get the location
    try:
        current_location = load_location(ip)
        log_data["location_data"] = current_location
        latitude = current_location["lat"]
        longitude = current_location["lng"]
    except:
        latitude = None
        longitude = None

    # if the context is dressSense, get the weather data and return a dress recommendation based on the data
    if context == "dressSense":
        data = get_weather_data(latitude, longitude)
        recommendation = get_recommendation(data)
        response = {"context": context, "response": recommendation, "data": data}
        log_data["recommendation"] = recommendation
        log_data["weather_data"] = data
        log_data["recommendation_type"] = "dressSense"
        log_data["time"] = str(datetime.datetime.now())
        save_log(log_data)
        return jsonify(response)

    # if the context is weather, get the appropriate weather data [current, past, future]
    if context == "weather":
        if message_tense == "past":
            data = get_history_weather_data(latitude, longitude)
            response = {"context": context, "response": data, "data": data}
            log_data["weather_data"] = data
            log_data["response_type"] = "history"
            log_data["time"] = str(datetime.datetime.now())
            save_log(log_data)
            return jsonify(response)
        if message_tense == "present":
            data = get_weather_data(latitude, longitude)
            response = {"context": context, "response": data, "data": data}
            log_data["weather_data"] = data
            log_data["response_type"] = "present"
            log_data["time"] = str(datetime.datetime.now())
            save_log(log_data)
            return jsonify(response)
        if message_tense == "future":
            data = get_forecast_weather_data(latitude, longitude)
            response = {"context": context, "response": data, "data": data}
            log_data["weather_data"] = data
            log_data["response_type"] = "future"
            log_data["time"] = str(datetime.datetime.now())
            save_log(log_data)
            return jsonify(response)

    # if the context is stormwatch, get the stormwatch data
    if context == "stormwatch":
        data = get_stormwatch_data(latitude, longitude)
        response = {"context": context, "response": data, "data": data}
        log_data["stormwatch_data"] = data
        log_data["time"] = str(datetime.datetime.now())
        save_log(log_data)
        return jsonify(response)

    # if the context is location, get the specified location, save the location to storage
    if context == "location":
        location_name = get_location_from_sentence(message)
        if not location_name:
            return jsonify({"context": context, "response": "Please provide a location."})
        latitude, longitude = get_coordinates(location)
        location_data = {"ip": ip, "location": location_name, "lat": latitude, "lng": longitude}
        save_location(location_data)
        log_data["location_data"] = location_data
        log_data["time"] = str(datetime.datetime.now())
        save_log(log_data)
        return jsonify({"context": context, "response": location_name, "data": location_data})

    return jsonify({"response": "Sorry, I don't understand."})

def get_tense(message):
    verb_positions = []
    for i in range(len(message)):
        if message[i] in ["am", "was", "is", "are", "has", "have", "had"]:
            if message[i] == "am":
                return "present"
            if message[i] == "was":
                return "past"
            if message[i] == "is":
                return "present"
            if message[i] == "are":
                return "present"
            if message[i] == "has":
                return "present"
            if message[i] == "have":
                return "present"
            if message[i] == "had":
                return "past"
            if message[i] in ["will", "would", "should"]:
                return "future"
    return ""

def get_recommendation(data):
    if not data:
        return "Sorry, I cannot get the weather information."
    if data["description"] in ["thunderstorm", "drizzle", "rain", "snow"]:
        return "Bring an umbrella."
    if data["description"] in ["mist", "fog"]:
        return "Bring a jacket."
    if data["description"] in ["clear", "clouds"]:
        if data["temp"] >= 20:
            return "You can wear a t-shirt."
        if data["temp"] < 20:
            return "You can wear a jacket."
    return "Sorry, I don't know how to respond to that."

def get_location_from_sentence(sentence):
    for i in range(len(sentence)-1):
        if sentence[i] == "in":
            return " ".join(sentence[i+1:])
    return None

def get_coordinates(location):
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}".format(location))
    if response.status_code != 200:
        return None, None
    data = response.json()
    return data["coord"]["lat"], data["coord"]["lon"]

def save_location(location_data):
    with open("../storage/location.json", "w+") as f:
        f.write(json.dumps(location_data))

def load_location(ip):
    with open("../storage/location.json", "r") as f:
        try:
            data = json.loads(f.read())
            return data
        except:
            return None

def get_stormwatch_data(latitude, longitude):
    if not latitude or not longitude:
        return None
    r = requests.get("https://api.stormglass.io/v1/weather/point?lat={}&lng={}".format(latitude, longitude),
                    headers={"Authorization": "d47e5efb-5c08-11ea-87a8-0242ac130002-d47e5f87-5c08-11ea-87a8-0242ac130002"})
    if r.status_code != 200:
        return None
    data = r.json()
    comments = []
    if len(data["hours"]) == 0:
        return None
    data = data["hours"][0]
    if data["waveDirection"]["noWave"]:
        comments.append("There are no waves.")
    if data["waveDirection"]["northEast"]:
        comments.append("The waves are coming from the north east.")
    if data["waveDirection"]["southEast"]:
        comments.append("The waves are coming from the south east.")
    if data["waveDirection"]["southWest"]:
        comments.append("The waves are coming from the south west.")
    if data["waveDirection"]["northWest"]:
        comments.append("The waves are coming from the north west.")
    if data["waveDirection"]["north"]:
        comments.append("The waves are coming from the north.")
    if data["waveDirection"]["east"]:
        comments.append("The waves are coming from the east.")
    if data["waveDirection"]["south"]:
        comments.append("The waves are coming from the south.")
    if data["waveDirection"]["west"]:
        comments.append("The waves are coming from the west.")
    if data["waveDirection"]["northEast"]:
        comments.append("The waves are coming from the north east.")
    return comments

def get_forecast_weather_data(latitude, longitude):
    if not latitude or not longitude:
        return None
    r = requests.get("https://api.weatherapi.com/v1/forecast.json?key=e8a1873d1c8f4b44b7116035202409&q={},{}".format(latitude, longitude))
    if r.status_code != 200:
        return None
    data = r.json()
    if len(data["forecast"]["forecastday"]) == 0:
        return None
    data = data["forecast"]["forecastday"][0]
    comment = ""
    if data["day"]["avgtemp_c"] >= 20:
        comment = "It will be {} and {}.".format(data["day"]["condition"]["text"], data["day"]["avgtemp_c"])
    if data["day"]["avgtemp_c"] < 20:
        comment = "It will be {} and {}.".format(data["day"]["condition"]["text"], data["day"]["avgtemp_c"])
    return comment

def get_history_weather_data(latitude, longitude):
    if not latitude or not longitude:
        return None
    r = requests.get("https://api.weatherapi.com/v1/history.json?key=e8a1873d1c8f4b44b7116035202409&q={},{}&dt=2020-03-10".format(latitude, longitude))
    if r.status_code != 200:
        return None
    data = r.json()
    if len(data["forecast"]["forecastday"]) == 0:
        return None
    data = data["forecast"]["forecastday"][0]
    comment = ""
    if data["day"]["avgtemp_c"] >= 20:
        comment = "It was {} and {}.".format(data["day"]["condition"]["text"], data["day"]["avgtemp_c"])
    if data["day"]["avgtemp_c"] < 20:
        comment = "It was {} and {}.".format(data["day"]["condition"]["text"], data["day"]["avgtemp_c"])
    return comment

def get_weather_data(latitude, longitude):
    if not latitude or not longitude:
        return None
    r = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=56e9a0b74f0b7a26aac33f29bdb80e5f".format(latitude, longitude))
    if r.status_code != 200:
        return None
    data = r.json()
    description = data["weather"][0]["description"]
    temp_c = data["main"]["temp"] - 273.15
    comment = ""
    if description in ["thunderstorm", "drizzle", "rain", "snow"]:
        comment = "It is {} and {}.".format(description, temp_c)
    if description in ["mist", "fog"]:
        comment = "It is {} and {}.".format(description, temp_c)
    if description in ["clear", "clouds"]:
        comment = "It is {} and {}.".format(description, temp_c)
    return {"description": description, "temp": temp_c, "comment": comment}

def save_log(log_data):
    with open("../storage/log.json", "r") as f:
        try:
            data = json.loads(f.read())
            data.append(log_data)
        except:
            data = [log_data]
    with open("../storage/log.json", "w") as f:
        f.write(json.dumps(data))