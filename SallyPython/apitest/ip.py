import requests


def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    #will load the json response into data
    for attr in data.keys():
        #will print the data line by line
        print(attr,' '*13+'\t->\t',data[attr])
    return data["loc"]

def reverseGeocode(latlng):
    result = {}
    apikey = 'AIzaSyAmxhIlDVfiAyXGUCEplWBixuU1ULJOuHQ'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latlng}&key={apikey}'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    if data['results']:
        result = data['results'][0]['formatted_address']
    return result

print(reverseGeocode(ipInfo()))
