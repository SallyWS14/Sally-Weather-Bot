from flask import Flask, request, render_template, url_for, jsonify
import googlemaps
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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from geotext import GeoText
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")

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
# Define the words related to time
timeWords = ["month", "months", "year", "years", "week", "weeks", "day", "days",
             "hour", "hours", "minute", "minutes", "second", "seconds", "ago", "now", "today", "tomorrow", "yesterday", "past", "future", "present"]

numbersWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
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
    print(request)
    print(request.form)
    # print(request.form['userInput'])
    if request.method == 'POST':
        message = request.form['message']
        ip = socket.gethostbyname(socket.gethostname())
        print(ip)
        response = process_response(request)
        print(response)
        return response
    # else :
    #     return render_template('chat.html')

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
    msg = text.form['message']
    current_context = get_context(msg)
    cbsession = "Sally_"+find_location_by_ip()["location"]
    print(cbsession)
    print(get_context)
    print(getSentenceTense)
    contexts = get_context(text.form["message"])
    print(contexts)
    mode = getmode(text.form["message"])
    # location = findhas_country(text.form["message"])
    location = find_location_by_ip()
    # print(location)
    if len(contexts) > 0:
        for context in contexts:
            if context == "dressSense":
                weatherData = weather.get_weather(location['lat'], location['lng'])
                # descs = weatherData["weather"][0]["main"]
                rec = dressSense.getDressSense()
                result = {"response": rec, "context": context, "data": weatherData}
            elif context == "history":
                result = history.History(text = msg, tense=getSentenceTense(msg), location=location).reply()
            elif context == "weather":
                # result = history.History(text = msg, tense=getSentenceTense(msg), location=location).reply()
                result = {'response': weather.get_weather(location['lat'], location['lng']), "context": context}
            elif context == "stormwatch":
                # result = {"response": "UNable to load stormwatch data", "context": context}
                result = {'response': get_stormwatch(location['latitude'], location['longitude']), "context": context}
            elif context == "location":
                # result = {"response": "Your location has been changed", "context": context, "data": find_location_by_ip()}
                result = locationResponse(msg)
                result = {'response': result[0], "context": context, "data": {"link": result[1]}}
            elif context == "future":
                result = history.History(text = msg, tense=getSentenceTense(msg), location=location).reply()
            else:
                msgHistory.append(text)
                result = cb.cleverbot(msg, session=cbsession)
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
    if getSentenceTense(text) == "future":
        rcontext.append("future")
    for token in tokens:
        for context in valid_contexts:
            if token.text in valid_contexts[context]:
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
        if token.tag_ == "VBG" or token.tag_ == "VBZ":
        # if token.tag_ == "VBZ":
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
    with req.urlopen("https://geolocation-db.com/json/?ip="+ip) as locdata:
        print(locdata)
        data = json.loads(locdata.read().decode())
        print(data)
        # print(data)
        lat = data["latitude"]
        long = data["longitude"]
        # check if city state and country_name are not None
        location = ""
        if data["city"] is not None and data["state"] is not None and data["country_name"] is not None:
            location = data["city"] + ", " + data["state"] + ", " + data["country_name"]
        elif data["city"] is not None and data["country_name"] is not None:
            location = data["city"] + ", " + data["country_name"]
        elif data["state"] is not None and data["country_name"] is not None:
            location = data["state"] + ", " + data["country_name"]
        elif data["country_name"] is not None:
            location = data["country_name"]
        else:
            location = "Earth"
        res = {"ip": ip, "lat": lat, "lng": long, "location": location}
        # print(res)
        return res

def get_dates(message):
    dates = []
    entities = []
    for token in appnlp(message):
        if token.ent_type_ != "":
            entities.append(token.text)

    for i in entities:
        if i.lower() in timeWords:
            dates.append(i)
    return dates

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

def get_time(message, context):
    # Get the current date
    current_date = datetime.now()
    entities = []
    numbers = []
    for token in appnlp(message):
        if token.ent_type_ != "":
            entities.append(token.text)

    for i in entities:
        if i.lower() in numbersWords:
            numbers.append(i)

    # If the user wants to know the weather in the past
    if "past" in context:
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
    elif "future" in context:
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
    elif "present" in context:
        current_date = current_date
    else:
        current_date = current_date

    # Get the date
    date = {"year": current_date.year, "month": current_date.month,
            "day": current_date.day, "hour": current_date.hour,
            "minute": current_date.minute, "second": current_date.second}
    print(date)
    return date

def get_stormwatch(lat, lng):
    # Get the stormwatch information
    weather_data = {}
    stormwatch_url = "https://api.stormglass.io/v2/weather/point?"
    stormwatch_url += "lat=" + str(lat) + "&lng=" + str(lng) + "&params=waveDirection"
    stormwatch_data = requests.get(stormwatch_url, headers={"Authorization": config["stormwatch"]})

    # Get the data
    weather_data["wave_direction"] = stormwatch_data.json()["hours"][0]["waveDirection"]["noWaveDirection"]["value"]

    return weather_data

def getmode(sentence):
    mode = 'default'
    tokens = appnlp(sentence.lower())
    for token in tokens:
        if token.text == 'street':
            mode = 'streetview'
        elif token.text == 'map' or token.text == 'images':
            mode = 'mapimage'
    return mode

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, "label") and t.label:
        if t.label() == "NE":
            entity_names.append(" ".join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def get_entities(line):
    sentences = nltk.sent_tokenize(line)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entities = []
    for tree in chunked_sentences:
        entities.extend(extract_entity_names(tree))

    print(entities)
    return entities

def locationResponse(sentence):
    # Location stuff
    # data = [lat, lng]
    # result being the string response, what the bot says to the user
    data = ""
    loc = find_location_by_ip()["location"];
    if(loc[0]!=None):
        if(getmode(sentence) == 'streetview'):
            result = "Here's a street view of " + loc[0] + ". "
            data = streetview(loc[0])
        elif(getmode(sentence) == 'mapimage'):
            result = "Here's a map of " + loc[0]+ ". "
            data = mapimg(loc[0])
    else:
        result = "Here's a street view of Kelowna. "
        data = streetview("Kelowna")
    return [result, data]

def streetview(location):
    meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
    pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
    api_key = 'AIzaSyAmxhIlDVfiAyXGUCEplWBixuU1ULJOuHQ'
    meta_params = {'key': api_key,
                'location': location}
    pic_params = {'key': api_key,
                'location': location,
                'size': "600x600"}
    meta_response = requests.get(meta_base, params=meta_params)
    meta_response.json()
    pic_response = requests.get(pic_base, params=pic_params)
    for key, value in pic_response.headers.items():
        print(f"{key}: {value}")
    with open('./static/img/street.jpg', 'wb') as file:
        file.write(pic_response.content)
    pic_response.close()
    # plt.figure(figsize=(10, 10))
    # img=mpimg.imread('street.jpg')
    # imgplot = plt.imshow(img)
    # plt.show()
    return url_for("static", filename="/img/street.jpg")

def mapimg(location):
    api_key = "AIzaSyAmxhIlDVfiAyXGUCEplWBixuU1ULJOuHQ"
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    center = location
    zoom = 15
    r = requests.get(url + "center=" + center + "&zoom=" + str(zoom) + "&size=640x640&key=" + api_key + "&sensor=false")
    f = open('address of the file location', 'wb')
    f.write(r.content)
    f.close()
    with open('./static/img/img.jpg', 'wb') as file:
        file.write(r.content)
    r.close()
    # plt.figure(figsize=(10, 10))
    # img=mpimg.imread('img.jpg')
    # imgplot = plt.imshow(img)
    # plt.show()
    return url_for("static", filename="/img/img.jpg")


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
