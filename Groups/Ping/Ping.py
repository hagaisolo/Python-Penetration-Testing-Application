# This is a ping test, just for checking
import os

hostname = "google.com"
response = os.system("ping -c 1" + hostname)

if response == 0:
    print hostname, 'is up!'
else:
    print hostname, 'is down!'