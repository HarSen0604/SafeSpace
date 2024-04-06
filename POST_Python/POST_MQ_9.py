import RPi.GPIO as GPIO
import time

DO_PIN = 8

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DO_PIN, GPIO.IN)

def loop():
    R0 = 0.91
    
    while True:
        alarm = 0
        sensor_volt = 0.0
        RS_gas = 0.0
        ratio = 0.0
        
        sensorValue = analog_read(0)
        sensor_volt = (sensorValue / 1024.0) * 5.0
        RS_gas = (5.0 - sensor_volt) / sensor_volt
        
        ratio = RS_gas / R0
        
        print("sensor_volt =", sensor_volt)
        print("RS_ratio =", RS_gas)
        print("Rs/R0 =", ratio)
        print("\n\n")
        
        alarm = GPIO.input(DO_PIN)
        
        time.sleep(1)

def analog_read(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
