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
    width, height = image_obj.size
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    # cropped_image.show()

#loop over all JSONs
#loop over each picture
#loop over each box

def select_region():
    labels = {}
    index = 0
    for k in range(1, 19):
        with open("JSON-Data/" + str(k).zfill(8) + ".json", "r") as f:
                data = json.load(f)

        keys = list(data.keys())

        for j in range(0, len(keys)):

            for i in range(0, len(data[keys[j]]['regions'])):
                filename = data[keys[j]]['filename']

                if data[keys[j]]['regions'][str(i)]['shape_attributes']['width'] == 0 or data[keys[j]]['regions'][str(i)]['shape_attributes']['height'] == 0:
                    continue

                x1 = data[keys[j]]['regions'][str(i)]['shape_attributes']['x']
                y1 = data[keys[j]]['regions'][str(i)]['shape_attributes']['y']
                y2 = y1 + data[keys[j]]['regions'][str(i)]['shape_attributes']['height']
                x2 = x1 + data[keys[j]]['regions'][str(i)]['shape_attributes']['width']

                labels[str(index)] = []
                labels[str(index)].append(data[keys[j]]['regions'][str(i)]['region_attributes'])

                # print('width = ' + str(data[keys[j]]['regions'][str(i)]['shape_attributes']['width']))
                # print('height = ' + str(data[keys[j]]['regions'][str(i)]['shape_attributes']['height']))
                # print('x1 = ' + str(x1))
                # print('y1 = ' + str(y1))
                # print('x2 = ' + str(x2))
                # print('y2 = ' + str(y2))

                # print(json.dumps(data, indent=4, sort_keys=True))

                crop('./Traffic_Dataset/' + str(k).zfill(8) + '/' + filename, (x1, y1, x2, y2), 'output/' + str(index) + '.jpg')
                index += 1

    with open('label.txt', 'w') as outfile:
        json.dump(labels, outfile)

select_region()
