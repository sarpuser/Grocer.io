import sys
import requests
import json


import RPi.GPIO as GPIO
import time


BUTTON_GPIO = 16
USER_ID = 0


def request_user_id():
    url = "INSERT URL HERE"
    try:
        r = request.get(url, timeout=1) #wait for response for 1 second before timing out
        r = response.json()
        USER_ID = r["user_id"] #need to test if this works, or if I need matchdict or something

    except requests.exceptions.Timeout:
        print("request_user_id restful request timed out (No match ?)")


if __name__ == "__main__":
    try:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP) #might need to look into this line

        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
                callback=request_user_id, bouncetime=100)

    except KeyboardInterrupt:
        exit
