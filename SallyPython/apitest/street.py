import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    apikey = 'AIzaSyC6hJ8U_clMgEkSdsktg1M8m5L0T-xeEBw'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latlng}&key={apikey}'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    if data['results']:
        result = data['results'][0]['formatted_address']
    return result

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = 'AIzaSyC6hJ8U_clMgEkSdsktg1M8m5L0T-xeEBw'
# using my graduate school almar mater, GWU, as an example
print(reverseGeocode(ipInfo()))
location = reverseGeocode(ipInfo());
# define the params for the metadata reques
meta_params = {'key': api_key,
               'location': location}
# define the params for the picture request
pic_params = {'key': api_key,
              'location': location,
              'size': "600x600"}
# obtain the metadata of the request (this is free)
meta_response = requests.get(meta_base, params=meta_params)
# display the contents of the response
# the returned value are in JSON format
meta_response.json()
pic_response = requests.get(pic_base, params=pic_params)
for key, value in pic_response.headers.items():
    print(f"{key}: {value}")

with open('imgstreet.jpg', 'wb') as file:
    file.write(pic_response.content)
# remember to close the response connection to the API
pic_response.close()

# using matpltolib to display the image

plt.figure(figsize=(10, 10))
img=mpimg.imread('imgstreet.jpg')
imgplot = plt.imshow(img)
plt.show()
