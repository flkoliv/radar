#!/usr/bin/env python

import time, sys
import signal
import VL53L1X


class Telemeter():

    def __init__(self):
        self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.tof.open()
        self.tof.set_timing(66000, 70)
        signal.signal(signal.SIGINT, self.__exit_handler)
        

    def get_distance(self):
        return self.tof.get_distance()

    def start(self):
        self.tof.start_ranging(2)
        self.running = True
        return self

    def stop(self):
        self.tof.stop_ranging()

    def __exit_handler(self,signal, frame):
        self.running = False
        self.stop()


if __name__=="__main__":
    tel = Telemeter().start()
    while tel.running:
        start = time.time()
        distance_in_mm = tel.get_distance()
        print("Distance: {}mm, time: {}".format(distance_in_mm, time.time() - start))
<<<<<<< HEAD
        time.sleep(2)
=======
    
>>>>>>> 17a1bf6e792d09c8e6248febf801a0a0c34a15a
