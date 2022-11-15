from flask import Flask, request, render_template, url_for, jsonify
import spacy
# from ../SallyPython import location
from scripts import history, dressSense, weather
import socket
import re
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import cleverbotfreeapi
import requests
import json
import os
import urllib.request as req
from geotext import GeoText

# cb = cleverbot.Cleverbot('CCC1afw_sCnym21L6wpLuWBLDbA')
msgHistory = []
cb = cleverbotfreeapi

current_context = ""

appnlp = spacy.load("en_core_web_sm")
sp = spacy.load("en_core_web_sm")

location_file = './storage/location.json'
ip = ""
with (open("./config.json")) as jsonFile:
    config = json.load(jsonFile)
    # print(config)
openWeatherMapApiKey = config['API_KEY']
openWeatherMapEndPoint = config['OpenWeatherMapEndpoint']
cbsession = ""

app = Flask(__name__)
app.config.from_object('config')

chatHistory = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# receive and send responses to the chat
@app.route('/chat', methods=['GET','POST'])
def chat_post():
    if request.method == 'POST':
        message = request.form['message']
        ip = socket.gethostbyname(socket.gethostname())
        response = process_response(request)
        return response

def process_response(text):
    print("Processing response")
    """
    response: "The bot message",
    command: "history",
    data: [list of data]
    """
    # result = {'response': "What can I help you with?"}
    # result = {'response': text}
    # bot = weatherbot.main(socket.gethostbyname(socket.gethostname()), text.form['message'])
    # bot = history.History().reply()
    # sbot = bot.main(text.form['message'], socket.gethostbyname(socket.gethostname()))
    # bot = bot2.main(text.form['message'])
    result = ""
    current_context = get_context(text.form['message'])[0]
    cbsession = "Sally_"+find_location_by_ip()["location"]
    print(get_context)
    print(getSentenceTense)
    if current_context == "" or current_context is None:
        # result = cb.say(text)
        msgHistory.append(text.form['message'])
        result = cb.cleverbot(text.form['message'], msgHistory, cbsession)
        result = {'response': result, 'context': current_context}
    else:
        contexts = get_context(text.form["message"])
        print(contexts)
        # location = findhas_country(text.form["message"])
        location = find_location_by_ip()
        # print(location)
        if len(contexts) > 0:
            for context in contexts:
                if context == "dressSense":
                    weatherData = getWeather()
                    descs = weatherData["weather"][0]["main"]
                    rec = dressSense()
                    return {"response": rec, "context": context, "data": weatherData}
                elif context == "weather":
                    # result = history.History(text = text.form['message'], tense=getSentenceTense(text.form['message']), location=location).reply()
                    result = {'response': weather.get_weather(), "context": context}
                elif context == "stormwatch":
                    result = {"response": "UNable to load stormwatch data", "context": context}
                elif context == "location":
                    result = {"response": "Your location has been changed", "context": context, "data": find_location_by_ip()}
                elif context == "future":
                    result = history.History(text = text.form['message'], tense=getSentenceTense(text.form['message']), location=location).reply()
                elif context == "history":
                    result = history.History(text = text.form['message'], tense=getSentenceTense(text.form['message']), location=location).reply()
                elif context == "conversation":
                    msgHistory.append(text)
                    result = cb.cleverbot(text.form['message'], msgHistory, cbsession)
                    result = {'response': result, 'context': current_context}
    print(result)
    return jsonify(result)

def has_country(text):
    """
    Check if the text contains a country code
    :param text:
    :return:
    """
    locations = []
    tokens = appnlp(text)
    for token in tokens:
        if token.tag_ == "NNP":
            locations.append(token.text)
    places = GeoText(text)
    for city in places.cities:
        locations.append(city)
                    # for country in locations.country_mentions:`````````````````````````````````````````````````
                    #     locations.append(country.values())`````````````````````````````````````````````````
    return locations

def get_context(text):
    """returns context from text"""
    tokens = appnlp(text)
    valid_contexts = {
        "dressSense" : ["recommend", "dress", "clothes", "wear", "put on"],
        "weather" : ["weather", "cold", "chill", "warm", "cool", "temperature", "humidity", "breeze", "wind"],
        "stormwatch" : ["stormwatch", "storm", "thunder", "snowfall", "snow", "typhoon", "alerts"],
        "location" : ["moving", "going to", "living", "live", "flying", "driving", "moved"]
    }
    rcontext = []
    if getSentenceTense(text) == "past":
        rcontext.append("history")
    elif getSentenceTense(text) == "future":
        rcontext.append("future")
    else:
        for token in tokens:
            for context in valid_contexts:
                if token.tag_ in valid_contexts[context]:
                    rcontext.append(context)
                    break
                else:
                    rcontext.append("conversation")
    rcontext = list(dict.fromkeys(rcontext))
    return rcontext

def getSentenceTense(sentence):
    sentenceTense = "present"
    sentence = appnlp(sentence)
    for token in sentence:
        if token.tag_ == "VBD" or token.tag_ == "VBN" or token.tag_ == "VBP":
            sentenceTense = "past"
            print(token.text)
        # if token.tag_ == "VBG" or token.tag_ == "VBZ":
        if token.tag_ == "VBZ":
            sentenceTense = "future"
            print(token.text)
    return sentenceTense

def save_location(loc, lat, lon):
    loc = location_file
    if not os.path.isfile(loc):
        data = {"locations": []}
    else:
        with open(loc) as jsonFile:
            data = json.load(jsonFile)
            userLocationData = [locationData for locationData in data["locations"] if locationData["ip"] == ip]
            if len(userLocationData) > 0:
                userLocationData[0]["location"] = loc
                userLocationData[0]["lat"] = lat
                userLocationData[0]["lng"] = lon
                return
    data["locations"].append({"ip": ip, "location": loc, "lat": lat, "lng": lon})
    with open(loc, "w") as jsonFile:
        json.dump(data, jsonFile)

def get_location():
    userLocationFile = location_file
    if not os.path.isfile(userLocationFile):
        return None
    with open(userLocationFile) as jsonFile:
        userLocationData = json.load(jsonFile)
        userLocation = [location for location in userLocationData["locations"] if location["ip"] == ip]
        if len(userLocation) > 0:
            return userLocation[0]
        return None

def new_location():
    if get_location() is None:
        newLoc = find_location_by_ip()
        save_location(loc = newLoc['location'], lat=newLoc['lat'], lon=newLoc['lon'])
        return newLoc

def find_location_by_ip():
    with req.urlopen("https://geolocation-db.com/json/"+ip) as locdata:
        data = json.loads(locdata.read().decode())
        # print(data)
        lat = data["latitude"]
        long = data["longitude"]
        location = data["city"] + ", " + data["state"] + ", " + data["country_name"]
        res = {"ip": ip, "lat": lat, "lng": long, "location": location}
        # print(res)
        return res

def getWeather():
    userIp = ip
    myloc = new_location() if get_location() is None else get_location()
    openWeatherMapParams = {
        "lat": myloc["latitude"],
        "lon": myloc["longitude"],
        "appid": openWeatherMapApiKey,
        "units": "metric" if "usa" in myloc["location"].lower() else "imperial"
    }
    response = requests.get(openWeatherMapEndPoint, params=openWeatherMapParams)
    print(response.json())
    return response.json()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

with app.test_request_context():
    print(url_for('index'))
    print(url_for('chat'))
    print(url_for('about'))
    print(url_for('credits'))

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(debug=True)