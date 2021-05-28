'''DEFAULT_BEACON_INTERVAL = 30
INIT_GPS = '0 0.0000, 0 00.0000'
global LOCK_STATE
LOCK_STATE = False

EVENTS = {
    'Alarm': False,
    'Open': False,
    'Closed': True,
    'Received': True,
    'Vibration': True,
    'Sanatized': False,
    'Temperature': 25,
    'Wifi_Error': False,
    'gps': '0 0.0000, 0 00.0000',
    'snap': False
}'''


#import urequests as requests

ADAFRUIT_IO_USERNAME = "ankit007"
ADAFRUIT_IO_KEY = "aio_YZEK82x4l14vky6t2Sj9PokSAUhx"
feedName = "safe"


import urequests as requests

url = "https://io.adafruit.com/api/v2/ankit007/feeds/safe/data/last.json"

headers = {'X-AIO-Key': 'aio_YZEK82x4l14vky6t2Sj9PokSAUhx',
           'Content-Type': 'application/json'}

r = requests.get(url, headers=headers)
results = r.json()
print(r.json())
#Below code for Posting new data

#url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/'+feedName+'/data'


#dataObj = {"value":"16"} # Put value which you want to store
#x = requests.post(url, data = dataObj, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})

'''import urequests as requests

url = "https://io.adafruit.com/api/v2/ankit007/feeds/safe/data.json"

headers = {'X-AIO-Key': 'aio_YZEK82x4l14vky6t2Sj9PokSAUhx',
           'Content-Type': 'application/json'}

data = '{"value": "123123"}'

r = requests.post(url, data=data, headers=headers)
results = r.json()
print(results)'''
