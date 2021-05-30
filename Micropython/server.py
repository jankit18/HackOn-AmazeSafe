from time import sleep
import src
import network


def connect_wlan(essid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network...", end="")
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
        print("done")
    my_ip = wlan.ifconfig()[0]
    return my_ip


def countdown(t):

    while t:
        secs = t
        timer = "FETCH EVENT AFTER "+str(secs)+" sec......."
        print(timer, end="\r")
        sleep(1)
        t -= 1


def run(essid, password):
    my_ip = connect_wlan(essid, password)
    print("Server is running [{}].".format(my_ip))
    LOCK_STATE = src.DEFAULT_LOCK_STATE
    open_ = 0
    threat = False
    while(not threat):
        countdown(src.DEFAULT_BEACON_INTERVAL)
        init_data = src.receive_data()
        if init_data['open']:
            open_ = open_ +1
        event = src.Event(ideal_gps=src.INITIAL_GPS,
                          gps_threshold=src.GPS_THRESHOLD,
                          Open=init_data['open'],
                          delivered=init_data['delivered'],
                          sanatize=init_data['sanitize'],
                          lock_state=LOCK_STATE)
        event.update_state()
        LOCK_STATE = event.lock_state
        send_info = {'GPS': event.gps,
                     'TEMPERATURE': event.temperature,
                     'ALARM': event.alarm,
                     'IMAGE': event.image
                    }
        if event.alarm:
            threat = True
        src.send_data(value = send_info, feed = src.FEED_SEND)
        if init_data['delivered']:
            send_info1 = {'open' : False,
                         'delivered' : False,
                         'sanitize' : False
                         }
            src.send_data(value = send_info1, feed = src.FEED_RECEIVE)
        elif init_data['sanitize']:
            send_info2 = {'open' : init_data['open'],
                         'delivered' : False,
                         'sanitize' : False
                         }
            src.send_data(value = send_info2, feed = src.FEED_RECEIVE)
        if open_>2:
            print("OPEN TIMEOUT BOX CLOSING")
            send_info3 = {'open' : False,
                         'delivered' : False,
                         'sanitize' : False
                         }
            src.send_data(value = send_info3, feed = src.FEED_RECEIVE)
            open_ = 0
                          
        print("*********************EVENT OVER **************************")
        
    print("##################Alarm is ON Your package is in threat#############")


