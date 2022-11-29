import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = 'AIzaSyAmxhIlDVfiAyXGUCEplWBixuU1ULJOuHQ'
# using my graduate school almar mater, GWU, as an example
location = "kelowna";
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

with open('street.jpg', 'wb') as file:
    file.write(pic_response.content)
# remember to close the response connection to the API
pic_response.close()

# using matpltolib to display the image

plt.figure(figsize=(10, 10))
img=mpimg.imread('street.jpg')
imgplot = plt.imshow(img)
plt.show()
