# Using python. first import required libraries
# Using the spacy library, tokenize the sentence
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
# Please write the code as optimal as possible
# please comment as much as possible
# please use the library

# First import required libraries

import json
import logging
import os
import re
from datetime import datetime

import requests
import spacy

# Setting up the logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

with (open("./config.json")) as jsonFile:
    config = json.load(jsonFile)
    # print(config)

# Defining the global variables
nlp = spacy.load("en_core_web_sm")
openWeatherMapApiKey = config['API_KEY']
openWeatherMapEndPoint = config['OpenWeatherMapEndpoint']
weatherApiKey = config['weatherapikey']
weatherApiEndPoint = config['WeatherApiEndpoint']
stormWatchEndPoint = config['StormWatchEndpoint']
defaultLocation = config['default_loc']

# Defining the userLocation function
def userLocation(userIp):
    userLocationFile = "./storage/location.json"
    if not os.path.isfile(userLocationFile):
        return None
    with open(userLocationFile) as jsonFile:
        userLocationData = json.load(jsonFile)
        userLocation = [location for location in userLocationData["locations"] if location["ip"] == userIp]
        if len(userLocation) > 0:
            return userLocation[0]
        return None

# Defining the saveUserLocation function
def saveUserLocation(userIp, location, latitude, longitude):
    userLocationFile = "./storage/location.json"
    if not os.path.isfile(userLocationFile):
        data = {"locations": []}
    else:
        with open(userLocationFile) as jsonFile:
            data = json.load(jsonFile)
            userLocationData = [locationData for locationData in data["locations"] if locationData["ip"] == userIp]
            if len(userLocationData) > 0:
                userLocationData[0]["location"] = location
                userLocationData[0]["lat"] = latitude
                userLocationData[0]["lng"] = longitude
                return
    data["locations"].append({"ip": userIp, "location": location, "lat": latitude, "lng": longitude})
    with open(userLocationFile, "w") as jsonFile:
        json.dump(data, jsonFile)

# Defining the getLocation function
def getLocation(userIp):
    userLocationData = userLocation(userIp)
    if userLocationData:
        return userLocationData["location"]
    return defaultLocation

# Defining the getLatitude function
def getLatitude(userIp):
    userLocationData = userLocation(userIp)
    if userLocationData:
        return userLocationData["lat"]
    return "37.0839"

# Defining the getLongitude function
def getLongitude(userIp):
    userLocationData = userLocation(userIp)
    if userLocationData:
        return userLocationData["lng"]
    return "-122.0891"

# Defining the getWeather function
def getWeather(userIp):
    userLocationData = userLocation(userIp)
    openWeatherMapParams = {
        "lat": getLatitude(userIp),
        "lon": getLongitude(userIp),
        "appid": openWeatherMapApiKey,
        "units": "imperial"
    }
    response = requests.get(openWeatherMapEndPoint, params=openWeatherMapParams)
    print(response.json())
    return response.json()

# Defining the getWeatherForecast function
def getWeatherForecast(userIp):
    weatherParams = {
        "key": weatherApiKey,
        "q": getLocation(userIp),
        "format": "json",
        "num_of_days": 10,
        "tp": 24,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = requests.get(weatherApiEndPoint, params=weatherParams)
    print(response.json())
    return response.json()

# Defining the getStormWatch function
def getStormWatch(userIp):
    stormWatchParams = {
        "lat": getLatitude(userIp),
        "lon": getLongitude(userIp),
        "format": "json"
    }
    response = requests.get(stormWatchEndPoint, params=stormWatchParams)
    return response.json()

# Defining the getWeatherHistory function
def getWeatherHistory(userIp):
    weatherParams = {
        "key": weatherApiKey,
        "q": getLocation(userIp),
        "format": "json",
        "num_of_days": 5,
        "date": "2020-05-15"
    }
    response = requests.get(weatherApiEndPoint, params=weatherParams)
    return response.json()

# Defining the getSentenceContext function
def getSentenceContext(sentence):
    sentenceContext = set([])
    if "clothes" in sentence or "recommend" in sentence:
        sentenceContext.add("dressSense")
    if "weather" in sentence:
        sentenceContext.add("weather")
    if "location" in sentence:
        sentenceContext.add("location")
    if "history" in sentence:
        sentenceContext.add("history")
    if "stormwatch" in sentence:
        sentenceContext.add("stormwatch")
    return sentenceContext

# Defining the getSentenceTense function
def getSentenceTense(sentence):
    sentenceTense = "present"
    sentence = nlp(sentence)
    
    for token in sentence:
        if token.tag_ == "VBD" or token.tag_ == "VBN" or token.tag_ == "VBP":
            sentenceTense = "past"
        if token.tag_ == "VBG" or token.tag_ == "VBZ":
            sentenceTense = "future"
    return sentenceTense

# Defining the getWeatherRecommendation function
def getWeatherRecommendation(weatherData):
    weatherRecommendation = {
        "sunny": "Wear sunglasses, sunscreen, hat and light t-shirt",
        "fog": "Wear sunglasses, sunscreen and dress in layers",
        "haze": "Wear sunglasses, sunscreen and dress in layers",
        "smoke": "Wear sunglasses, sunscreen and dress in layers",
        "clouds": "Wear sunglasses, sunscreen and dress in layers",
        "rain": "Bring an umbrella and wear waterproof shoes",
        "drizzle": "Bring an umbrella and wear waterproof shoes",
        "thunderstorm": "Bring an umbrella and wear waterproof shoes",
        "snow": "Bring a jacket and wear warm clothes",
        "mist": "Wear sunglasses, sunscreen and dress in layers"
    }
    return weatherRecommendation[weatherData["weather"][0]["main"].lower()]

# Defining the getWeatherMessage function
def getWeatherMessage(weatherData, weatherHistoryData):
    weatherMessage = {
        "sunny": "The weather is " + weatherData["weather"][0]["main"],
        "fog": "The weather is " + weatherData["weather"][0]["main"],
        "haze": "The weather is " + weatherData["weather"][0]["main"],
        "smoke": "The weather is " + weatherData["weather"][0]["main"],
        "clouds": "The weather is " + weatherData["weather"][0]["main"],
        "clear": "The weather is " + weatherData["weather"][0]["main"],
        "rain": "The weather is " + weatherData["weather"][0]["main"],
        "drizzle": "The weather is " + weatherData["weather"][0]["main"],
        "thunderstorm": "The weather is " + weatherData["weather"][0]["main"],
        "snow": "The weather is " + weatherData["weather"][0]["main"],
        "mist": "The weather is " + weatherData["weather"][0]["main"],
        "history": "The weather was " + weatherHistoryData["weather"][0]["main"]
    }
    return weatherMessage[weatherData["weather"][0]["main"].lower()]

# Defining the getForecastWeatherMessage function
def getForecastWeatherMessage(weatherData, weatherForecastData):
    weatherMessage = {
        "sunny": "The weather is " + weatherData["weather"][0]["main"],
        "fog": "The weather is " + weatherData["weather"][0]["main"],
        "haze": "The weather is " + weatherData["weather"][0]["main"],
        "smoke": "The weather is " + weatherData["weather"][0]["main"],
        "clouds": "The weather is " + weatherData["weather"][0]["main"],
        "clear": "The weather is " + weatherData["weather"][0]["main"],
        "rain": "The weather is " + weatherData["weather"][0]["main"],
        "drizzle": "The weather is " + weatherData["weather"][0]["main"],
        "thunderstorm": "The weather is " + weatherData["weather"][0]["main"],
        "snow": "The weather is " + weatherData["weather"][0]["main"],
        "mist": "The weather is " + weatherData["weather"][0]["main"],
        "forecast": "The weather is " + weatherForecastData["data"][0]["weather"][0]["main"]
    }
    return weatherMessage[weatherData["weather"][0]["main"].lower()]

# Defining the getLocationFromSentence function
def getLocationFromSentence(sentence):
    tokenizedSentence = nlp(sentence)
    for token in tokenizedSentence:
        if token.ent_type_ == "GPE":
            return token.text
    return None

# Defining the getLocationCoordinates function
def getLocationCoordinates(location):
    openWeatherMapParams = {
        "q": location,
        "appid": openWeatherMapApiKey
    }
    response = requests.get(openWeatherMapEndPoint, params=openWeatherMapParams)
    data = response.json()
    return data["coord"]["lat"], data["coord"]["lon"]

# Defining the getWeatherData function
def getWeatherData(userIp, sentence, sentenceContext, sentenceTense):
    # Getting the weather data
    weatherData = getWeather(userIp)

    # Check if the sentence has a dress sense context
    if "dressSense" in sentenceContext:
        return {"context": "dressSense", "response": getWeatherRecommendation(weatherData), "data": weatherData}
    
    # Check if the sentence has a weather context
    if "weather" in sentenceContext:
        # Check if the sentence has a history context
        if "history" in sentenceContext:
            weatherHistoryData = getWeatherHistory(userIp)
            return {"context": "history", "response": getWeatherMessage(weatherData, weatherHistoryData), "data": weatherHistoryData}
        else:
            # Check if the sentence has a forecast context
            if sentenceTense == "future":
                weatherForecastData = getWeatherForecast(userIp)
                return {"context": "forecast", "response": getForecastWeatherMessage(weatherData, weatherForecastData), "data": weatherForecastData}
            else:
                return {"context": "weather", "response": getWeatherMessage(weatherData, weatherData), "data": weatherData}

    # Check if the sentence has a stormwatch context
    if "stormwatch" in sentenceContext:
        stormWatchData = getStormWatch(userIp)
        return {"context": "stormwatch", "response": "No warnings.", "data": stormWatchData}
    
    # Check if the sentence has a location context
    if "location" in sentenceContext:
        # Get the location name from the sentence
        location = getLocationFromSentence(sentence)

        # Get the latitude and longitude for the location
        latitude, longitude = getLocationCoordinates(location)

        # Save the user's location
        saveUserLocation(userIp, location, latitude, longitude)

        # Get the weather data for the new location
        weatherData = getWeather(userIp)

        return {"context": "location", "response": "", "data": {"location": location, "lat": latitude, "lng": longitude}}

# Defining the getWeatherData function
def getWeatherDataAsMessage(userIp, sentence, sentenceContext, sentenceTense):
    weatherData = getWeatherData(userIp, sentence, sentenceContext, sentenceTense)
    return weatherData["response"]

# Defining the main function
def main(userIp, sentence):
    # userIp = "117.199.61.165"
    # sentence = "What should i wear?"
    sentenceContext = getSentenceContext(sentence)
    sentenceTense = getSentenceTense(sentence)

    weatherData = getWeatherData(userIp, sentence, sentenceContext, sentenceTense)
    logging.info(json.dumps(weatherData))
    return weatherData

# # Calling the main function
# if __name__ == "__main__":
#     main()