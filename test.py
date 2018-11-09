import base64
import json
import os
import ssl
try:
    import httplib  # Python 2
except:
    import http.client as httplib  # Python 3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

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


def findAny(atr, cars):
    # draw bounding box
    for car in cars:
        color = car['vehicleAnnotation']['attributes']['system']['color']['name']
        make = car['vehicleAnnotation']['attributes']['system']['make']['name']
        model = car['vehicleAnnotation']['attributes']['system']['model']['name']
        type = car['vehicleAnnotation']['attributes']['system']['vehicleType']
        if atr.lower() == color.lower() or atr.lower() == make.lower() or atr.lower() == model.lower() or atr.lower() == type.lower():
            drawBox(car, ax)


def findTypeColor(type, color, cars):
    # draw bounding box
    for car in cars:
        car_color = car['vehicleAnnotation']['attributes']['system']['color']['name']
        car_type = car['vehicleAnnotation']['attributes']['system']['vehicleType']
        if color.lower() == car_color.lower() and type.lower() == car_type.lower():
            drawBox(car, ax)



headers = {"Content-type": "application/json",
           "X-Access-Token": "nikyJuVbPcrjvx2W7A1ijY76V7uBpGRXNpTA"}
conn = httplib.HTTPSConnection("dev.sighthoundapi.com",
       context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

image = 'maxresdefault_live.jpg'

# To use a hosted image uncomment the following line and update the URL
#image_data = "http://example.com/path/to/hosted/image.jpg"

# To use a local file uncomment the following line and update the path
image_data = base64.b64encode(open(image, "rb").read()).decode()

# api call
params = json.dumps({"image": image_data})
conn.request("POST", "/v1/recognition?objectType=vehicle,licenseplate", params, headers)
response = conn.getresponse()
result = response.read()

# parse json
my_json = result.decode('utf8').replace("'", '"')
data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)

im = np.array(Image.open(image), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# findAny('ford', data['objects'])
findTypeColor('suv', 'white', data['objects'])

plt.show()
# print(s)
