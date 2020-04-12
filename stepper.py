#!/usr/bin/env python 

# libraries
import time
import RPi.GPIO as GPIO

class Stepper():
    
    def __init__(self, halfStep=True):
        GPIO.setmode(GPIO.BCM)
        # Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
        self.StepPins = [24,25,8,7]
        # Set all pins as output
        for pin in self.StepPins:
            print("Setup pins")
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        # Define some settings
        self.WaitTime = 0.002
        self.halfStep = halfStep
        # Define simple sequence
        StepCount1 = 4
        Seq1 = []
        Seq1.append([1,0,0,0])
        Seq1.append([0,1,0,0])
        Seq1.append([0,0,1,0])
        Seq1.append([0,0,0,1])
        # Define advanced half-step sequence
        StepCount2 = 8
        Seq2 = []
        Seq2.append([1,0,0,0])
        Seq2.append([1,0,0,0])
        Seq2.append([1,1,0,0])
        Seq2.append([0,1,0,0])
        Seq2.append([0,1,1,0])
        Seq2.append([0,0,1,0])
        Seq2.append([0,0,1,1])
        Seq2.append([0,0,0,1])
        Seq2.append([1,0,0,1])
        # Choose a sequence to use
        if self.halfStep:
            self.Seq = Seq2
            self.StepCount = StepCount2
        else:
            self.Seq = Seq1
            self.StepCount = StepCount1
    
    def steps(self, nb):
        StepCounter = 0
        if nb<0: sign=-1
        else: sign=1
        nb=sign*nb*2 #times 2 because half-step
        print("nbsteps {} and sign {}".format(nb,sign))
        for i in range(nb):
            for pin in range(4):
                xpin = self.StepPins[pin]
                if self.Seq[StepCounter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
            StepCounter += sign
        # If we reach the end of the sequence
        # start again
            if (StepCounter==self.StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = self.StepCount-1
            # Wait before moving on
            time.sleep(self.WaitTime)

    def stop(self):
        for pin in self.StepPins:
            GPIO.output(pin, False)

if __name__=="__main__":
    nbStepsPerRev=2048
    stepper = Stepper()
    stepper.steps(nbStepsPerRev)# parcourt un tour dans le sens horaire
    time.sleep(1)
    stepper.steps(-nbStepsPerRev//2)# parcourt un tour dans le sens anti-horaire
    time.sleep(1)
    stepper.stop()
