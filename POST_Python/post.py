import RPi.GPIO as GPIO
import serial
import time
from gpiozero import MCP3008, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import spidev
import threading

# Initialize SPI for MQ-9 sensor
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Define sensor pins
gas_sensor_pin_mq2 = 14
led_pin = 15
do_pin_mq9 = 8

# Setup GPIO pins
GPIO.setup(gas_sensor_pin_mq2, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(do_pin_mq9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup serial for NEO-6M GPS Module
serial_port = "/dev/ttyS0"
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# Setup pigpio for AO-03 sensor
Device.pin_factory = PiGPIOFactory()
ao03_channel = MCP3008(channel=0)

def analog_read(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def perform_post():
    print("Performing POST checks for all modules...")
    # AO-03 POST Check
    analog_value = ao03_channel.value
    if analog_value < 0.1 or analog_value > 0.9:
        print("POST failed: Unexpected analog output from AO-03.")
        return False
    
    # MQ-2 POST Check
    if GPIO.input(gas_sensor_pin_mq2) == GPIO.LOW:
        print("POST failed: MQ-2 sensor not connected.")
        return False
    
    # MQ-9 POST Check
    sensorValue = analog_read(0)
    if sensorValue < 100 or sensorValue > 900:  # Threshold values can be adjusted
        print("POST failed: MQ-9 sensor not within expected range.")
        return False

    # NEO-6M POST Check
    ser.write(b'$PMTK220,1000*1F\r\n')  # Set update rate to 1Hz (for example)
    if ser.read(6) != b'$PMTK001':  # Expected ACK response
        print("POST failed: NEO-6M GPS module not responding.")
        return False
    
    return True

def ao03_loop():
    while True:
        oxygen_concentration = ao03_channel.value * 1023
        print(f"O2 Concentration: {oxygen_concentration:.2f} %")
        time.sleep(1)

def mq2_loop():
    while True:
        gas_level_mq2 = GPIO.input(gas_sensor_pin_mq2)
        print("Gas Level MQ-2:", gas_level_mq2)
        time.sleep(1)

def mq9_loop():
    while True:
        sensorValue = analog_read(0)
        sensor_volt = (sensorValue / 1024.0) * 5.0
        print("Sensor Volt MQ-9:", sensor_volt)
        time.sleep(1)

def neo6m_loop():
    while True:
        data = ser.readline()
        print("GPS Data:", data.decode().strip())
        time.sleep(1)

if __name__ == "__main__":
    if perform_post():
        print("POST checks passed. Initializing sensor readings...")
        # Starting separate threads for each sensor after POST checks
        threading.Thread(target=ao03_loop, daemon=True).start()
        threading.Thread(target=mq2_loop, daemon=True).start()
        threading.Thread(target=mq9_loop, daemon=True).start()
        threading.Thread(target=neo6m_loop, daemon=True).start()

        try:
            while True:  # Main thread does nothing but wait for interrupt to clean up
                time.sleep(10)
        except KeyboardInterrupt:
            print("Program terminated by user")
            GPIO.cleanup()
            ser.close()
    else:
        print("POST failed for one or more modules. Check hardware setup.")
        GPIO.cleanup()
        ser.close()
