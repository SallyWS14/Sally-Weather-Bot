import requests
import socket
import json
# TODO: synonym, spellcheck

api_key = "2de35d4c586e85adf3afcbd482bd52dd"
# with open('../storage/data_location.json', 'r') as infile:
#     geo = json.load(infile)
# for loc in geo:
#     if(loc['ip'] == socket.gethostbyname(socket.gethostname())):
#         lat = loc['latitude']
#         lon = loc['longitude']
#         break

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    # print(data)
    # print("Current Weather: ", data['weather'][0]['description'])
    # print("Maximum Temperature: ", data['main']['temp_min'])
    # print("Minimum Temperature: ", data['main']['temp_max'])
    # print("Humidity", data['main']['humidity'])
    buildStr = f"The current weather is {data['weather'][0]['description']} with a high of {data['main']['temp_max']} and a low of {data['main']['temp_min']}. The humidity is {data['main']['humidity']}"
    return buildStr