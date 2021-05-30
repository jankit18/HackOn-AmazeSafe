import urequests as requests
import src
import json

def receive_data():
    url = src.URL + src.USER_NAME + "/feeds/" + src.FEED_RECEIVE +"/data/last.json"
    
    headers = {'X-AIO-Key': src.API_KEY ,
               'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers)
    results = r.json()["value"]
    return(json.loads((results)))

def send_data(value = None, feed = src.FEED_SEND):
    url = src.URL + src.USER_NAME + "/feeds/" + feed +"/data.json"

    headers = {'X-AIO-Key': src.API_KEY ,
               'Content-Type': 'application/json'}
    data = {"value": json.dumps(value)}
    requests.post(url, json=data, headers=headers).json()

