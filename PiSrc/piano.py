#!/usr/bin/env python3
import RPi.GPIO as GPIO, sys, termios, tty, select, time

# ─ GPIO ─
RED, GREEN, BLUE = 14, 15, 18
PIEZO = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIEZO, GPIO.OUT)
pwm = GPIO.PWM(PIEZO, 440)      # dummy freq
pwm.start(0)                    # Duty 0 → 소리 OFF

COLORS = [RED, GREEN, BLUE]     # LED 순환용

# ─ 음계 매핑 ─
NOTE_TABLE = {
    '1': ('C4', 262),
    '2': ('D4', 294),
    '3': ('E4', 330),
    '4': ('F4', 349),
    '5': ('G4', 392),
    '6': ('A4', 440),
    '7': ('B4', 494),
    '8': ('C5', 523)
}


fd = sys.stdin.fileno()
old_attr = termios.tcgetattr(fd)
tty.setcbreak(fd)

def leds_off():
    GPIO.output([RED, GREEN, BLUE], GPIO.HIGH)

print("=== 숫자 1~8: 도레미파솔라시도,   q 또는 ESC: 종료 ===")
led_idx = 0

try:
    while True:
        # select() 로 키 입력 체크 (타임아웃 0.05 s)
        if select.select([sys.stdin], [], [], 0.05)[0]:
            ch = sys.stdin.read(1)
            if ch in NOTE_TABLE:
                name, freq = NOTE_TABLE[ch]
                print(f"{name} ({freq} Hz)")
                pwm.ChangeFrequency(freq)
                pwm.ChangeDutyCycle(50)      # 소리 ON

                leds_off()
                GPIO.output(COLORS[led_idx % 3], GPIO.LOW)
                led_idx += 1

            elif ch in ('q', '\x1b'):        # 'q' or ESC
                break

        # 아무 키도 안 누르면 소리를 끔 (1/20초 마다 체크)
        else:
            pwm.ChangeDutyCycle(0)           # 소리 OFF

except KeyboardInterrupt:
    pass
finally:
    # 복구
    termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)
    pwm.stop()
    leds_off()
    GPIO.cleanup()
    print("\n종료")
