import json
import logging
import os
import re
from datetime import datetime
import urllib.request as req
import socket

import requests
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English

class SallyNLP:

    def __init__(self, message, ip):
        self.message = message
        self.ip = ip
        self.location_file = '../storage/location.json'

    def save_location(self, loc, lat, lon):
        loc = self.location_file
        if not os.path.isfile(loc):
            data = {"locations": []}
        else:
            with open(loc) as jsonFile:
                data = json.load(jsonFile)
                userLocationData = [locationData for locationData in data["locations"] if locationData["ip"] == self.ip]
                if len(userLocationData) > 0:
                    userLocationData[0]["location"] = loc
                    userLocationData[0]["lat"] = lat
                    userLocationData[0]["lng"] = lon
                    return
        data["locations"].append({"ip": self.ip, "location": loc, "lat": lat, "lng": lon})
        with open(loc, "w") as jsonFile:
            json.dump(data, jsonFile)

    def get_location(self):
        userLocationFile = self.location_file
        if not os.path.isfile(userLocationFile):
            return None
        with open(userLocationFile) as jsonFile:
            userLocationData = json.load(jsonFile)
            userLocation = [location for location in userLocationData["locations"] if location["ip"] == self.ip]
            if len(userLocation) > 0:
                return userLocation[0]
            return None

    def new_location(self):
        if self.get_location() is None:
            newLoc = self.find_location_by_ip()
            if newLoc is not None:
                self.save_location(newLoc["location"], newLoc["lat"], newLoc["lng"])
                return True
            else:
                return False
    
    def find_location_by_ip(self):
        with req.urlopen("https://geolocation-db.com/json/"+self.ip) as locdata:
            data = json.loads(locdata.read().decode())
            # print(data)
            lat = data["latitude"]
            long = data["longitude"]
            location = data["city"] + ", " + data["state"] + ", " + data["country_name"]
            res = {"ip": self.ip, "lat": lat, "lng": long, "location": location}
            print(res)
            return res


sally = SallyNLP(input(">> "), socket.gethostbyname(socket.gethostname()))
sally.find_location_by_ip()