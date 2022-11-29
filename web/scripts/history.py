import datetime
import json
import socket
import requests
import spacy
from spacy.lang.en import English
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token

sp = spacy.load('en_core_web_sm')

# from web.scripts.history import histInfo

with open('./config.json', 'r') as f:
    config = json.load(f)
    
weatherapikey = config['weatherapikey']
    
# with open('../storage/location.json', 'r') as f:
#     location = json.load(f)
        
# # if name is found in the location.json file, update else create a new entry
# def locationUpdate(name, location):
#     res = getLocation(name, name)
#     if res is not None:
#         newLoc = {}
#     else:
        
# look for a location value if the name matches the name key in the location.json file
# def getLocationByName(name, lookfor='location'):
#     for loc in location:
#         if location[loc]['name'] == name:
#             return location[loc][lookfor]
        
# def getLocationByIp(ip, lookfor='location'):
#     for loc in location:
#         if location[loc]['ip'] == ip:
#             return location[loc][lookfor]

openWeatherMapApiKey = config['API_KEY']
openWeatherMapEndPoint = config['OpenWeatherMapEndpoint']
class History:
    def __init__(self, text, tense, location = [], rdate = datetime.datetime.now().date(), unit = 'C', time = datetime.datetime.now().hour):
        # self.url = config['history']['url']
        r = requests.get("https://restcountries.com/v2/all")
        r.raise_for_status()
        countries = r.json()
        self.nlp = English()
        # self.countries = {c["name"]: c for c in countries}
        # self.matcher = PhraseMatcher(sp.vocab)
        # self.matcher.add("COUNTRIES", [self.nlp.make_doc(c) for c in self.countries.keys()])
        # Span.set_extension("is_country", default=None)
        # Span.set_extension("country_capital", default=None)
        # Doc.set_extension("has_country", default=None)
        self.location = location
        self.date = rdate
        self.unit = unit
        self.time = time
        self.tokens = []
        self.location = ""
        self.tense = tense
        self.message = self.nlp(text)
        self.message_raw = text
        self.ip = location['ip']
        self.location_file = '../storage/location.json'
        
    def has_country(self):
        """Checks if the message has a country in it"""
        return any([entity._.get("is_country") for entity in self.message.ents])
        
    def get_tokens(self, message):
        """Gets the tokens from the message"""
        self.tokens = sp(message)
        return self.tokens
    
    def set_location(self, location):
        """Gets the location data from the location.json file"""
        self.location = location
    
    def get_context(self, message):
        """Gets the context of the message"""
        tokens = self.get_tokens(message)
        # get the location
        for token in tokens:
            if token.ent_type_ == 'GPE':
                self.set_location(token.text)
                
                
    def get_tense(self, message):
        """Gets the tense of the message"""
        tokens = self.get_tokens(message)
        for token in tokens:
            if token.tag_ == 'VBD' or token.tag_ == 'VBN':
                return 'past'
            elif token.tag_ == 'VBZ' or token.tag_ == 'VBP':
                return 'present'
            elif token.tag_ == 'VB' or token.tag_ == 'VBP':
                return 'future'
            else:
                return 'present'
    
    def process(self, location: str, date, unit: str, time: int):
        """Gets the weather data from the weather api and returns it
            location: the location to get the weather data for
            date is in the format of YYYY-MM-DD
            unit is either metric or imperial
            time is the current hour in 24 hour format
        """
        # get the location data
        location = self.location
        time = time if time is not None else datetime.datetime.now().hour
        # get the weather data
        mtense = "current"
        if self.tense == "history":
            mtense = "history"
        elif self.tense == "future":
            mtense = "future"
        else:
            mtense = mtense

        url = f'https://api.weatherapi.com/v1/{mtense}.json?key={weatherapikey}&q={location}&dt={date}&hour={time}'
        req = requests.get(url)
        if (req.status_code == 200):
            data = req.json()
            history = {
                'location': data['location'],
                'forcast': data['forecast'],
                'day': data['forecast']['forecastday'][0]['day'],
                'hours': data['forecast']['forecastday'][0]['hour'],
            }
            hour = "12 AM" if (time == 0) else str(time)+" AM" if (int(time) < 12) else str(time) + ' PM'
            weather = ""
            # build weather return string
            if unit == 'c':
                weather += f"{history['location']['name']}, {history['location']['region']}, {history['location']['country']}\n"
                weather += f"{history['day']['condition']['text']} with a high of {history['day']['maxtemp_t']}°F and a low of {history['day']['mintemp_t']}°F on {data['forecast']['forecastday'][0]['date']}. "
                weather += f"At {hour} it was {history['hours'][time]['condition']['text']} with a temperature of {history['hours'][time]['temp_t']}°F and a humidity of {history['hours'][time]['humidity']}%."
            else:
                weather += f"{history['location']['name']}, {history['location']['region']}, {history['location']['country']}"
                weather += f"{history['day']['condition']['text']} with a high of {history['day']['maxtemp_f']}°F and a low of {history['day']['mintemp_f']}°F on {data['forecast']['forecastday'][0]['date']}."
                weather += f"At {hour} it was {history['hours'][time]['condition']['text']} with a temperature of {history['hours'][time]['temp_f']}°F and a humidity of {history['hours'][time]['humidity']}%."
                
            return weather
        else:
            return "Error: Could not get weather data"
    def reply(self):
        return self.process(self.location, self.date, self.unit, self.time)