import requests
import json
import datetime

with open('../storage/config.json', 'r') as f:
    config = json.load(f)
    
with open('../storage/location.json', 'r') as f:
    location = json.load(f)
    

class History:
    def __init__(self) -> None:
        pass
    
    def GetLocation(self, location):
        """Gets the location data from the location.json file"""
        return location[location]
    
    def Process(self, location: str, date: str, unit: str, time: int):
        """Gets the weather data from the weather api and returns it
            location: the location to get the weather data for
            date is in the format of YYYY-MM-DD
            unit is either metric or imperial
            time is the current hour in 24 hour format
        """
        # get the location data
        location = self.GetLocation(location)
        time = time if time is not None else datetime.datetime.now().hour
        # get the weather data
        url = f'https://api.weatherapi.com/v1/history.json?key={weatherapikey}&q={location}&dt={date}&hour={time}'
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
                weather += f"{history['location']['name']}, {history['location']['region']}, {history['location']['country']}"
                weather += f"{history['day']['condition']['text']} with a high of {history['day']['maxtemp_t']}°F and a low of {history['day']['mintemp_t']}°F on {history['day']['date']}."
                weather += f"At {hour} it was {history['hours'][time]['condition']['text']} with a temperature of {history['hours'][time]['temp_t']}°F and a humidity of {history['hours'][time]['humidity']}%."
            else:
                weather += f"{history['location']['name']}, {history['location']['region']}, {history['location']['country']}"
                weather += f"{history['day']['condition']['text']} with a high of {history['day']['maxtemp_f']}°F and a low of {history['day']['mintemp_f']}°F on {history['day']['date']}."
                weather += f"At {hour} it was {history['hours'][time]['condition']['text']} with a temperature of {history['hours'][time]['temp_f']}°F and a humidity of {history['hours'][time]['humidity']}%."
                
            return weather
        else:
            return "Error: Could not get weather data"
    