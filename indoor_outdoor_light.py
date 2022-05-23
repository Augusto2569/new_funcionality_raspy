import RPi.GPIO as GPIO
import time
import threading
from threading import Semaphore
global in_light, out_light;
sem = Semaphore()

def setup():
    global in_light, out_light
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19,GPIO.OUT) # set GPIO pin 12 to outputmode
    GPIO.setup(26,GPIO.OUT) # set GPIO pin 12 to outputmode
    in_light = GPIO.PWM(19,100) #initialize PWM on pwmPin 100Hz frequency
    out_light = GPIO.PWM(26,100) #initialize PWM on pwmPin 100Hz frequency

    # Start PWM running, with value of 0 (pulse off)
    in_light.start(0)
    out_light.start(0)

def indoor_light():
    while True:
        in_on_off = str(input('Indoor light on/off? '))
        if in_on_off == "on":
            in_light_value = float(input('Indoor light intensity [0-100]: '))
            in_light.ChangeDutyCycle(in_light_value)
        else:
            in_light.ChangeDutyCycle(0)

def outdoor_light():
    while True:
        out_on_off = str(input('Indoor light on/off? '))
        if out_on_off == "on":
            out_light_value = float(input('Outdoor light intensity [0-100]: '))
            out_light.ChangeDutyCycle(out_light_value)
        else:
            out_light.ChangeDutyCycle(0)


def destroy():
    in_light.stop()
    out_light.stop()
    GPIO.cleanup()
    print("Goodbye!")


if __name__ == "__main__":
    setup()

    try:
        thread_indoor_light = threading.Thread(target=indoor_light, daemon=True)
        thread_outdoor_light= threading.Thread(target=outdoor_light, daemon=True)

        thread_indoor_light.start()
        thread_outdoor_light.start()

        thread_indoor_light.join()
        thread_outdoor_light.join()
        destroy()

    except KeyboardInterrupt:
        destroy()
