import sys
import os
import requests
import json


import RPi.GPIO as GPIO
import time


BUTTON_GPIO = 16
USER_ID = 0
url = "http://164.92.97.79/request_user_id/"

user_id_file_path = "user_id.txt"



def request_user_id():
    try:
        r = request.get(url, timeout=1) #wait for response for 1 second before timing out
        r = response.json()
        USER_ID = r["user_id"] #need to test if this works, or if I need matchdict or something

        #Save user_id for later use
        if os.path.exists(user_id_file_path):
            try:
                os.remove(user_id_file_path)
            except:
                pass

        f = open(user_id_file_path, "w")
        f.write("USER_ID: " + USER_ID)
        f.close()
        

    except requests.exceptions.Timeout:
        print("request_user_id restful request timed out (No match ?)")


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #make it a pull up input
                                                                    #this will be default 1, pulled down by button

        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
                callback=request_user_id, bouncetime=100)   #setup interrupt on pulldown to send request
        r = request.get(url, timeout=1) #wait for response for 1 second before timing out
    except KeyboardInterrupt:
        exit
