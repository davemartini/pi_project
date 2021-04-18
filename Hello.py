import RPi.GPIO as GPIO
import time, sched, _thread

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, False)







def blinker():
    GPIO.output(18, True)
    time.sleep(2)
    
def offer():
    GPIO.output(18, False)
    time.sleep(2)

for x in range(5):
    blinker()
    offer()
    
GPIO.cleanup()

    
    
    
    



#print("hello world")


