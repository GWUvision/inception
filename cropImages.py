import json
import pandas as pd
from PIL import Image

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    # cropped_image.show()


with open("JSON-Data/00000012.json", "r") as f:
        data = json.load(f)

keys = list(data.keys())

x = data[keys[0]]['regions']['0']['shape_attributes']['x']
y = data[keys[0]]['regions']['0']['shape_attributes']['y']
height = data[keys[0]]['regions']['0']['shape_attributes']['height']
width = data[keys[0]]['regions']['0']['shape_attributes']['width']
#print(data)
print(json.dumps(data, indent=4, sort_keys=True))


# for ele in data:
#     print(data['region_attributes'])

#loop over all JSON
#loop over each picture
#loop over each box

def select_region():
    for j in range(0, len(keys)):
        for i in range(0, len(data[keys[j]]['regions'])):
            filename = data[keys[j]]['filename']

            x1 = data[keys[j]]['regions'][str(i)]['shape_attributes']['x']
            y1 = data[keys[j]]['regions'][str(i)]['shape_attributes']['y']
            y2 = y1 + data[keys[j]]['regions'][str(i)]['shape_attributes']['height']
            x2 = x1 + data[keys[j]]['regions'][str(i)]['shape_attributes']['width']

            crop('./images/00000012/' + filename, (x1, y1, x2, y2), 'output/' + filename + str(i) + '.jpg')

select_region()
