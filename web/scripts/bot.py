# Using python. first import required libraries
# Using the spacy library, tokenize the sentence
# Determine a time period in the sentence and calculate it in reference to the current date, for example, if the user is searching for the 'weather'  [x periods ago], x being any number, periods being [months, years, weeks, days, etc]
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
# {"context": context, "response": resonse, data: weatherData}
# Use cleverbot if the context does not match any of the above
# Please write the code as optimal as possible
# please comment as much as possible
import datetime
import importlib
import json
import os
import random
import re
import sys
import time
import urllib
from datetime import datetime, timedelta
from urllib.request import urlopen

# import cleverbot
import geopy
import openweathermapy.core as owm
# import relativedelta
import requests
import spacy
import weatherapi
# from cleverwrap import CleverWrap
from dateutil.relativedelta import relativedelta
from geopy.geocoders import Nominatim


STORMWATCH_API_KEY = "7df7eade-63eb-11ed-a654-0242ac130002-7df7eb42-63eb-11ed-a654-0242ac130002"
WEATHER_API = "8995d3eda8f5489485251707221411"
geolocator = Nominatim(user_agent="Sally Weather Bot")

# Define the words related to time
timeWords = ["month", "months", "year", "years", "week", "weeks", "day", "days",
             "hour", "hours", "minute", "minutes", "second", "seconds", "ago", "now", "today", "tomorrow", "yesterday", "past", "future", "present"]

# Define the words related to numbers
numbersWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# Define the words related to locations
# location matches the token.tag_ NNP, NNPS
locations = []

# Define the words related to style
style = ["dress", "clothes", "recommendation", "recommended", "recommend", "recommending", "recommendations",
         "wearing", "wear", "wearable", "outfit", "outfits", "outfitting", "attire", "attiring",
         "style", "stylish", "stylishness", "stylist", "stylize", "stylized", "stylize", "stylizing",
         "styling", "fashion", "fashionable", "fashionably", "fashionize", "fashionized", "fashionize", "fashionizing",
         "fashioning", "wearable", "unwearable"]

# Define the words related to temperature
temperature = ["temp", "temperature", "hot", "cold", "warm", "freezing", "freeze", "frozen", "heat", "humid",
               "humidity", "weather", "windy", "wind", "rain", "snow", "sunny", "sunny", "sunshine", "snowfall",
               "snowing", "temperate", "thermostat", "thermal", "thermometer", "thermoregulation", "thermoregulatory",
               "thaw", "thawing", "tropical", "tropics", "troposphere", "tropospheric", "climate", "climatic", "climatically",
               "climatization", "climatize", "climatized", "climatize", "climatizing", "climatology", "meteorological", "meteorologically",
               "meteorologist", "meteorology", "meteorological", "meteorologically"]

# Define the user's IP address
user_ip = "127.0.0.1"

# Define the user's text
text = "What is the weather like in Johannesburg"


class NLP:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, text):
        return self.nlp(text)

    def get_entities(self, text):
        entities = []
        doc = self.parse(text)
        for token in doc:
            if token.ent_type_ != "":
                entities.append(token.text)
        return entities

    def get_dates(self, entities):
        dates = []
        for i in entities:
            if i.lower() in timeWords:
                dates.append(i)
        return dates

    def get_numbers(self, entities):
        numbers = []
        for i in entities:
            if i.lower() in numbersWords:
                numbers.append(i)
        return numbers

    def get_context(self, entities):
        context = ""
        for i in entities:
            if i.lower() in style:
                context += "style" + " "
            if i.lower() in temperature:
                context += "temperature" + " "
            if i.lower() in locations:
                context += "location" + " "
        return context


def get_current_weather(lat, lng):
    # Get the current weather
    current_weather = owm.get_current(
        lat=lat,
        lon=lng,
        units="metric"
    )
    return current_weather


def get_forecast(lat, lng):
    # Get the forecast
    forecast = owm.get_forecast(
        lat=lat,
        lon=lng,
        units="metric"
    )
    return forecast


def get_history(lat, lng, date):
    # Get history weather
    weather_history = weatherapi.Weather(API_key=WEATHER_API)

    # Get the weather in a specific day
    history = weather_history.history(
        lat=lat,
        lon=lng,
        start=date,
        end=date
    )
    return history


def get_recommendation(current_weather, date):
    # Get the temp and description
    temp = current_weather["temp"]
    description = current_weather["weather"][0]["description"]

    # Get a recommendation
    recommendation = ""
    if "rain" in description:
        recommendation = "Wear a raincoat"
    elif "snow" in description:
        if temp > 5:
            recommendation = "Wear a snowcoat"
        else:
            recommendation = "Wear a heavy coat"
    elif "thunderstorm" in description:
        recommendation = "Wear a windbreaker"
    elif "drizzle" in description:
        recommendation = "Wear a raincoat"
    elif "clear" in description:
        if temp > 30:
            recommendation = "Wear light clothes"
        elif temp < 0:
            recommendation = "Wear a heavy coat"
        else:
            recommendation = "Wear a jacket"
    elif temp < 0:
        recommendation = "Wear a heavy coat"
    else:
        recommendation = "Wear a jacket"

    # If it's the night
    if date["hour"] < 8 or date["hour"] > 19:
        recommendation += " and a hat"

    return recommendation


def get_weather_data(lat, lng, date, context, entities):
    weather_data = {}

    # If the user wants to know the current weather
    if "temperature" in context and "present" in entities:
        current_weather = get_current_weather(lat, lng)

        # Get the data
        weather_data["temp"] = current_weather["temp"]
        weather_data["temp_max"] = current_weather["temp_max"]
        weather_data["temp_min"] = current_weather["temp_min"]
        weather_data["humidity"] = current_weather["humidity"]
        weather_data["wind_speed"] = current_weather["wind_speed"]
        weather_data["wind_degree"] = current_weather["wind_deg"]
        weather_data["description"] = current_weather["weather"][0]["description"]
        weather_data["icon"] = current_weather["weather"][0]["icon"]
        weather_data["city"] = current_weather["name"]

        # Get the recommendation
        recommendation = get_recommendation(current_weather, date)
        return [recommendation, weather_data]

    # If the user wants to know the forecast
    elif "temperature" in context and "future" in entities:
        weather_data = {}
        forecast = get_forecast(lat, lng)
        weather_data["forecast"] = forecast

        return [None, weather_data]

    # If the user wants to know the history weather
    elif "temperature" in context and "past" in entities:
        history = get_history(lat, lng, date)

        # Get the data
        weather_data["temp"] = history["Temperature"]["Maximum"]
        weather_data["temp_max"] = history["Temperature"]["Maximum"]
        weather_data["temp_min"] = history["Temperature"]["Minimum"]
        weather_data["humidity"] = history["Relative Humidity"]["Maximum"]
        weather_data["wind_speed"] = history["Wind"]["Maximum Speed"]
        weather_data["wind_direction"] = history["Wind"]["Maximum Speed Direction"]
        weather_data["description"] = history["Weather"][0]["Condition"]
        weather_data["city"] = history["City"]

        return [None, weather_data]

    # If the user wants to know the recommendation
    elif "style" in context and "present" in entities:
        current_weather = get_current_weather(lat, lng)

        # Get the recommendation
        recommendation = get_recommendation(current_weather, date)
        return [recommendation, weather_data]

    else:
        return ["We could not understand your question", weather_data]


def get_location(user_ip, entities):
    # Get the user's location
    lat = None
    lng = None
    user_location = None
    try:
        # Open the location file
        with open("../storage/location.json") as file:
            data = json.load(file)

        # If the user's IP is in the file
        if user_ip in data:
            user_location = data[user_ip]["location"]
            lat = data[user_ip]["lat"]
            lng = data[user_ip]["lng"]

        # If the user wants to know the history weather
        if len(entities) > 0 and entities[0].lower() in locations:
            user_location = entities[0]
            location = geolocator.geocode(user_location)

            # Get the latitude and longitude of the location
            lat = location.latitude
            lng = location.longitude

            # Save the information in the file
            data[user_ip] = {"location": user_location, "lat": lat, "lng": lng}
            with open("../storage/location.json", "w") as file:
                json.dump(data, file)

    except Exception as e:
        print(e)

    return [lat, lng, user_location]


def get_time(entities, numbers):
    # Get the current date
    current_date = datetime.now()

    # If the user wants to know the weather in the past
    if "past" in entities:
        if "month" in entities:
            current_date = current_date - relativedelta(months=int(numbers[0]))
        elif "year" in entities:
            current_date = current_date - relativedelta(years=int(numbers[0]))
        elif "week" in entities:
            current_date = current_date - relativedelta(weeks=int(numbers[0]))
        elif "day" in entities:
            current_date = current_date - relativedelta(days=int(numbers[0]))
        else:
            current_date = current_date - relativedelta(days=int(numbers[0]))

    # If the user wants to know the weather in the future
    elif "future" in entities:
        if "month" in entities:
            current_date = current_date + relativedelta(months=int(numbers[0]))
        elif "year" in entities:
            current_date = current_date + relativedelta(years=int(numbers[0]))
        elif "week" in entities:
            current_date = current_date + relativedelta(weeks=int(numbers[0]))
        elif "day" in entities:
            current_date = current_date + relativedelta(days=int(numbers[0]))
        else:
            current_date = current_date + relativedelta(days=int(numbers[0]))

    # If the user wants to know the weather in the past
    elif "present" in entities:
        current_date = current_date

    else:
        current_date = current_date

    # Get the date
    date = {"year": current_date.year, "month": current_date.month,
            "day": current_date.day, "hour": current_date.hour,
            "minute": current_date.minute, "second": current_date.second}

    return date


def get_stormwatch(lat, lng):
    # Get the stormwatch information
    weather_data = {}
    stormwatch_url = "https://api.stormglass.io/v2/weather/point?"
    stormwatch_url += "lat=" + str(lat) + "&lng=" + str(lng) + "&params=waveDirection"
    stormwatch_data = requests.get(stormwatch_url, headers={"Authorization": STORMWATCH_API_KEY})

    # Get the data
    weather_data["wave_direction"] = stormwatch_data.json()["hours"][0]["waveDirection"]["noWaveDirection"]["value"]

    return weather_data


def get_response(text, user_ip):
    # Initialize NLP
    nlp = NLP()

    # Get the user's entities
    entities = nlp.get_entities(text)
    entities = [i.lower() for i in entities]

    # Get the time information
    time_entities = nlp.get_dates(entities)
    numbers = nlp.get_numbers(entities)
    date = get_time(time_entities, numbers)

    # Get the location information
    lat, lng, user_location = get_location(user_ip, entities)

    # Get the context
    context = nlp.get_context(entities)

    # Get the weather data
    if "temperature" in context:
        res, weather_data = get_weather_data(lat, lng, date, context, entities)
    else:
        res, weather_data = ["We could not understand your question", {}]

    # Get the stormwatch information
    if "stormwatch" in context:
        weather_data["stormwatch"] = get_stormwatch(lat, lng)

    # Get the response
    response = {"context": context, "response": res, "data": weather_data}

    return response


def main(text, user_ip):
    get_response(text, user_ip)