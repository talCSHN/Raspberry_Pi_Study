import RPi.GPIO as GPIO
import time

# RED, GREEN, BLUE = 14, 15, 18
piezoPin = 25

Melody = [
    ('E4', 0.5), ('F4', 0.5), ('G4', 0.25), ('A4', 0.25),
    ('G4', 0.25), ('F4', 0.25), ('E4', 0.5), ('D4', 0.5),
    ('C4', 1.0),  ('E4', 1.0)
]

freqs = {
    'C4': 261, 'D4': 294, 'E4': 329, 'F4': 349,
    'G4': 392, 'A4': 440
}

TEMPO_BPM  = 143       # 원곡 템포
BEAT       = 60 / TEMPO_BPM      # 1박 길이(초)

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

sound = GPIO.PWM(piezoPin, 440)

try:
	while True:
		sound.start(50)
		for note, length in Melody:
			sound.ChangeFrequency(freqs[note])
			time.sleep(length * BEAT)
		sound.stop()
		time.sleep(1)

except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
