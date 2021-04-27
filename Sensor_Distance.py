import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 13
ECHO = 19
BUTTON = 23
LIGHT = 18
BUZZER = 26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LIGHT, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LIGHT, False)
GPIO.output(BUZZER, False)


def armed():
    GPIO.output(LIGHT, True) #Turns on LED indicating the system is armed and polling


def distanceMath(start, end):
    #distance math function. distance = speed * Time, however input from the echo pin is time from the emitter
    #to the object and back to the reciever, so the time must be /2 to get only the distance to the object. Thus the distance is time-duration * (34300/2)
    duration = end-start
    distance = (duration * 17150)
    distance = round(distance, 2)
    #speed of sound is 343m/s which is = to 34300cm/s. 

    return distance

def pollPosition():
    

    while True:
        GPIO.output(TRIG, True) #trig pin starts the ultrasonic pulse and then turns the pin off
        ##time.sleep(.00001)
        GPIO.output(TRIG,False)

        while GPIO.input(ECHO) == 0: #echo is the input pin on the sensor, after pulse is sent, the sensor reads the time when it was last a zero or low signal and sets time to start
            #then when input is read, or rather echo reads a high signal or a 1 it is set to time end
            start = time.time()

        while GPIO.input(ECHO) == 1:
            end=time.time()

        pollDistance = distanceMath(start,end) #sends start and end times to math function to calculate distance in cm
        print("Current distance is:",pollDistance,"cm") #prints to console the distance currently measured
        checkThresh(pollDistance) #checks the distance against the set thresh hold
        time.sleep(3) #sleeps 3 seconds to allow for stable measuring performance, can be slower or faster 3 sec seemed a good compromise

def setThresh(): #runs same function as pollPosition but sets a global variable for the first time to set the threshhold that if exceeded triggers the alarm
    GPIO.output(TRIG, True)
    ##time.sleep(.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        end=time.time()

    global thresh

    thresh = distanceMath(start,end) #alarm threshold calculated in cm

def checkThresh(currentDistance):
    threshDeviation = thresh+5 #adds five cm to the threshold measurement to decrease the likelihood of a false positive alarm and control for calibration errors

    if(currentDistance > threshDeviation): #if polled distance is greater than the threshold it triggers the alarm
        alarm()

def alarm(): #alarm function triggers the pin to send up signal to buzzer, setting it off and leaving it on until manually interrupted by keyboard, essentially end condition
    while True:
        GPIO.output(BUZZER, True)

try:
    while True: #main while loop that loops awaiting input from the button to bring the signal to the down position to trigger the alarm process
        untriggered = GPIO.input(BUTTON) #untriggered initilizes to 1 as was set at the begining of the script setup
        if(untriggered == 0): #when button is pressed the system calls functions to arm the system at the current position and poll until interrupted by keyboard
            armed()
            setThresh()
            pollPosition()


finally:
    GPIO.cleanup() #when interrupted by keyboard, finally block executes and cleans up the pins so there is no hold over in-use pin conflicts between runs


