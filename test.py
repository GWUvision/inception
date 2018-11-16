import json
import requests
import ssl
import numpy as np
import http.client as httplibs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO, StringIO
import random

def maxmax(num1, num2, num3, num4):
    return max(max(num1, num2), max(num3, num4))

def minmin(num1, num2, num3, num4):
    return min(min(num1, num2), min(num3, num4))

def drawBox(car, ax):
    x = car['vehicleAnnotation']['bounding']['vertices'][0]['x']
    y = car['vehicleAnnotation']['bounding']['vertices'][0]['y']

    height = maxmax(car['vehicleAnnotation']['bounding']['vertices'][0]['y'], car['vehicleAnnotation']['bounding']['vertices'][1]['y'], car['vehicleAnnotation']['bounding']['vertices'][2]['y'], car['vehicleAnnotation']['bounding']['vertices'][3]['y']) - minmin(car['vehicleAnnotation']['bounding']['vertices'][0]['y'], car['vehicleAnnotation']['bounding']['vertices'][1]['y'], car['vehicleAnnotation']['bounding']['vertices'][2]['y'], car['vehicleAnnotation']['bounding']['vertices'][3]['y'])

    width = maxmax(car['vehicleAnnotation']['bounding']['vertices'][0]['x'], car['vehicleAnnotation']['bounding']['vertices'][1]['x'], car['vehicleAnnotation']['bounding']['vertices'][2]['x'], car['vehicleAnnotation']['bounding']['vertices'][3]['x']) - minmin(car['vehicleAnnotation']['bounding']['vertices'][0]['x'], car['vehicleAnnotation']['bounding']['vertices'][1]['x'], car['vehicleAnnotation']['bounding']['vertices'][2]['x'], car['vehicleAnnotation']['bounding']['vertices'][3]['x'])

    color = car['vehicleAnnotation']['attributes']['system']['color']['name']
    make = car['vehicleAnnotation']['attributes']['system']['make']['name']
    type = car['vehicleAnnotation']['attributes']['system']['vehicleType']
    label = color + ', ' + make + ', ' + type
    # Create a Rectangle patch
    rect = patches.Rectangle((x,y),width,height,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.text(x, y, label)

def findCars(cars, url):
    global i
    s = json.dumps(cars, indent=4, sort_keys=True)
    # print(s)

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    #print(img)

    # im = np.array(Image.open(url), dtype=np.uint8)
    # im = np.array(img, dtype=np.uint8)
    im = np.array(img)

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    for car in cars:
        drawBox(car, ax)

    #save the plot to an output folder
    plt.savefig('./output/image' + str(i) + '.jpg')
    i += 1

def findAny(atr, cars, url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # im = np.array(Image.open(url), dtype=np.uint8)
    im = np.array(img)
    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # draw bounding box
    for car in cars:
        color = car['vehicleAnnotation']['attributes']['system']['color']['name']
        make = car['vehicleAnnotation']['attributes']['system']['make']['name']
        model = car['vehicleAnnotation']['attributes']['system']['model']['name']
        type = car['vehicleAnnotation']['attributes']['system']['vehicleType']
        if atr.lower() == color.lower() or atr.lower() == make.lower() or atr.lower() == model.lower() or atr.lower() == type.lower():
            drawBox(car, ax)

    #save the plot to an output folder
    plt.savefig('./output/image' + str(i) + '.jpg')
    i += 1


def findTypeColor(type, color, cars, url):
    response = requests.get(url)
    img = Image.open(StringIO(response.content))

    # im = np.array(Image.open(url), dtype=np.uint8)
    im = np.array(img)
    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # draw bounding box
    for car in cars:
        car_color = car['vehicleAnnotation']['attributes']['system']['color']['name']
        car_type = car['vehicleAnnotation']['attributes']['system']['vehicleType']
        if color.lower() == car_color.lower() and type.lower() == car_type.lower():
            drawBox(car, ax)
    #save the plot to an output folder
    plt.savefig('./output/image' + str(i) + '.jpg')
    i += 1

def getImageData(image_data):
    headers = {"Content-type": "application/json",
               "X-Access-Token": "nikyJuVbPcrjvx2W7A1ijY76V7uBpGRXNpTA"}
    conn = httplibs.HTTPSConnection("dev.sighthoundapi.com",
           context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

    # api call
    params = json.dumps({"image": image_data})
    conn.request("POST", "/v1/recognition?objectType=vehicle,licenseplate", params, headers)
    response = conn.getresponse()
    result = response.read()

    # parse json
    my_json = result.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    # s = json.dumps(data, indent=4, sort_keys=True)
    return data

def getImages():
    headers = {"accept": "application/json",
               "Authorization": "apikey s2ZoJwvCcLoJ9QDkHg9wii9YNMlxYdUYgMuY"}
    conn = httplibs.HTTPSConnection("api.transport.nsw.gov.au",
           context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

    params = {}
    conn.request("GET", "/v1/live/cameras", params, headers)
    response = conn.getresponse()
    result = response.read()

    # parse json
    my_json = result.decode('utf8').replace('""', '')
    data = json.loads(my_json)

    # s = json.dumps(data, indent=4, sort_keys=True)
    return data


def main():
    i = 0
    images = getImages()

    for val in images['features'][:30]:
        print(val['properties']['href'])
        url = val['properties']['href']
        data = getImageData(url)

	    # findCars(data['objects'])
	    # savefig('foo.png')
        findCars(data['objects'], url)


    #plt.show()
i = 0
if __name__ == "__main__": main()
