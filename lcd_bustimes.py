import json
import requests

from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,23], numbering_mode=GPIO.BOARD)

# Get Bus Eireann bus information
max_results = "1"
stop_id = "231291" # Broadale bus stop number
bus_number = "220"

response = requests.get(''.join(["https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?format=json",\
	"&maxresults=", max_results, "&stopid=", stop_id, "&routeid=", bus_number]))

while True:
    try:
        lcd.clear()
        json_data = response.json()

	# Build a string with the retrieved information
	data = ""
	bus_count = int(json_data["numberofresults"])
	for i in range(0,bus_count):
		route = json_data["results"][i]["route"]
		dueTime = json_data["results"][i]["duetime"]
		data += "%s is due in %s minutes\n" % (route, dueTime)

	print(data)
	lcd.write_string(u"Bus Route %s:  %s minutes" % (route, dueTime))
	time.sleep(1)

    except:
	print("Could not find any bus data")
	print(response)
	lcd.write_string(u"Error:")
	lcd.cursor_pos = (1,0)
	lcd.write_string(u"No bus times")

