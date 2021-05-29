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
    while(True):
        init_data = src.receive_data()
        event = src.Event(ideal_gps=src.INITIAL_GPS,
                          gps_threshold=src.GPS_THRESHOLD,
                          Open=init_data['open'],
                          delivered=init_data['delivered'],
                          sanatize=init_data['sanatize'],
                          lock_state=LOCK_STATE)
        event.update_state()
        LOCK_STATE = event.lock_state
        countdown(src.DEFAULT_BEACON_INTERVAL)
        send_info = {'GPS': event.gps,
                     'TEMPERATURE': event.temperature,
                     'ALARM': event.alarm,
                     'IMAGE': event.image
                    }
        src.send_data(send_info)
        print("*********************EVENT OVER **************************")


run(wifi_username,password)
