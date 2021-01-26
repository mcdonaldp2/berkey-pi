 #!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import smtplib
import os
import json
from datetime import datetime,date
import calendar
import sqlite3

def getConfig():
	with open(os.path.dirname(os.path.realpath(__file__)) + '/berkey-pi.config.json') as f:
		data = json.load(f)
		return data

def setupIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.IN)

def getDayOfTheWeek():
	return calendar.day_name[date.today().weekday()]

def logFillToDB():
	connection = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/berkeydata")
	cursor = connection.cursor()
	cursor.execute(
		"Insert into BerkeyFillLog (FillTime, FillDayOfWeek) values(? , ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), getDayOfTheWeek())
	)
	
	connection.commit()
	connection.close()

def sendAlertEmail(config):
	server= smtplib.SMTP(config['smtp_server'], config['smtp_port'])
	server.starttls()
	server.login(config['smtp_auth_user'], os.environ.get('BERKEYPI_SMTP_PASSWORD'))
	msg="\r\n\r\n The Berkey is almost full! time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\r\n\r\n"
	server.sendmail(config['berkey_alert_from'], config['berkey_alert_recipients'],msg)

	server.quit()

def main():
	setupIO()
	config = getConfig()

	isInWater = False
	timeInWater = 0
	maxTimeInWater = 1


	while True:
		isInWater = GPIO.input(18) == 1
		
		if  isInWater:
			timeInWater += 1
		else:
			timeInWater = 0


		if timeInWater == maxTimeInWater:
			sendAlertEmail(config)
			logFillToDB()
		time.sleep(1)

main()




