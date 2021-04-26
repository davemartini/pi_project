import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 13
ECHO = 19
BUTTON = 23
LIGHT = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LIGHT, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LIGHT, False)


try:
    GPIO.output(LIGHT, True)
    
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    #time.sleep(.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end=time.time()
        
    duration = end-start
    distance = (duration * 17150)

    distance = round(distance, 2)

    print("Current Distance:",distance,"cm")
finally:
    GPIO.cleanup()




#print("testing the distance")



