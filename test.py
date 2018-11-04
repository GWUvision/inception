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

headers = {"Content-type": "application/json",
           "X-Access-Token": "nikyJuVbPcrjvx2W7A1ijY76V7uBpGRXNpTA"}
conn = httplib.HTTPSConnection("dev.sighthoundapi.com",
       context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

# To use a hosted image uncomment the following line and update the URL
#image_data = "http://example.com/path/to/hosted/image.jpg"

# To use a local file uncomment the following line and update the path
image_data = base64.b64encode(open("./half.jpeg", "rb").read()).decode()

# api call
params = json.dumps({"image": image_data})
conn.request("POST", "/v1/recognition?objectType=vehicle,licenseplate", params, headers)
response = conn.getresponse()
result = response.read()

# parse json
my_json = result.decode('utf8').replace("'", '"')
data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)

# draw bounding box
x = data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][0]['x']
y = data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][0]['y']
height = data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][2]['y'] - data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][0]['y']
width = data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][2]['x'] - data['objects'][0]['vehicleAnnotation']['bounding']['vertices'][0]['x']

im = np.array(Image.open('half.jpeg'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((x,y),height,width,linewidth=1,edgecolor='r',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()


print(s)
