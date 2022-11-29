# importing requests and json
import requests, json
from scripts import rewordSentence

with open('../config.json', 'r') as configfile:
    config = json.load(configfile)
    
with open('./storage/data_location.json', 'r') as locationJson:
    location = json.load(locationJson)
    
url1 = "https://api.openweathermap.org/data/2.5/weather?lat="

#Default lat and lon is Kelowna
lat = "49.88"
lon = "-119.47"
API_KEY = config['API_KEY']

URL = url1 + lat + "&lon=" + lon + "&appid=" + API_KEY + "&units=metric"


response = requests.get(URL)

#Grab current users latitude and longitude

def getLocation():
    lat = location[0]['latitude']
    lon = location[0]['latitude']


def getDressSense():
    getLocation()
    
    if response.status_code == 200: 
        data = response.json()
        main = data['main']
   
        temperature = main['temp']
        clouds = data['clouds']['all']
        windSpeed = data['wind']['speed']
        report = data['weather']
        isRaining = "rain" in report[0]['description']
        
        
        
        w = "I recommend you wear: \n"
        try:
            wear = rewordSentence.getRewordSentence(w) + "\n"
        except:
            wear = "I recommend you wear:  \n"
            print('there was an error with running rewordSentence')
            
   
        def checkIfWindy():
            if (windSpeed):
                 wear = wear + (' - a windbreaker \n') + ('- a hat\n')
           
   
        if(isRaining):
            wear = wear + ('- a raincoat \n') + ('- rain boots \n') + ('- an umbrella \n')
   
        if(temperature < -13):
            wear = wear + ('- a winter jacket \n' ) + ('- a scarf \n') + ('- gloves \n') + ('- a hat \n ')
   
        if(temperature >= -13 and temperature < 7):
            wear = wear + ('- a light or medium jacket \n')
            if(windSpeed >= 40):
                wear = wear + ('- a hat\n')
   
        if(temperature >= 7 and temperature < 15):
            wear = wear + ('- a hoodie or a sweater \n')
            checkIfWindy()
   
        if(temperature >= 15 and temperature < 22):
            wear = wear + ('- a T-shirt \n')
            checkIfWindy()
       
   
        if(temperature >= 22):
            wear = wear + ("- a short sleeved shirt \n") + ("- shorts \n")
            if(clouds<40):
                 wear = wear + ('- a hat \n') + ('- sunglasses \n')
                 
        try:
            wear = wear + sentimentNLTK.isNegOrIsPos(wear)
        except:
            print('there was an error with running sentimentNLTK')
         
                 
        return wear
    else:
        return("Sorry there was an error")
    
# print(getDressSense())
 
