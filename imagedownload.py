#!/pless_nfs/home/krood20/AMOSEast/env/bin/python

#Traffic Cameras Dataset --> https://catalog.data.gov/dataset/traffic-cameras-af0c9
import datetime
import gevent
import hashlib
import os
import pandas as pd

from gevent import monkey, socket
from gevent.pool import Pool

from socket import timeout
from socket import error as SocketError
from urllib.parse import urlparse
import urllib.request
import http.client

# Using threading to download files here
def download_file(index, url):
    #print('starting %s' % url)
    try:
        data = urllib.request.urlopen(url, timeout=5)

        dt = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        data = data.read()
        filename = os.path.basename(dt)
        filepath = '%s/%s_%s.jpg' % (str(index).zfill(8), index, filename)
        # print(filepath)
        # print(index)
        os.makedirs('images/%s' % str(index).zfill(8), exist_ok=True)
        f = open('images/%s/%s_%s.jpg' % (str(index).zfill(8), index, filename), 'wb')
        f.write(data)
        f.close()

    except urllib.error.HTTPError as err:
        print(err)
    except urllib.error.URLError as err:
        print(err)
    except timeout as err:
        print(err)
    except http.client.HTTPException as err:
        print(err)
    except http.client.IncompleteRead as err:
        print(err)
    except http.client.ImproperConnectionState as err:
        print(err)
    except http.client.RemoteDisconnected as err:
        print(err)
    except ConnectionResetError as err:
        print(err)
    except SocketError as err:
        print(err)
    # except:
    #     conn.rollback()


monkey.patch_socket()
pool = Pool(30)

#need to get all of the camera information
cameras = pd.read_json("kansas_cameras.json")

#print(cameras['ImageUrl'])

camera_urls = cameras['ImageUrl']

jobs = [pool.spawn(download_file, index, url) for index, url in camera_urls.items()]

print('Downloaded images')
