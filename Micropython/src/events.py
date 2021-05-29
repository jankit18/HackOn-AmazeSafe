import random
import time


class Event:

    def __init__(
            self,
            ideal_gps=None,
            gps_threshold=None,
            Open=True,
            delivered=True,
            sanatize=False,
            lock_state=None):

        self.ideal_gps = ideal_gps
        self.gps = None
        self.vibratation_flag = None
        self.temperature = None
        self.Close = not Open
        self.Open = Open
        self.delivered = delivered
        self.alarm = False
        self.sanatize = sanatize
        self.snap = False
        self.gps_threshold = gps_threshold
        self.lock_state = lock_state
        self.image = None

    def update_state(self):

        self.gps = self.get_gps_state()
        print('CURRENT GPS COORDINATES', self.gps)

        if not self.check_threshold_gps(
                self.gps,
                self.ideal_gps,
                self.gps_threshold):
            self.alarm = True
            print('GPS WITHIN THRESHOLD ->', False)

        self.vibratation_flag = self.vibratation_state()
        if self.vibratation_flag:
            self.alarm = True
            print("PACKAGE IS VIBRATING")

        self.temperature = self.get_temperature()
        print("CURRENT TEMPERATURE OF SYSTEM IS",self.temperature)

        if self.Open:
            self.unlock()
            if self.delivered:
                self.Close = True
                print("PACKAGE HAS BEEN DELIVERED AND BOX IS CLOSING")
                self.sanatize = False

        if self.sanatize:
            self.sanatize = self.sanatize_box()
            print('BOX HAS BEEN SANATIZED')

        if self.alarm:
            self.Close = True
            self.snap = True
            print("ALARM INITIATED")
            self.alarm = False

        if self.Close:
            self.lock()

        if self.snap:
            self.image = self.get_snap()
            self.snap = False

    def get_gps_state(self):

        ''' Ideally it should get the required coordinates from
        the GPS module but since it has not been implemented yet
        we return random junk values'''

        return ([random.getrandbits(4), random.getrandbits(4)])

    def check_threshold_gps(self,
                            Current_gps=None,
                            Ideal_gps=None,
                            Gps_threshold=None):

        ''' Ideally it should calculate the distance from actual
        location but since it has not been implemented yet
        simple comparison'''
        if ((Ideal_gps[0]-Current_gps[0])**2 + (Ideal_gps[1]-Current_gps[1])**2)**0.5 < Gps_threshold:
            return True
        else:
            return False

    def get_temperature(self):

        ''' Ideally it should get the current temperature
        using SPI sensors and hence return the temperature'''

        return(random.getrandbits(6)%35)

    def unlock(self):
        ''' Will be used to refer to functions for unlocking the lock'''
        if self.lock_state:
            self.lock_state = False
            print("LOCK HAS BEEN UNLOCKED")
            return True   # you have to unlock

        else:
            print("SAFE ALREADY IS UNLOCKED")
            return False  # you donot have to unlock

    def lock(self):
        ''' Will be used to refer to functions for locking the lock'''
        if self.lock_state:
            print("LOCK HAS BEEN ALREADY LOCKED")
            return False   # you have to unlock

        else:
            self.lock_state = True
            print("SAFE ALREADY IS UNLOCKED")
            return True  # you donot have to unlock

    def sanatize_box(self):
        ''' Will be used to activate the sanatizer'''

        return(True)

    def get_snap(self):
        ''' Will be used to get the image from the camera'''
        image = b'314234234fww'
        print('IMAGE TAKEN')
        return (image)

    def vibratation_state(self):
        if random.getrandbits(5)%4 == 0:
            return True
        else:
            return False
