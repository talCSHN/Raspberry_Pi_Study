import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import mysql.connector

dhtPin = 23

GPIO.setmode(GPIO.BCM)
# GPIO.setup(dhtPin, GPIO.IN)

dht = adafruit_dht.DHT11(board.D23)

db = mysql.connector.connect(host='localhost', user='root', password='12345', database='testdb')
cursor = db.cursor()

while True:
	try:
		temperature = dht.temperature
		humidity = dht.humidity
		print(f'Temp: {temperature} ℃ ')
		print(f'Humid: {humidity} %')

		if (temperature != None and humidity != None):
			sql = "INSERT INTO sensor_datas (temp, humid) VALUES (%s, %s)"
			cursor.execute(sql, (int(temperature), int(humidity)))
			db.commit()
		else:
			print("sensor data doesn't exist")
		time.sleep(60)

	except RuntimeError as error:
		print(error.args[0])
	except KeyboardInterrupt:
		GPIO.cleanup()
		break

cursor.close()
db.close()
print('sensor stopped')
