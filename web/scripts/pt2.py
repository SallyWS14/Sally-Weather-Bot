# Using the nltk library,
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
# If the user requests a clothing advice, return a message based on the data and context
# if the user requests stormwatch information, return the stormwatch information
# if the user requests weather information, return the weather information
# otherwise, return a message based on the context data
import json
import os
import stat
import sys

import requests

# Permission to use
per = 0o600
 
# type of node to be created
node_type = stat.S_IRUSR
mode = per | node_type

def get_message(sentence, user_ip):
    """
    Get the message from the sentence.
    """

    print(user_ip)
    context = get_context(sentence)
    messageOrRecommendation = ""
    weatherData = {}

    if "dressSense" in context:
        messageOrRecommendation = get_dress_recommendation(sentence, context)
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    if "weather" in context:
        weatherData = get_weather_data(sentence, context, user_ip)
        messageOrRecommendation = get_weather_message(sentence, context, weatherData)
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    if "location" in context:
        user_ip = user_ip.split(',')[0]
        lat, lng = get_lat_long(user_ip)
        messageOrRecommendation = update_location(user_ip, lat, lng, context["location"])
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    if "history" in context:
        messageOrRecommendation = get_history_message(sentence, context, weatherData)
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    if "stormwatch" in context:
        messageOrRecommendation = get_stormwatch_message(sentence, context, weatherData)
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    if "forecast" in context:
        messageOrRecommendation = get_forecast_message(sentence, context, weatherData)
        return {"context": context, "response": messageOrRecommendation, "data": weatherData}

    return {"context": context, "response": messageOrRecommendation, "data": weatherData}


def get_context(sentence):
    """
    Get the context from the sentence.
    """
    context = []
    if "location" in sentence[1]:
        context.append("location")
    if "history" in sentence[1]:
        context.append("history")
    if "clothes" in sentence[1] or "dress" in sentence[1] or "recommend" in sentence[1]:
        context.append("dressSense")
    if "stormwatch" in sentence[1]:
        context.append("stormwatch")
    if "forecast" in sentence[1]:
        context.append("forecast")
    if "weather" in sentence[1]:
        context.append("weather")
    return context


def get_dress_recommendation(sentence, context):
    """
    Get the dress recommendation from the sentence.
    """
    if "rain" in sentence[1] or "snow" in sentence[1]:
        return "The weather is " + sentence[1][0] + " and the temperature is " + sentence[1][1] + ". You should dress warmly."

    if "cloudy" in sentence[1]:
        return "The weather is " + sentence[1][0] + " and the temperature is " + sentence[1][1] + ". You should dress casually."

    return "The weather is " + sentence[1][0] + " and the temperature is " + sentence[1][1] + ". You should dress formally."


def get_weather_data(sentence, context, user_ip):
    """
    Get the weather data from the sentence.
    """
    user_location = get_user_location(user_ip)
    if user_location == "":
        return {}
    if "history" in context:
        weatherData = get_history(user_location, sentence[0])
    elif "forecast" in context:
        weatherData = get_forecast(user_location, sentence[0])
    else:
        weatherData = get_current_weather(user_location, sentence[0])
    return weatherData


def get_current_weather(user_location, sentence):
    """
    Get the current weather information.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    units = "metric"
    locality = user_location[0]
    country = user_location[1]
    appid = os.environ.get('OPEN_WEATHER_API_KEY')
    payload = {"q": locality + "," + country, "units": units, "appid": appid, "lang": "en"}
    response = requests.get(url, params=payload)
    data = response.json()
    weatherData = {"temperature": data["main"]["temp"], "feelsLike": data["main"]["feels_like"], "humidity": data["main"]["humidity"], "condition": data["weather"][0]["description"], "windSpeed": data["wind"]["speed"]}
    return weatherData


def get_history(user_location, sentence):
    """
    Get the weather history information.
    """
    url = "https://api.weatherapi.com/v1/history.json"
    startDate = sentence[0]
    endDate = sentence[0]
    locality = user_location[0]
    country = user_location[1]
    units = "metric"
    appid = os.environ.get('WEATHER_API_KEY')
    payload = {"key": appid, "q": locality + "," + country, "dt": startDate, "end_dt": endDate, "lang": "en", "format": "json", "tp": "24", "units": units}
    response = requests.get(url, params=payload)
    data = response.json()
    dailyData = data["forecast"]["forecastday"][0]
    weatherData = {"temperature": dailyData["day"]["avgtemp_c"], "feelsLike": dailyData["day"]["feelslike_c"], "humidity": dailyData["day"]["avghumidity"], "condition": dailyData["day"]["condition"]["text"], "windSpeed": dailyData["day"]["maxwind_kph"]}
    return weatherData


def get_forecast(user_location, sentence):
    """
    Get the weather forecast information.
    """
    url = "https://api.weatherapi.com/v1/forecast.json"
    startDate = sentence[0]
    locality = user_location[0]
    country = user_location[1]
    units = "metric"
    appid = os.environ.get('WEATHER_API_KEY')
    payload = {"key": appid, "q": locality + "," + country, "dt": startDate, "lang": "en", "format": "json", "tp": "24", "units": units}
    response = requests.get(url, params=payload)
    data = response.json()
    dailyData = data["forecast"]["forecastday"][0]
    weatherData = {"temperature": dailyData["day"]["avgtemp_c"], "feelsLike": dailyData["day"]["feelslike_c"], "humidity": dailyData["day"]["avghumidity"], "condition": dailyData["day"]["condition"]["text"], "windSpeed": dailyData["day"]["maxwind_kph"]}
    return weatherData


def get_user_location(user_ip):
    """
    Get the user's location.
    """
    if user_ip == "":
        return ["", ""]
    user_ip = user_ip.split(',')[0]
    url = "http://ip-api.com/json/" + user_ip
    response = requests.get(url)
    data = response.json()
    if data["status"] != "success":
        return ["", ""]
    return [data["city"], data["country"]]


def get_lat_long(user_ip):
    """
    Get the latitude and longitude from the user's ip.
    """
    if user_ip == "":
        return ""
    user_ip = user_ip.split(',')[0]
    url = "http://ip-api.com/json/" + user_ip
    response = requests.get(url)
    data = response.json()
    if data["status"] != "success":
        return ""
    return [data["lat"], data["lon"]]


def get_weather_message(sentence, context, weatherData):
    """
    Get the weather message from the sentence.
    """
    if "history" in context:
        return "The weather in " + sentence[1][0] + " " + sentence[1][1] + " was " + weatherData["temperature"] + "°C. The condition was " + weatherData["condition"] + "."

    if "forecast" in context:
        return "The weather in " + sentence[1][0] + " " + sentence[1][1] + " will be " + weatherData["temperature"] + "°C. The condition will be " + weatherData["condition"] + "."

    return "The weather in " + sentence[1][0] + " " + sentence[1][1] + " is " + weatherData["temperature"] + "°C. The condition is " + weatherData["condition"] + "."


def get_history_message(sentence, context, weatherData):
    """
    Get the weather history message from the sentence.
    """
    return "The weather in " + sentence[1][0] + " " + sentence[1][1] + " was " + weatherData["temperature"] + "°C. The condition was " + weatherData["condition"] + "."


def get_stormwatch_message(sentence, context, weatherData):
    """
    Get the stormwatch message from the sentence.
    """
    return "There isn't any stormwatch information for " + sentence[1][0] + " " + sentence[1][1] + "."


def get_forecast_message(sentence, context, weatherData):
    """
    Get the forecast message from the sentence.
    """
    return "The weather in " + sentence[1][0] + " " + sentence[1][1] + " will be " + weatherData["temperature"] + "°C. The condition will be " + weatherData["condition"] + "."


def update_location(user_ip, lat, lng, location):
    """
    Update the user's location.
    """
    if user_ip == "":
        return "Could not get your location."

    user_ip = user_ip.split(',')[0]
    lat, lng = get_lat_long(user_ip)
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    key = os.environ.get('GOOGLE_API_KEY')
    payload = {"address": location, "key": key}

    response = requests.get(url, params=payload)
    data = response.json()
    if data["status"] != "OK":
        return "Could not find the location specified."

    if "results" not in data or len(data["results"]) == 0:
        return "Could not find the location specified."

    results = data["results"][0]
    formattedAddress = results["formatted_address"]
    geometry = results["geometry"]
    geometryLocation = geometry["location"]
    lat = geometryLocation["lat"]
    lng = geometryLocation["lng"]
    update_location_file(user_ip, formattedAddress, lat, lng)
    return "Your current location is " + formattedAddress + "."


def update_location_file(ip, location, lat, lng):
    """
    Update the location.json file with the new location.
    """
    data = read_location_file()
    if data == "":
        data = {}
    user = data.get(ip, {})
    user["ip"] = ip
    user["location"] = location
    user["lat"] = lat
    user["lng"] = lng
    data[ip] = user
    write_location_file(data)


def read_location_file():
    """
    Read the location.json file.
    """
    file = "../storage/location.json"
    if not os.path.exists(file):
        return ""
    with open(file, "r") as f:
        data = f.read()
        if data == "":
            return ""
        return json.loads(data)


def write_location_file(data):
    """
    Write the location.json file.
    """
    file = "../storage/location.json"
    # if not os.path.exists(file):
    #     os.mknod(file, mode)
    with open(file, "w") as f:
        f.write(json.dumps(data))