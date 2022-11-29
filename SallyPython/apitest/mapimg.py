# Python program to get a google map
# image of specified location using
# Google Static Maps API

# importing required modules
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Enter your api key here
api_key = "AIzaSyAmxhIlDVfiAyXGUCEplWBixuU1ULJOuHQ"

# url variable store url
url = "https://maps.googleapis.com/maps/api/staticmap?"

# center defines the center of the map,
# equidistant from all edges of the map.
center = "Kelowna"

# zoom defines the zoom
# level of the map
zoom = 15

# get method of requests module
# return response object
r = requests.get(url + "center=" + center + "&zoom=" + str(zoom) + "&size=640x640&key=" + api_key + "&sensor=false")

# wb mode is stand for write binary mode
f = open('address of the file location', 'wb')

# r.content gives content,
# in this case gives image
f.write(r.content)

# close method of file object
# save and close the file
f.close()

with open('img.jpg', 'wb') as file:
    file.write(r.content)
# remember to close the response connection to the API
r.close()

# using matpltolib to display the image

plt.figure(figsize=(10, 10))
img=mpimg.imread('img.jpg')
imgplot = plt.imshow(img)
plt.show()
